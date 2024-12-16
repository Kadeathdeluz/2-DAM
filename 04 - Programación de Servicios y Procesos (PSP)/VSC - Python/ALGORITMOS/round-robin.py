import threading
import time
import random

# Variables compartidas
lista_hilos = []  # Cola circular de hilos
lock = threading.Lock()  # Lock para proteger la lista
sem = threading.Semaphore(3)  # Permitir hasta 3 hilos simultáneamente

# Función que ejecutará cada hilo
def tarea_del_hilo(id_hilo, tiempo_restante):
    with sem:  # El semáforo controla el acceso
        print(f"Hilo {id_hilo} comienza su ejecución. Tiempo restante: {tiempo_restante:.2f}s")
        tiempo_a_ejecutar = min(quantum, tiempo_restante)  # Ejecutar dentro del quantum
        time.sleep(tiempo_a_ejecutar)  # Simular trabajo
        tiempo_restante -= tiempo_a_ejecutar
        if tiempo_restante > 0:
            print(f"Hilo {id_hilo} pausado. Tiempo restante: {tiempo_restante:.2f}s")
        else:
            print(f"Hilo {id_hilo} completado.")
        return tiempo_restante

# Función Round Robin con quántums
def round_robin():
    while lista_hilos:  # Mientras haya hilos en la cola
        lock.acquire()  # Proteger el acceso a la lista
        id_hilo, tiempo_restante = lista_hilos.pop(0)  # Extraemos el primer hilo y su tiempo restante
        lock.release()  # Liberamos el lock

        # Ejecutar el hilo por un quantum
        tiempo_restante = tarea_del_hilo(id_hilo, tiempo_restante)

        # Si el hilo aún tiene tiempo restante, volver a colocarlo al final de la cola
        if tiempo_restante > 0:
            lock.acquire()
            lista_hilos.append((id_hilo, tiempo_restante))
            lock.release()

# Crear hilos y asignarles un tiempo de ejecución simulado
def crear_hilos(numero_de_hilos, min_time, max_time):
    min_time, max_time

    for i in range(numero_de_hilos):
        tiempo_total = random.randint(min_time,max_time)  # Cada hilo tiene entre 1 y 7 segundos de trabajo
        lock.acquire()
        lista_hilos.append((i, tiempo_total))  # Guardar el ID del hilo y su tiempo restante
        lock.release()

# Programa principal
if __name__ == "__main__":
    quantum = int(input("Define un quantum\n"))
    num_hilos = max(10, int(input("Define un número de hilos mayor que 10 (10 por defecto)\n")) )  # Cambia este valor para probar con más hilos
    min_time = int(input("Mínimo tiempo\n"))
    max_time = int(input("Tiempo máximo\n"))
    
    crear_hilos(num_hilos, min_time, max_time)  # Crear los hilos y añadirlos a la lista
    
    print(f"Iniciando Round Robin con quantum de {quantum} segundo/s...")
    round_robin()  # Ejecutar el Round Robin
    print("Todos los hilos han terminado.")