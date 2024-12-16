import threading
import time
import random
from queue import PriorityQueue

# Función del productor
def productor(queue):
    for i in range(10):  # Generar un total de 10 números
        numero = random.randint(1, 100)  # Generar un número aleatorio entre 1 y 100
        prioridad = random.choice([1, 2, 3])  # 1: alta, 2: media, 3: baja
        queue.put((prioridad, numero))  # Añadir el número y su prioridad a la cola
        print(f"Productor: número generado {numero} con prioridad {prioridad}")
        time.sleep(random.randint(1, 3))  # Esperar un tiempo aleatorio entre 1 y 3 segundos

# Función del consumidor
def consumidor(queue, nivel_prioridad):
    while not queue.empty():
        prioridad, numero = queue.get()  # Leer un número y su prioridad de la cola
        if prioridad == nivel_prioridad:
            print(f"Consumidor (prioridad {nivel_prioridad}): número consumido {numero}")
            time.sleep(random.randint(2, 4))  # Simular tiempo de procesamiento entre 2 y 4 segundos
        else:
            queue.put((prioridad, numero))  # Reinsertar si no es el turno de este consumidor
            time.sleep(0.1)  # Evitar busy-waiting

# Programa principal
if __name__ == "__main__":
    # Crear la cola de prioridad
    cola = PriorityQueue()

    # Crear los hilos del productor y de los consumidores
    hilo_productor = threading.Thread(target=productor, args=(cola,))
    hilo_consumidor_alta = threading.Thread(target=consumidor, args=(cola, 1))
    hilo_consumidor_media = threading.Thread(target=consumidor, args=(cola, 2))
    hilo_consumidor_baja = threading.Thread(target=consumidor, args=(cola, 3))

    # Iniciar los hilos
    hilo_productor.start()
    hilo_consumidor_alta.start()
    hilo_consumidor_media.start()
    hilo_consumidor_baja.start()

    # Esperar a que todos los hilos terminen
    hilo_productor.join()
    hilo_consumidor_alta.join()
    hilo_consumidor_media.join()
    hilo_consumidor_baja.join()

    print("\nTodos los números han sido producidos y consumidos por prioridad.")