import threading
import random
import time

"""
VARIABLES
"""

# Hay 5 cajas disponibles (el semáforo permite pasar sólo a 5)
supermarket_semaphore = threading.Semaphore(5)
# Barrera para los 15 clientes que cierra el supermercado
supermarket_barrier = threading.Barrier(15)
# Número de clientes que serán atendidos (15)
num_customers = 15

"""
FUNCIONES
"""

def customer_asks(num_customer):
    # Como tratamos con hilos, utilizamos un bloque try para tratamiento de excepciones y para en el apartado "finally" añadir la barrera
    try:
        # Cliente entra
        print(f"Cliente {num_customer} entra al supermercado y pide pasar por una caja.")
        # Cliente pide ir a una caja
        supermarket_semaphore.acquire()
        # Cliente entra a una caja
        print(f"Cliente {num_customer} entra a una caja.")
        # Simula cliente siendo atendido en caja
        time.sleep(random.randint(1,3))
        supermarket_semaphore.release()
        print(f"Cliente {num_customer} deja la caja.")
    finally:
        supermarket_barrier.wait()

"""
EJECUCIÓN
"""

# Main:
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    # Lista que contendrá a los clientes
    customers_list = []
    # Lanzamos cada cliente como un hilo
    for i in range(1, num_customers+1):
        customer = threading.Thread(target=customer_asks, args=(i,))
        customers_list.append(customer)
        customer.start()


    # Mostrar los resultados finales
    print("\n-------------------------- RESULTADOS --------------------------\n")

    # Cuando todos los clientes hayan salido, el supermercado se cierra
    for customer in customers_list:
        customer.join()
    print("El supermercado ha cerrado sus puertas.")

#Añadir Timer con tarea "abrir oferta" y crear Timer con tarea "cerrar oferta" (dentro del primero se lanza el segundo y viceversa)
# tempo = Timer(5, tarea)
# tempo.start()