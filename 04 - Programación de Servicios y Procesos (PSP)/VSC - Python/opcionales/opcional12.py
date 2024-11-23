import threading
from threading import Barrier
import random
import time

# Barrera para controlar que todos han terminado de hacer la pieza para comenzar a ensamblar (como la barrera está en el main, el hilo principal también espera)
make_barrier = Barrier(4)
# Barrera para controlar que todos han terminado de ensamblar para que el coche esté listo
assembly_barrier = Barrier(4)

# Fase 1
def phase_one(worker_id, random_time):
    """
    PRIMERA FASE
    """
    # Cada trabajador hace una pieza y la ensambla para crear el coche entre todos
    print(f"El trabajador {worker_id} está haciendo una pieza...")
    time.sleep(random_time) # Simula al trabajador haciendo la pieza
    print(f"El trabajador {worker_id} ha terminado su pieza.")
    make_barrier.wait()

# Fase 2
def phase_two(worker_id):
    """
    SEGUNDA FASE
    """
    # Cada trabajador ensambla su pieza
    print(f"Soy el trabajador {worker_id} y estoy ensamblando.")
    time.sleep(3) # Todas las piezas tardan 3
    print(f"Soy el trabajador {worker_id} y he terminado de ensamblar.")
    assembly_barrier.wait()

# Main:
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    """
    PRIMERA FASE
    """

    workers_list = []
    for i in range(1,5):
        # Cada trabajador tiene un tiempo aleatorio
        random_time = random.randint(1,4)
        # El worker_id de cada worker es el número de hilo.
        worker = threading.Thread(target=phase_one, args=(i,random_time))
        workers_list.append(worker)
        worker.start()
    
    # Esperamos a que todos los trabajadores terminen
    for worker in workers_list:
        worker.join()

    print("\nFase 1 terminada.\n")
    
    """
    SEGUNDA FASE
    """

    # Reinicializamos la lista para volver a usarla
    workers_list2 = []

    for i in range(1,5):
        # Cada trabajador tiene un tiempo aleatorio
        random_time = random.randint(1,4)
        # El worker_id de cada worker es el número de hilo.
        worker = threading.Thread(target=phase_two, args=(i,))
        workers_list2.append(worker)
        worker.start()
    
    # Esperamos a que todos los trabajadores terminen
    for worker in workers_list2:
        worker.join()
    
    # Finalmente el coche está listo
    print("\nSe ha juntado la 1a fase con el trabajo de ensamblaje y ya tenemos el coche listo")
    
    # Indica el final del programa (si no se muestra, algo ha ido mal)
    print("\n-------------------------- FIN --------------------------\n")