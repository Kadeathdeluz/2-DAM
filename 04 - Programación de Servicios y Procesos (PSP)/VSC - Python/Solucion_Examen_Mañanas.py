import threading
import time
import random

#Posibles mejoras: Rellenar los camiones, no esperar al stock y buscar pedidos más pequeños que entren. Utilizar variables globales.

NUM_PROD = 5
stock_virtual_total = [0] * NUM_PROD
lock_stock_virtual = threading.Lock()

class Fabrica(threading.Thread):
    global stock_virtual_total
    global lock_stock_virtual
    def __init__(self, nombre, producto, cantidad, tiempo_produccion, productos, stock, lock_stock, semaphore):
        super().__init__()
        self.nombre = nombre
        self.producto = producto
        self.productos = productos
        self.cantidad = cantidad
        self.tiempo_produccion = tiempo_produccion
        self.stock = stock
        self.lock_stock = lock_stock
        self.semaphore = semaphore
        

    def run(self):
        print(f"{self.nombre} comenzando producción de {self.cantidad} unidades de {self.producto}.")
        time.sleep(self.tiempo_produccion * self.cantidad)  # Simula el tiempo de producción
        with self.lock_stock:
            var = self.productos.index(self.producto)
            self.stock[var] += self.cantidad
        with lock_stock_virtual:
            stock_virtual_total[var] = 0
        print(f"{self.nombre} terminó de producir {self.cantidad} unidades de {self.producto}. Stock actualizado: {self.stock}")
        self.semaphore.release()

class Almacen(threading.Thread):
    global stock_virtual_total
    global lock_stock_virtual
    def __init__(self, nombre, tiempos_configuracion, tiempos_produccion, productos, stock, max_stock, lock_stock, semaphore):
        super().__init__()
        self.nombre = nombre
        self.tiempos_configuracion = tiempos_configuracion
        self.tiempos_produccion = tiempos_produccion
        self.productos = productos
        self.stock = stock
        self.max_stock = max_stock
        self.pedidos_produccion = []
        self.lock_stock = lock_stock
        self.semaphore = semaphore
        self._stop_event = threading.Event()
        self.count = 0
        
    def stop(self):
        self._stop_event.set()
        
    def configurar(self, num, producto):
        tiempo = self.tiempos_configuracion[self.productos.index(producto)]
        print(f"Fabrica{num} configurada para {producto} (Tiempo: {tiempo}s)")
        time.sleep(tiempo)
    
    def ordenarSJF(self, pedidosSJF, tiempos_configuracion, tiempos_produccion):
        # Calcular el tiempo estimado para cada pedido
        pedidos_con_tiempo = []
        print(f"Lista de pedidos sin ordenar: {pedidosSJF}")
        for producto, cantidad in pedidosSJF:
            if producto in self.productos:
                index = self.productos.index(producto)
                # Tiempo estimado: configuración + (tiempo por unidad * cantidad)
                tiempo = tiempos_configuracion[index] + (tiempos_produccion[index] * cantidad)
                pedidos_con_tiempo.append((producto, cantidad, tiempo))
        
        # Ordenar los pedidos según el tiempo estimado (tercer elemento en la tupla)
        pedidos_con_tiempo.sort(key=lambda x: x[2])

        print(f"Lista ordenada de pedidos con tiempos: {pedidos_con_tiempo}")
        
        # Devolver el array original de pedidos pero ordenado
        array = [(producto, cantidad) for producto, cantidad, _ in pedidos_con_tiempo]
        print(f"Lista ordenada de pedidos con tiempos: {array}")
        return array
        

    def revisar_stock(self):
        with self.lock_stock and lock_stock_virtual:
            for i, cantidad_actual in enumerate(self.stock):
                max_cantidad = self.max_stock[i]
                stock_virtual = stock_virtual_total[i]
                if (cantidad_actual+stock_virtual) < 0.3 * max_cantidad:
                    cantidad_pedido = int(0.5 * max_cantidad)
                    producto = self.productos[i]
                    stock_virtual_total[i] += cantidad_pedido
                    self.pedidos_produccion.append((producto, cantidad_pedido))
                    print(f"{self.nombre} detectó stock bajo de {producto}. Pedido generado: {cantidad_pedido}")

    def run(self):
        para=False
        while not self._stop_event.is_set():
            if para:
                time.sleep(0.5)
                para= False
            self.revisar_stock()
            with self.lock_stock:
                if not self.pedidos_produccion:
                    para=True
                    continue

                # Seleccionar el pedido FIFO
                #pedido = self.pedidos_produccion.pop(0)

                # Seleccionar el pedido SJF

                self.pedidos_produccion = self.ordenarSJF(self.pedidos_produccion, self.tiempos_configuracion, self.tiempos_produccion)
                pedido = self.pedidos_produccion.pop(0)
            
            producto, cantidad = pedido
            tiempo_produccion = self.tiempos_produccion[self.productos.index(producto)]

            self.semaphore.acquire()  # Limita el número de hilos concurrentes
            self.count = (self.count % 3) + 1
            self.configurar(self.count, producto)
            hilo = Fabrica(f"Fabrica{self.count}", producto, cantidad, tiempo_produccion, self.productos, self.stock, self.lock_stock, self.semaphore)
            hilo.start()
            print(f"Se pone en funcionamiento la Fabrica{self.count}")
            

