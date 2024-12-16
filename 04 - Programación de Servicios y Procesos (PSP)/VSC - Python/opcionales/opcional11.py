import threading
import time
import random
"""
PRODUCTOR-CONSUMIDOR
"""
# Variables globales
BUF_SIZE = 10
buffer = [None]*BUF_SIZE

# Semáforos
semaforo_productor = threading.Semaphore(BUF_SIZE) # Controla la cantidad máxima de productos en el buffer
semaforo_consumidor = threading.Semaphore(0) # Inicialmente, el buffer está vacío

# Hilo productor
class Productor(threading.Thread):

    def run(self):
        global BUF_SIZE, buffer
        global semaforo_productor, semaforo_consumidor
        indice_entrada = 0

        for i in range(20):
            time.sleep(random.uniform(0.1, 0.5)) # Simula la producción de un elemento
            product = random.choice(self.products) # Coge un elemento al azar de la lista disponible
            item = f"{i+1}: {product}" #Producido el elemento i
            semaforo_productor.acquire()
            buffer[indice_entrada] = item
            indice_entrada = (indice_entrada +1)%BUF_SIZE
            print(f"El Productor {self.name} ha añadido el producto {item}")
            semaforo_consumidor.release()

# Hilo consumidor
class Consumidor(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        global BUF_SIZE, buffer
        global semaforo_productor, semaforo_consumidor
        indice_salida = 0

        for i in range(20):
            time.sleep(random.uniform(0.1, 0.5)) # Simula el tiempo de procesamiento
            semaforo_consumidor.acquire()
            producto = buffer[indice_salida]
            indice_salida = (indice_salida +1)%BUF_SIZE
            print(f"El Consumidor {self.name} ha sacado el producto {producto}")
            semaforo_productor.release()

# Hilo productor (fruta)
class ProductorFruta(Productor):
    def run(self):
        # Mandamos la lista de frutas como lista disponible
        self.products = ["naranja", "manzana", "plátano", "pomelo", "melón"]
        self.name = "<<Productor Fruta>>"
        super().run()

# Hilo productor (verdura)
class ProductorVerdura(Productor):
    def run(self):
        # Mandamos la lista de verduras como lista disponible
        self.products = ["brócoli", "alcachofa", "setas", "berenjena", "zanahoria"]
        self.name = "<<Productor Verdura>>"
        super().run()


# Main: Productor-Consumidor
if __name__ == "__main__":
    # Creamos hilos para los productores y los consumidores
    # Productores
    hilo_productor_verdura = ProductorVerdura()
    hilo_productor_fruta = ProductorFruta()
    # Consumidores
    hilo_consumidor1 = Consumidor(">>Consumidor 1<<")
    hilo_consumidor2 = Consumidor(">>Consumidor 2<<")

    # Iniciamos los hilos
    hilo_productor_verdura.start()
    hilo_productor_fruta.start()
    hilo_consumidor1.start()
    hilo_consumidor2.start()

    # Esperamos a que ambos hilos terminen
    hilo_productor_verdura.join()
    hilo_productor_fruta.join()
    hilo_consumidor1.join()
    hilo_consumidor2.join()

    print("\nTodas las operaciones han finalizado")