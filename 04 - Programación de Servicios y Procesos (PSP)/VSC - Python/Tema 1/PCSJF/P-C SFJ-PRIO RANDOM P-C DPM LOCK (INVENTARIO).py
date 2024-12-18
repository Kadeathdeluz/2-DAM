"""
Enunciado:
Sistema de Gestión de Inventario con Productores y Consumidores

Imagina que estás desarrollando un sistema para gestionar el inventario de un almacén. El sistema tiene múltiples productores que generan artículos para el inventario y múltiples consumidores que toman estos artículos para su procesamiento.

Los productores y los consumidores deben funcionar de manera concurrente, pero para asegurar la integridad de los datos del inventario, el sistema debe utilizar un mecanismo de bloqueo para proteger el acceso a los recursos compartidos. Este bloqueo debe garantizar que solo un hilo pueda acceder a una sección crítica del código (el inventario) en un momento dado.

Detalles:
Productores: Los productores generan artículos que se agregan al inventario. Cada artículo tiene un identificador único y una prioridad. Los productores pueden generar varios artículos, pero el número de artículos generados por cada productor es aleatorio.

Consumidores: Los consumidores toman artículos del inventario para procesarlos. Cada consumidor debe esperar a que haya productos disponibles en el inventario. El tiempo de procesamiento de los artículos depende de la prioridad del producto que toman.

Inventario: El inventario es una lista de productos. Cada producto tiene un identificador, una prioridad (Alta, Media, Baja) y un tiempo de procesamiento. El inventario debe ser gestionado por los consumidores y productores de manera que solo un hilo (productor o consumidor) pueda modificar el inventario a la vez.

Bloqueo (lock): Para garantizar que no haya condiciones de carrera al acceder y modificar el inventario, el sistema debe usar un lock. El lock debe ser adquirido por los productores al agregar artículos y por los consumidores al retirar artículos del inventario.

Requisitos:
Generación de productos: Los productores generan artículos con una prioridad aleatoria y un tiempo de creación aleatorio entre 1 y 5 segundos.

Procesamiento de productos: Los consumidores toman productos del inventario. Si el inventario está vacío, deben esperar hasta que haya productos disponibles. El tiempo de procesamiento depende de la prioridad del artículo:

Alta: Tiempo de procesamiento reducido en un 50%.
Media: Tiempo de procesamiento sin cambios.
Baja: Tiempo de procesamiento duplicado.
Bloqueo en el inventario: El acceso al inventario debe estar protegido por un lock para evitar que múltiples hilos modifiquen el inventario simultáneamente.

Semáforo para consumidores: El número de consumidores activos a la vez debe estar limitado por un semáforo. El semáforo debe permitir que solo un número limitado de consumidores acceda al inventario en cualquier momento.

Orden de procesamiento: Los artículos deben ser procesados en el orden de su prioridad, con los artículos de alta prioridad procesados antes que los de prioridad media, y estos a su vez antes que los de baja prioridad.

Sincronización: Los productores y consumidores deben ejecutarse en hilos paralelos. El programa debe garantizar que todos los productores terminen antes de comenzar el procesamiento de productos por parte de los consumidores.

Finalización del sistema: El programa debe finalizar cuando todos los productos hayan sido generados y procesados. El sistema debe mostrar estadísticas, como el tiempo total de ejecución y el tiempo medio de espera para los consumidores.
"""

import threading
import time
import random

# Configuración
NUM_PRODUCTORES = 5  # Número de productores
NUM_CONSUMIDORES = 3  # Número de consumidores
CAPACIDAD_CONSUMIDORES = 2  # Máximo de consumidores activos simultáneamente
PRIORIDADES = ["Alta", "Media", "Baja"]
PESOS_PRIORIDAD = {"Alta": 0.5, "Media": 1, "Baja": 2}  # Pesos para ajustar tiempos
INVENTARIO_MAX = 10  # Capacidad máxima del inventario

# Semáforos
semaforo_consumidores = threading.Semaphore(CAPACIDAD_CONSUMIDORES)  # Limitar consumidores
lock_inventario = threading.Lock()  # Lock para proteger el inventario
produccion_terminada = threading.Event()  # Señal para indicar que la producción ha terminado

# Inventario
inventario = []  # Lista de productos en el inventario

# Función para que un productor genere productos
def productor(nombre):
    global inventario
    for _ in range(random.randint(1, 3)):  # Generar entre 1 y 3 productos
        prioridad = random.choice(PRIORIDADES)
        tiempo_creacion = random.randint(1, 5)
        producto = {
            "nombre": f"{nombre}-Producto-{time.time()}",
            "prioridad": prioridad,
            "tiempo": tiempo_creacion,
        }

        # Controlar el acceso al inventario con un lock
        with lock_inventario:
            if len(inventario) < INVENTARIO_MAX:
                inventario.append(producto)
                print(f"Productor {nombre} generó: {producto}")
            else:
                print(f"Inventario lleno. Productor {nombre} espera.")

        time.sleep(random.randint(1, 3))

    # Indicar que este productor ha terminado de generar productos
    print(f"Productor {nombre} ha terminado de generar productos.")
    produccion_terminada.set()  # Señaliza que la producción ha terminado

# Función para procesar un producto por un consumidor
def procesar_producto(producto):
    print(f"Procesando {producto['nombre']} - Prioridad: {producto['prioridad']}, Tiempo: {producto['tiempo']}s")
    time.sleep(producto["tiempo"] * PESOS_PRIORIDAD[producto["prioridad"]])

# Función para que un consumidor consuma productos
def consumidor(nombre):
    global inventario
    while True:
        # Semáforo para limitar los consumidores simultáneos
        with semaforo_consumidores:
            # Bloqueo para proteger el acceso al inventario
            with lock_inventario:
                if inventario:
                    producto = inventario.pop(0)
                    print(f"Consumidor {nombre} tomó el producto: {producto}")
                    procesar_producto(producto)
                elif produccion_terminada.is_set() and not inventario:
                    print(f"Consumidor {nombre} ha terminado, no hay más productos para consumir.")
                    break  # Sale del bucle cuando la producción ha terminado y el inventario está vacío
                else:
                    print(f"Consumidor {nombre} no hay productos para consumir. Esperando...")
                    time.sleep(2)

# Función principal
def main():
    # Crear y comenzar los hilos productores
    hilos_productores = []
    for i in range(NUM_PRODUCTORES):
        hilo = threading.Thread(target=productor, args=(f"Productor-{i+1}",))
        hilos_productores.append(hilo)
        hilo.start()

    # Crear y comenzar los hilos consumidores
    hilos_consumidores = []
    for i in range(NUM_CONSUMIDORES):
        hilo = threading.Thread(target=consumidor, args=(f"Consumidor-{i+1}",))
        hilos_consumidores.append(hilo)
        hilo.start()

    # Esperar a que todos los productores terminen
    for hilo in hilos_productores:
        hilo.join()

    # Esperar a que todos los consumidores terminen
    for hilo in hilos_consumidores:
        hilo.join()

    print("Proceso completado. Todos los productos han sido procesados.")

# Ejecutar el programa
if __name__ == "__main__":
    main()