class Tienda(threading.Thread):
    def __init__(self, nombre, productos, intervalo_pedidos, pedidos_normales, pedidos_prioritarios, lock_pedidos):
        super().__init__()
        self.nombre = nombre
        self.productos = productos
        self.intervalo_pedidos = intervalo_pedidos
        self.pedidos_normales = pedidos_normales
        self.pedidos_prioritarios = pedidos_prioritarios
        self.lock_pedidos = lock_pedidos
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set(): #Lo añado para parar pero no es necesario
            time.sleep(self.intervalo_pedidos)
            pedido = {prod: random.randint(0, 4) for prod in self.productos}
            prioridad = random.choice([False, True])  # False: normal, True: alta
            with self.lock_pedidos:
                if prioridad:
                    self.pedidos_prioritarios.append((self.nombre, pedido))
                else:
                    self.pedidos_normales.append((self.nombre, pedido))
                print(f"{self.nombre} solicitó {pedido} con prioridad {'alta' if prioridad else 'normal'}")

class Camion(threading.Thread):
    def __init__(self, nombre, productos, stock, pedidos_normales, pedidos_prioritarios, tiempos_transporte_tienda, lock_stock, lock_pedidos):
        super().__init__()
        self.nombre = nombre
        self.productos = productos
        self.stock = stock
        self.pedidos_normales = pedidos_normales
        self.pedidos_prioritarios = pedidos_prioritarios
        self.tiempos_transporte_tienda = tiempos_transporte_tienda
        self.lock_stock = lock_stock
        self.lock_pedidos = lock_pedidos
        self._stop_event = threading.Event()
        self.tiendas = []
        self.restriccioncarga = 20
        self.restricciontiendas = 4

    def stop(self):
        self._stop_event.set()

    def sumarTiendas(self, shop, contador):
        if shop not in self.tiendas:
            self.tiendas.append(shop)
            contador += 1
        return contador
    
    def revisarMAX(self, total, pedido, max):
        actual = 0
        for prod, cantidad in pedido.items():
            actual += cantidad
        return True if (total+actual) > max else False
        

    def run(self):
        while not self._stop_event.is_set(): #Lo añado para parar pero no es necesario
            carga = 0
            contador_tiendas = 0
            tiempo_acumulado = 0
            del self.tiendas[:]
            
            while carga < self.restriccioncarga and contador_tiendas < self.restricciontiendas:
            
                contador_normales=2
                with self.lock_pedidos:
                    """Los pedidos prioritarios se ven perjudicados con este sistema, pero normalmente no deberiamos tener muchos pedidos prioritarios.
                    Aunque puse que fuera al azar, para simplificar, por lo que la mitad de ellos son prioritarios. Fallo mío."""
                    
                    if self.pedidos_prioritarios and contador_normales == 2:
                        tienda, pedido = self.pedidos_prioritarios[0]
                        if self.revisarMAX(carga, pedido, self.restriccioncarga): break
                        tienda, pedido = self.pedidos_prioritarios.pop(0)
                        contador_normales=0
                    elif self.pedidos_normales:
                        tienda, pedido = self.pedidos_normales[0]
                        if self.revisarMAX(carga, pedido, self.restriccioncarga): break
                        tienda, pedido = self.pedidos_normales.pop(0)
                        contador_normales+=1
                    elif self.pedidos_prioritarios:
                        tienda, pedido = self.pedidos_prioritarios[0]
                        if self.revisarMAX(carga, pedido, self.restriccioncarga): break
                        tienda, pedido = self.pedidos_prioritarios.pop(0)
                        contador_normales=0
                    else:
                        continue

                #Sumar tiendas
                contador_tiendas=self.sumarTiendas(tienda, contador_tiendas)

                #Sumar tiempo de transporte

                numero_tienda = int(tienda.replace("Tienda", "")) - 1
                tiempo_acumulado += self.tiempos_transporte_tienda[numero_tienda]
                print(f"Añadiendo la {tienda} a la ruta del {self.nombre} : tiempo total {tiempo_acumulado}")

                print(f"{self.nombre} cargando pedido para {tienda}: {pedido}")
                for prod, cantidad in pedido.items():
                    """Añado el comentario a raíz de un correo de David preguntado sobre este problema: Yo lo he simplificado poniendo un bucle que va comprobando el stock del almacén,
                    libera el lock() del stock durante unas décimas de segundo para que las fábricas actualicen el stock y vuelve a comprobar hasta que existe el suficiente.
                    No es lo más efeciente porque el camión esta parado hasta que consigue stock, pero si supones que puedes ajustar la producción de la fábrica para que esto no suela pasar,
                    sería un caso bastante raro. De todas formas, también se podría controlar al buscar el pedido en la cola y no seleccionar pedidos con falta de stock en el almacén.
                    Lo bueno de estos problemas es que existen muchas posibilidades."""
                    while True:  # Seguiremos verificando hasta que se cumpla la condición
                        with self.lock_stock:
                            var = self.productos.index(prod)
                            if self.stock[var] >= cantidad:  # Comprobamos si hay stock suficiente, si no se comprueba no lo cuento como mal
                                self.stock[var] -= cantidad  # Reducimos el stock
                                carga += cantidad
                                break  # Salimos del bucle si hemos procesado el pedido
                        time.sleep(0.2)  # Esperamos antes de volver a intentar
                    time.sleep(0.25 * cantidad)  # Tiempo de carga
                    

            print(f"{self.nombre} transportando pedido hacia {self.tiendas} (Carga total: {carga})")
            time.sleep(tiempo_acumulado)
            print(f"{self.nombre} entregó el pedido a las tiendas: {self.tiendas}")
                            
            

