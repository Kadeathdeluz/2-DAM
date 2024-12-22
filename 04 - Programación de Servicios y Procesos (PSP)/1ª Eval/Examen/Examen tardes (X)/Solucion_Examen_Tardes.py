import threading
import time
import random
import queue

# Posibles mejoras: No he implementado un método muy bonito para parar. Rellenar los camiones, no esperar al stock y buscar pedidos más pequeños que entren.
# He utilizado listas y queue, para ver su funciobnamiento
# Llevar cuidado con el método sorted(), os recomiendo utilizar .sort(). Os dejo pensar el motivo y ponerlo por el foro.
# No se especificaba, pero podriamos haber sincronizado los hilos con el main, creando los hilos de las embotelladoras y camiones cada dia, utilizando semáforos como en la solución de la mañana.
# Crear los pedidos diarios, ordenarlos, crear los camiones con sus pedidos calculados, revisar si existen pedidos de produccion, crear las embotelladoras que sean necesarias y esperar al siguiente día.
# Controlando que el pedido a las embotelladoras es menor de 8 segundos, que sería la jornada laboral. 


# TIEMPOS
DIA_PRODUCCION = 8  # segundos
SEMANA_PRODUCCION = 5 * DIA_PRODUCCION
NUM_SEMANAS = 1
NUM_CERVEZAS = 6
PORCENTAJE = 0.4 #Cantidad de solicitud a la fábrica sobre la demanda_semanal

# Variables Globales

# Tiempos de producción por tipo de cerveza (segundos por palet)
tiempos_produccion = [0.35, 0.53, 0.48, 0.65, 0.8, 1]

# Capacidades máximas y stock inicial
capacidad_maxima = [120, 90, 100, 80, 70, 60]
stock_inicial = [80, 60, 70, 60, 50, 40]
stock_virtual = [0] * NUM_CERVEZAS
lock_stock_virtual = threading.Lock()

# Demanda base por tipo de cerveza
demanda_base = [50, 35, 40, 30, 25, 20]

# Capacidad de los camiones
camiones_max = [20, 20]

parar = False



class Embotelladora(threading.Thread):
    def __init__(self, nombre, cola_produccion, lock_almacen, almacen):
        super().__init__(name=nombre)
        self.cola_produccion = cola_produccion
        self.lock_almacen = lock_almacen
        self.almacen = almacen

    def run(self):
        global tiempos_produccion, stock_virtual, lock_stock_virtual, parar
        while not parar:
            try:
                # Obtener el pedido de la cola de producción
                prioridad, pedido_id, (tipo, cantidad) = self.cola_produccion.get(timeout=1)
                tiempo_produccion = tiempos_produccion[tipo] * cantidad

                print(f"{self.name} iniciando producción de {cantidad} palets de Tipo{tipo}.")
                time.sleep(tiempo_produccion*cantidad)  # Simulación del tiempo de producción
                print(f"{self.name} completó la producción de {cantidad} palets de Tipo{tipo}.")

                # Actualizar el stock del almacén
                with self.lock_almacen and lock_stock_virtual:
                    self.almacen[tipo] += cantidad
                    stock_virtual[tipo] -= cantidad

                self.cola_produccion.task_done() #Se utiliza para el join() de la Queue

            except queue.Empty:
                    continue

