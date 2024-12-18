import threading
import random
import time

# Almacén
BUF_SIZE = 101
buffer = [None]*BUF_SIZE

indice_entrada = 0
indice_salida = 0

# Camión buffer aux
BUF_CAM = 40
buff_cam = [None]*BUF_CAM

in_ent_cam = 0
in_sal_cam = 0

# Porcentaje mínimo para pedir (30%)
PORCENTAJE_CRIT_STOCK = 0.3

# Semáforos
# Productores
semaforo_productor = threading.Semaphore(BUF_SIZE) # Controla la cantidad máxima de productos en el buffer

# Consumidores (incialmente hay stock)
semaforo_consumidor = threading.Semaphore(75) # Inicialmente hay 75 productos en total

# Intervalos de tiempo entre pedidos
intervalos_pedidos = [10, 12, 8, 15, 18, 9, 11, 14, 13, 12]

# Tiempos de transporte del almacén a las tiendas
tiempos_transporte_tienda = [2, 3, 1.5, 2.5, 2, 3.5, 4, 4.5, 3.2, 4.1]

# Lista de productos que puede producir cada máquina
productos = [
    {"Tipo":'A', "t_config":0.2, "t_prod":0.3, "capacidad":20, "stock":15},
    {"Tipo":'B', "t_config":0.4, "t_prod":0.35, "capacidad":19, "stock":14},
    {"Tipo":'C', "t_config":0.3, "t_prod":0.2, "capacidad":16, "stock":12},
    {"Tipo":'D', "t_config":0.5, "t_prod":0.5, "capacidad":22, "stock":16},
    {"Tipo":'E', "t_config":0.6, "t_prod":0.4, "capacidad":24, "stock":18}
]

# Lock global para secciones críticas
lock = threading.Lock()

# Lista global de pedidos (cada pedido tiene un tipo y una cantidad)
pedidos = []

# Clases y métodos: algunos ejemplos
class Fabrica(threading.Thread):
    def __init__(self, i):
        super().__init__()
        self.name = f"Fabrica{i+1}"
    def run(self):
        global productos, pedidos
        for pedido in pedidos:
            producir(self, pedido)

def producir(self, pedido):
    global BUF_SIZE, buffer, productos, indice_entrada, semaforo_productor, semaforo_consumidor
    for producto in productos:
        # Simula el tiempo que tarda en configurar la maquinaria para producir dicho producto
        time.sleep(producto["t_config"])
        print(f"{self.name} configurada para {producto["Tipo"]}. V")
        with lock:
            indice_entrada = producto["stock"]
        count = 0
        # Recorremos los pedidos
        for _ in pedido["Tipo"]:
            # Para cada pedido recorremos los productos
            if(producto["Tipo"] == pedido["Tipo"]):
                # Añadimos el producto sólo si cabe en el almacén
                if(producto["stock"] < producto["capacidad"]):
                    try:
                        semaforo_productor.acquire()
                        with lock:
                            # Añadimos el producto al buffer
                            buffer[indice_entrada] = producto
                            indice_entrada = (indice_entrada +1)%BUF_SIZE
                            producto["stock"] += 1
                            count += 1
                            # Simulamos el tiempo de producción del producto
                            time.sleep(producto["t_prod"])
                        semaforo_consumidor.release()
                    except Exception as err:
                        print(f"Algo ha salido mal: {err}")
        print(f"El productor {self.name} ha producido {count} unidades de {producto["Tipo"]}, hay {producto["stock"]} en stock")
# ----------------------------------------------------------------
class Tienda(threading.Thread):
    def __init__(self, i, intervalo):
        super().__init__()
        self.name = f"Tienda{i+1}"
        self.intervalo_pedido = intervalo
    
    def run(self):
        pedir(self)
    
# Realiza la petición del pedido
def pedir(self):
    intervalo = self.intervalo_pedido
    for producto in productos:
        # Realiza los pedidos
        with lock:
            tipo = producto["Tipo"]
            cantidad = random.randint(0,4)
            pedido = {"Tipo": tipo, "Cantidad":cantidad, "Tienda": self.name}
            pedidos.append(pedido)
    # Simula la realización del pedido
    time.sleep(intervalo)

def recibir(self):
    pass

# ----------------------------------------------------------------
class Camion(threading.Thread):
    def __init__(self, i):
        super().__init__()
        self.name = f"Camión{i+1}"
    
    def run(self):
        cargar(self)

def cargar(self):
    global BUF_SIZE, BUF_CAM, buff_cam, productos, indice_salida, in_ent_cam, pedidos
    while pedidos and buff_cam < BUF_CAM:
        pedido = pedidos.pop()
        for producto in productos:
            with lock:
                indice_salida = producto["stock"]
            # Recorremos los pedidos
            for _ in pedido["Tipo"]:
                # Para cada pedido recorremos los productos
                if(producto["Tipo"] == pedido["Tipo"]):
                    # Añadimos el producto sólo si cabe en el almacén
                    if(producto["stock"] > 0):
                        try:
                            semaforo_consumidor.acquire()
                            with lock:
                                # Añadimos el producto al buffer
                                buffer[in_sal_cam] = producto
                                in_sal_cam = (in_sal_cam +1)%BUF_SIZE
                                producto["stock"] += 1
                                # Simulamos el tiempo de producción del producto
                                time.sleep(producto["t_prod"])
                            semaforo_productor.release()
                        except Exception as err:
                            print(f"Algo ha salido mal: {err}")

def descargar():
    pass

# ----------------------------------------------------------------

"""
Métodos auxiliares para modular el programa
"""
# Crea y retorna la lista de Fábricas
def crear_fabricas(num_threads: int):
    lista_fabricas = []

    for i in range(num_threads):
        hilo = Fabrica(i)
        lista_fabricas.append(hilo)
        hilo.start()

    return lista_fabricas

# Crea y retorna la lista de Tiendas, cada una con su intervalo de pedido
def crear_tiendas(num_threads: int, lista_tiempos):
    lista_tiendas = []

    for i in range(num_threads):
        hilo = Tienda(i, lista_tiempos[i])
        lista_tiendas.append(hilo)
        hilo.start()

    return lista_tiendas

# Crea y retorna la lista de Fábricas
def crear_camiones(num_threads: int):
    lista_camiones = []

    for i in range(num_threads):
        hilo = Camion(i)
        lista_camiones.append(hilo)
        hilo.start()

    return lista_camiones

# Main:
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    # Crea las tiendas (Tienda) con su intervalo de pedidos
    lista_tiendas = crear_tiendas(10, intervalos_pedidos)

    # Crea las máquinas (Fabrica)
    lista_fabricas = crear_fabricas(3)
    
    
    # Crea los camiones (Camion)
    lista_camiones = crear_camiones(2)

    print(pedidos)

    for hilo in lista_tiendas:
        hilo.join()
    for hilo in lista_fabricas:
        hilo.join()
    for hilo in lista_camiones:
        hilo.join()

"""
Ejercicio 8:

1. SJF es más eficiente, teniendo en cuenta que los pedidos son limitados y no hay riesgo de inanición.
Primero se atenderán los pedidos más cortos, permitiendo liberar recursos y servir tienedas lo antes posible.

2. He elegido el 30% porque si el stock baja del 30% podríamos llegar a tener problemas de abastecimiento.
No dispongo de datos para analizar el impacto.
"""