import threading
from threading import Timer
import random
import time

"""
VARIABLES
"""
# Número de clientes que serán atendidos
num_customers = 15
# Hay 5 cajas disponibles (el semáforo permite pasar sólo a 5)
supermarket_semaphore = threading.Semaphore(5)
# Barrera para los 15 clientes que cierra el supermercado
supermarket_barrier = threading.Barrier(num_customers)
# Determina si la promo está activa o no
promo = False # Inicialmente la promo no está activa
# Lock para actualizar la promo
lock = threading.Lock()
# Variable para controlar el temporizador
supermarket_closed = False # Inicialmente el supermercado está abierto
# Temporizador
promo_timer = None # Declaramos el temporizador sin inicializar

"""
FUNCIONES
"""
# Inicia la profmoción
def promo_on():
    global promo, promo_timer

    with lock:
        promo = True
        print("\nMegafonía >> Promoción ACTIVADA.\n")
        promo_timer = Timer(5, promo_off).start()

# Detiene la promoción
def promo_off():
    global promo, promo_timer

    with lock:
        promo = False
        print("\nMegafonía >> Promoción DESACTIVADA.\n")
        promo_timer = Timer(10, promo_on)
        promo_timer.start()

# Simula la entrada de un cliente al supermercado
def customer_asks(num_customer,random_time):
    # Como tratamos con hilos, utilizamos un bloque try para tratamiento de excepciones y para en el apartado "finally" añadir la barrera
    try:
        # Cliente entra y espera a ser atendido
        print(f"Cliente {num_customer} entra al supermercado y pide pasar por una caja.")
        
        # Cliente intenta entrar a una caja
        supermarket_semaphore.acquire()
        # Cliente entra a una caja
        print(f"Cliente {num_customer} entra a una caja.")
        if promo:
            print(f"Cliente {num_customer} ha aprovechado la promoción.")
        else:
            print(f"Cliente {num_customer} no pudo beneficiarse de la promoción.")
        # Simula cliente siendo atendido en caja
        time.sleep(random_time)
        
    finally:
        # Cliente deja la caja
        supermarket_semaphore.release()
        print(f"Cliente {num_customer} deja la caja.")

    # El super cierra cuando todos salen
    supermarket_barrier.wait()

"""
EJECUCIÓN
"""

# Main:
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    # Iniciamos la promo
    promo_on()

    # Lista que contendrá a los clientes
    customers_list = []
    # Lanzamos cada cliente como un hilo
    for i in range(1, num_customers+1):
        random_time = random.randint(1,3) # Cada cliente tarda un tiempo (entre 1 y 3 segundos)
        customer = threading.Thread(target=customer_asks, args=(i,random_time))
        customers_list.append(customer)
        customer.start()

    # Cuando todos los clientes hayan salido, el supermercado se cierra
    for customer in customers_list:
        customer.join()

    # Finalmente el supermercado cierra y muestra el mensaje de cierre (también desactiva las promos)
    supermarket_closed = True
    if promo_timer:
        promo_timer.cancel()
    print("\nMegafonía >> El supermercado ha cerrado sus puertas.\n")