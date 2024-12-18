import threading
import random
import time
from threading import Semaphore

# Máximo número de clientes en la frutería
max_customers = 4
# Semáforo para controlar la entrada de clientes (max_customers)
semaphore = Semaphore(max_customers)

def customer_inside(customer_num):
    # El cliente entra y espera
    print(f"El cliente {customer_num} entra en la frutería, y espera a ser atendido.")
    
    # Por evitar no liberar el semáforo en caso de error, añadimos un bloque try-finally
    try:
        # Justo al adquirir el semáforo, el cliente es atendido
        semaphore.acquire()
        print(f"El cliente {customer_num} está siendo atendido...")
        # Simulamos tiempo atendido
        time.sleep(random.randint(1,3))
    finally:
        # Cliente deja la frutería
        semaphore.release()
        print(f"El cliente {customer_num} deja la frutería.")

# Main: Frutería con aforo de 4 clientes, 10 clientes quieren entrar
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    # Lista con los clientes
    customer_list = []

    # Creamos 10 hilos que representan a los 10 clientes y los lanzamos
    for i in range(1,11):
        customer = threading.Thread(target=customer_inside, args=(i,))
        customer_list.append(customer)
        customer.start()

    # Esperamos a que todos los clientes salgan para mostrar el mensaje final
    for customer in customer_list:
        customer.join()
        
    # Mostrar los resultados finales
    print("\n-------------------------- RESULTADOS --------------------------\n")
    print(f"La frutería ha cerrado.")