if __name__ == "__main__":

    # Configuración de la producción y tiempos
    tiempos_configuracion = [0.2, 0.4, 0.3, 0.5, 0.6]  # A, B, C, D, E
    tiempos_produccion = [0.3, 0.35, 0.2, 0.5, 0.4]  # A, B, C, D, E
    productos = ['A', 'B', 'C', 'D', 'E']
    capacidad_maxima = [20, 19, 16, 22, 24]
    stock_inicial = [15, 14, 12, 16, 18]
    intervalos_pedidos = [10, 12, 8, 15, 18, 9, 11, 14, 13, 12]
    tiempos_transporte_tienda = [2, 3, 1.5, 2.5, 2, 3.5, 4, 4.5, 3.2, 4.1]
    NUM_TIENDAS = 10
    NUM_CAMIONES = 2

    # Variables
    semaphore = threading.Semaphore(3)
    lock_stock = threading.Lock()
    lock_pedidos = threading.Lock()
    pedidos_normales = []
    pedidos_prioritarios = []
    stock = stock_inicial[:]

    #Si utilizamos variables globales se simplifica mucho el código, no es necesario que todas sean locales.

    # Inicialización de hilos
    fabrica = Almacen(f"Almacen", tiempos_configuracion, tiempos_produccion, productos, stock, capacidad_maxima, lock_stock, semaphore)
    tiendas = [Tienda(f"Tienda{i+1}", productos, intervalos_pedidos[i], pedidos_normales, pedidos_prioritarios, lock_pedidos) for i in range(NUM_TIENDAS)]
    camiones = [Camion(f"Camion{i+1}", productos, stock, pedidos_normales, pedidos_prioritarios, tiempos_transporte_tienda, lock_stock, lock_pedidos) for i in range(NUM_CAMIONES)]

    # Inicio de hilos
    fabrica.start()
    
    for t in tiendas:
        t.start()
    for c in camiones:
        c.start()

    #Parte opcional para parar los hilos después de 30 segundos.
    try:
        time.sleep(60)
    finally:
        # Fin de hilos
        fabrica.stop()
        for t in tiendas:
            t.stop()
        for c in camiones:
            c.stop()
        fabrica.join()
        for t in tiendas:
            t.join()
        for c in camiones:
            c.join()
        


    
