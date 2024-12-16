import threading
import time
import random
from queue import Queue

# Función del productor
def productor(queue):
    for i in range(10):  # Generar un total de 10 números
        numero = random.randint(1, 100)  # Generar un número aleatorio entre 1 y 100
        queue.put(numero)  # Añadir el número a la cola
        print(f"Productor: número generado {numero}")
        time.sleep(random.randint(1, 3))  # Esperar un tiempo aleatorio entre 1 y 3 segundos

# Función del consumidor
def consumidor(queue):
    for i in range(10):  # Consumir un total de 10 números
        numero = queue.get()  # Leer un número de la cola
        print(f"Consumidor: número consumido {numero}")
        time.sleep(random.randint(2, 4))  # Simular tiempo de procesamiento entre 2 y 4 segundos

# Programa principal
if __name__ == "__main__":
    # Crear la cola
    cola = Queue()

    # Crear los hilos del productor y del consumidor
    hilo_productor = threading.Thread(target=productor, args=(cola,))
    hilo_consumidor = threading.Thread(target=consumidor, args=(cola,))

    # Iniciar los hilos
    hilo_productor.start()
    hilo_consumidor.start()

    # Esperar a que ambos hilos terminen
    hilo_productor.join()
    hilo_consumidor.join()

    print("\nTodos los números han sido producidos y consumidos.")