class Camion(threading.Thread):
    global DIA_PRODUCCION
    def __init__(self, nombre, max_carga, pedidos, lock_pedidos, lock_almacen, almacen):
        super().__init__(name=nombre)
        self.pedidos = pedidos
        self.lock_almacen = lock_almacen
        self.lock_pedidos = lock_pedidos
        self.almacen = almacen
        self.max_carga = max_carga
    
    def run(self):
        global parar
        while not parar:
            carga_total = 0
            para = False
            var = False
            while carga_total < self.max_carga:
                if para:
                    time.sleep(0.3)
                    para = False
                with self.lock_pedidos:
                    if not self.pedidos:
                        para = True
                        continue
                    tipo, cantidad = self.pedidos[0]
                    if (carga_total + cantidad) > self.max_carga: break
                    tipo, cantidad = self.pedidos.pop(0)
                
                while True:  # Seguiremos verificando hasta que se cumpla la condición
                    with self.lock_almacen:
                        if self.almacen[tipo] >= cantidad:  # Comprobamos si hay stock suficiente, si no se comprueba no lo cuento como mal
                            self.almacen[tipo] -= cantidad  # Reducimos el stock
                            carga_total += cantidad
                            print(f"{self.name} cargó {cantidad} palets de Tipo{tipo}.")
                            break  # Salimos del bucle si hemos procesado el pedido
                    time.sleep(0.2)  # Esperamos antes de volver a intentar

            print(f"{self.name} envia {carga_total} palets.")
            time.sleep(DIA_PRODUCCION)  # Simulación del tiempo de entrega


def calcular_demanda_semanal(demanda):
    coeficiente = random.uniform(0.5, 1.5)
    return [int(base * coeficiente) for base in demanda]

def planificar_produccion(almacen, demanda, lock_almacen, num):
    produccion = []
    global stock_virtual
    global lock_stock_virtual
    for tipo in range(num):
        prioridad = 3
        with lock_almacen and lock_stock_virtual:
            stock_actual = almacen[tipo] + stock_virtual[tipo]
            demanda_diaria_portipo = int(demanda[tipo] // 5)  # Pedido diario

            if stock_actual < 3 * demanda_diaria_portipo:
                prioridad = 1
            elif stock_actual < 5 * demanda_diaria_portipo:
                prioridad = 2

            if prioridad < 3:
                cantidad_a_producir = min(capacidad_maxima[tipo] - stock_actual, int(demanda_diaria_portipo*PORCENTAJE))
                if cantidad_a_producir > 0:
                    produccion.append((prioridad, tipo, cantidad_a_producir))
                    stock_virtual[tipo] += cantidad_a_producir

    return produccion


if __name__ == "__main__":

    almacen = stock_inicial[:]
    pedidos = []
    lock_almacen = threading.Lock()
    lock_pedidos = threading.Lock()
    cola_produccion = queue.PriorityQueue()

    
    # Crear embotelladoras
    embotelladoras = [Embotelladora(f"Embotelladora{i+1}", cola_produccion, lock_almacen, almacen) for i in range(3)]

    # Crear camiones
    camiones = [Camion(f"Camion{i+1}", camiones_max[i], pedidos, lock_pedidos, lock_almacen, almacen) for i in range(2)]


    for emb in embotelladoras:
        emb.start()

    for cam in camiones:
        cam.start()

    
    # Simulación
    #La simulación se podría haber implementado en otro hilo también.
    pedido_id = 0
    for semana in range(NUM_SEMANAS):
        
        print(f"Empieza la semana {semana+1}")

        if semana%2 == 0:
            demanda_semanal = calcular_demanda_semanal(demanda_base)
            print(f"Actualización demanda semanal {demanda_semanal}")

        for dia in range(5):

            # Generar pedidos diarios
            with lock_pedidos:
                for tipo in range(NUM_CERVEZAS):
                    pedidos.append((tipo, int(demanda_semanal[tipo] / 5)))
                print(f"Pedidos desordenados: {pedidos}") 
                pedidos.sort(key=lambda x: x[1], reverse=True)
                print(f"Pedidos ordenados: {pedidos}")    

            # Planificar producción
            plan_produccion = planificar_produccion(almacen, demanda_semanal, lock_almacen, NUM_CERVEZAS)
            for prioridad, tipo, cantidad in plan_produccion:
                cola_produccion.put((prioridad, pedido_id, (tipo, cantidad)))
                pedido_id += 1

            time.sleep(DIA_PRODUCCION)  # Día de producción
    

    # Esperar a que terminen los threads
    cola_produccion.join()

    parar = True

    for emb in embotelladoras:
        emb.join()

    for cam in camiones:
        cam.join()
