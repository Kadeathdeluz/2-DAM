import threading
import time

# Variables compartidas
cola_hilos = []  # Cola FIFO para los hilos
lock = threading.Lock()  # Lock para proteger la cola
sem = threading.Semaphore(3)  # Permitir hasta 3 hilos simultáneamente

# Función que ejecutará cada hilo
def tarea_del_hilo(id_hilo):
    with sem:  # Controlar acceso con el semáforo
        print(f"Hilo {id_hilo} comienza su ejecución.")
        time.sleep(1)  # Simular una tarea (opcional, puedes eliminar este retraso)
        print(f"Hilo {id_hilo} ha terminado.")

# Función FIFO
def fifo():
    while cola_hilos:  # Mientras haya hilos en la cola
        lock.acquire()  # Proteger el acceso a la cola
        id_hilo = cola_hilos.pop(0)  # Extraer el primer hilo de la cola
        lock.release()  # Liberar el lock

        # Ejecutar la tarea del hilo
        tarea_del_hilo(id_hilo)

# Crear hilos y añadirlos a la cola
def crear_hilos(numero_de_hilos):
    for i in range(numero_de_hilos):
        lock.acquire()
        cola_hilos.append(i)  # Añadir el ID del hilo a la cola
        lock.release()

# Programa principal
if __name__ == "__main__":
    # Solicitar el número de hilos al usuario, mínimo 10
    num_hilos = max(10, int(input("Define el número de hilos (mínimo 10):\n")))

    # Crear los hilos con los parámetros ingresados
    crear_hilos(num_hilos)

    print("\nIniciando ejecución FIFO...")
    fifo()  # Ejecutar la lógica FIFO
    print("\nTodos los hilos han terminado.")