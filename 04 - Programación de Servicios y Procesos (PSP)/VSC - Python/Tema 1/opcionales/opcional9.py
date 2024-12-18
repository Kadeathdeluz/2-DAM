import threading
import random
import time

# Variable global
global_counter = 0

# Clase "padre"
class Proceso(threading.Thread):
    def __init__(self, lock, random):
        super().__init__()
        self.lock = lock
        self.random = random

    def run(self):
        global global_counter
        # Sección crítica
        with self.lock:
            try:
                # Nota: la _ es porque no necesitamos el contador
                for _ in range(5):
                    # Incrementa el contador global
                    global_counter += 1
                    print(f"Contador global incrementado. Valor del contador: {global_counter}")
                    # Duerme random segundos, simula un cálculo (tarea)
                    time.sleep(self.random)
            except Exception as e:
                print(f"Error durante la ejecución: {e}")

class ProcesoA(Proceso):
    def __init__(self, lock, random):
        super().__init__(lock, random)

class ProcesoB(Proceso):
    def __init__(self, lock, random):
        super().__init__(lock, random)

class ProcesoC(Proceso):
    def __init__(self, lock, random):
        super().__init__(lock, random)

# Main: Se crean 5 hilos (2 de tipo A, 2 de tipo B y 1 de tipo C) y cada uno realiza 5 iteraciones
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    # Creamos el lock pertinente para la sección crítica
    lock = threading.Lock()
    # Lista de hilos
    threads_list = []
    # Lista de valores random
    random_values = []

    # Para que cada proceso tenga un random diferente, añadimos 3 valores a una lista para luego asignarlos a cada proceso (la _ es porque no necesitamos el contador)
    for _ in range(5):
        # Random entre 0.1 y 0.3 para el time.sleep de los hilos
        random_values.append(random.uniform(0.1, 0.3))

    # Creamos los 5 hilos de los 3 tipos de procesos
    processA = ProcesoA(lock, random_values[0])
    processA2 = ProcesoA(lock, random_values[1])
    processB = ProcesoB(lock, random_values[2])
    processB2 = ProcesoB(lock, random_values[3])
    processC = ProcesoC(lock, random_values[4])

    #Añadir los 5 hilos a la lista de hilos
    threads_list.append(processA)
    threads_list.append(processA2)
    threads_list.append(processB)
    threads_list.append(processB2)
    threads_list.append(processC)

    # Iniciar todos los hilos
    for thread in threads_list:
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads_list:
        thread.join()
    
    # Mostrar los resultados finales
    print("\n-------------------------- RESULTADOS --------------------------\n")
    print(f"Todos los hilos han terminado. Resultado del contador global: {global_counter}")