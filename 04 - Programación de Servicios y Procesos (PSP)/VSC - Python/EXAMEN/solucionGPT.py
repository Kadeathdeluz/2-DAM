import threading
import time
import random
from queue import PriorityQueue

# --- Configuraciones generales ---
# Configuración de los productos
productos = ['A', 'B', 'C', 'D', 'E']
tiempo_configuracion = [0.2, 0.4, 0.3, 0.5, 0.6]  # Cambios entre productos
tiempo_produccion = [0.3, 0.35, 0.2, 0.5, 0.4]  # Producción por unidad

# Configuración del almacén
capacidad_maxima = [20, 19, 16, 22, 24]  # Máxima capacidad por producto
stock_actual = [15, 14, 12, 16, 18]  # Stock inicial
umbral_stock = 0.4  # Porcentaje de stock bajo para activar producción

# Configuración de tiendas y transporte
intervalos_pedidos = [10, 12, 8, 15, 18, 9, 11, 14, 13, 12]
tiempo_transporte_tienda = [2, 3, 1.5, 2.5, 2, 3.5, 4, 4.5, 3.2, 4.1]
capacidad_camion = 20  # Capacidad máxima de un camión

# Variables globales
cola_pedidos = PriorityQueue()  # Cola de pedidos (FIFO con prioridades)
lock_almacen = threading.Lock()  # Protección para el acceso al almacén

# --- Clases Personalizadas ---
# Clase para las máquinas de producción
class Fabrica(threading.Thread):
    def __init__(self, nombre, algoritmo):
        super().__init__()
        self.nombre = nombre
        self.algoritmo = algoritmo

    def run(self):
        while True:
            with lock_almacen:
                productos_necesarios = [capacidad_maxima[i] - stock_actual[i] for i in range(len(productos))]
            
            if max(productos_necesarios) > 0:
                if self.algoritmo == 'FIFO':
                    self.producir_fifo(productos_necesarios)
                elif self.algoritmo == 'SJF':
                    self.producir_sjf(productos_necesarios)

    def producir_fifo(self, productos_necesarios):
        for i, cantidad in enumerate(productos_necesarios):
            if cantidad > 0:
                print(f"{self.nombre} configurando para {productos[i]}.")
                time.sleep(tiempo_configuracion[i])
                for _ in range(cantidad):
                    time.sleep(tiempo_produccion[i])
                    with lock_almacen:
                        stock_actual[i] += 1
                        if stock_actual[i] >= capacidad_maxima[i]:
                            break
                print(f"{self.nombre} ha producido {cantidad} unidades de {productos[i]}.")

    def producir_sjf(self, productos_necesarios):
        orden_sjf = sorted([(i, tiempo_produccion[i], productos_necesarios[i]) for i in range(len(productos)) if productos_necesarios[i] > 0], key=lambda x: x[1])
        for producto in orden_sjf:
            i, _, cantidad = producto
            print(f"{self.nombre} configurando para {productos[i]}.")
            time.sleep(tiempo_configuracion[i])
            for _ in range(cantidad):
                time.sleep(tiempo_produccion[i])
                with lock_almacen:
                    stock_actual[i] += 1
                    if stock_actual[i] >= capacidad_maxima[i]:
                        break
            print(f"{self.nombre} ha producido {cantidad} unidades de {productos[i]}.")

# Clase para las tiendas
class Tienda(threading.Thread):
    def __init__(self, nombre, intervalo):
        super().__init__()
        self.nombre = nombre
        self.intervalo = intervalo

    def run(self):
        while True:
            time.sleep(self.intervalo)
            pedido = {producto: random.randint(0, 4) for producto in productos}
            prioridad = random.choice([1, 2])  # 1: Prioritario, 2: Normal
            cola_pedidos.put((prioridad, self.nombre, pedido))
            print(f"{self.nombre} solicitó {pedido} con prioridad {prioridad}.")

# Clase para los camiones de transporte
class Camion(threading.Thread):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def run(self):
        while True:
            if not cola_pedidos.empty():
                prioridad, tienda, pedido = cola_pedidos.get()
                with lock_almacen:
                    if self.verificar_stock(pedido):
                        self.cargar_pedido(pedido)
                        self.transportar_pedido(tienda)
                    else:
                        cola_pedidos.put((prioridad, tienda, pedido))  # Reinsertar si no hay stock suficiente

    def verificar_stock(self, pedido):
        return all(stock_actual[productos.index(p)] >= pedido[p] for p in pedido)

    def cargar_pedido(self, pedido):
        for producto, cantidad in pedido.items():
            index = productos.index(producto)
            stock_actual[index] -= cantidad
            time.sleep(0.25 * cantidad)  # Simular tiempo de carga
        print(f"{self.nombre} cargó el pedido {pedido}.")

    def transportar_pedido(self, tienda):
        tiempo_transporte = tiempo_transporte_tienda[int(tienda[-1]) - 1]
        time.sleep(tiempo_transporte)
        print(f"{self.nombre} entregó el pedido a {tienda}.")

# --- Inicialización del Sistema ---
if __name__ == "__main__":
    # Crear hilos de las fábricas
    fabricas = [Fabrica(f"Fabrica{i+1}", algoritmo='FIFO') for i in range(3)]

    # Crear hilos de las tiendas
    tiendas = [Tienda(f"Tienda{i+1}", intervalo=intervalos_pedidos[i]) for i in range(10)]

    # Crear hilos de los camiones
    camiones = [Camion(f"Camion{i+1}") for i in range(2)]

    # Iniciar todos los hilos
    for fabrica in fabricas:
        fabrica.start()
    for tienda in tiendas:
        tienda.start()
    for camion in camiones:
        camion.start()

    # Esperar la finalización (no ocurrirá porque es un sistema continuo)