"""
Enunciado:
Problema: Supermercado con Cajas y Productores
En un supermercado, hay tres cajas disponibles para atender a los clientes. Cada cliente tiene una prioridad (Alta, Media, Baja) que determinará el orden en que será atendido, además de un tiempo de compra que varía aleatoriamente. Los productos que compran los clientes son generados por productores de manera aleatoria, y estos productores también tienen una prioridad y un tiempo de creación del producto. La prioridad de los productos influye en el orden de procesamiento y los tiempos de los clientes en las cajas.

Requisitos:

Los clientes son atendidos en las cajas según un algoritmo SJF (Shortest Job First) con prioridad. Es decir, se atenderá primero al cliente con la mayor prioridad y, entre los clientes con la misma prioridad, se atenderá al que menor tiempo de compra tenga.

Los productores generan productos para los clientes y deben ser procesados siguiendo el mismo principio de SJF con prioridad. Los productores tienen una prioridad y un tiempo de creación para cada producto.

Hay que usar hilos (threads) para simular la atención de los clientes y la generación de productos.

El supermercado tiene un máximo de 3 cajas disponibles. Esto significa que solo hasta 3 clientes pueden ser atendidos al mismo tiempo.

Cada cliente será asignado a una caja cuando haya espacio disponible. Si las cajas están ocupadas, el cliente debe esperar hasta que una caja esté libre.

Se debe medir:

El tiempo total del programa (desde que inicia hasta que todos los clientes son atendidos).
El tiempo medio de espera de los clientes (desde que se generan hasta que son atendidos en las cajas).
Entrada:
Clientes: Una lista de clientes generados aleatoriamente, cada uno con una prioridad (Alta, Media, Baja) y un tiempo de compra aleatorio (de 1 a 10 segundos).
Productores: Una lista de productores generados aleatoriamente, cada uno con una prioridad (Alta, Media, Baja) y un tiempo de creación aleatorio (de 1 a 10 segundos).
Cajas: Un número máximo de cajas disponibles (en este caso 3).
Salida:
El programa debe mostrar el orden en que los clientes son atendidos y los productos son procesados.
Al final del programa, debe mostrar el tiempo total que ha durado la simulación y el tiempo medio que ha tardado cada cliente en ser atendido.
Condiciones:
Los productos generados por los productores deben ser procesados antes de que el cliente pueda realizar su compra.
El algoritmo de ordenación debe tener en cuenta tanto la prioridad de los clientes/productos como el tiempo de compra/creación.
"""

import threading
import time
import random

# Configuración
NUM_CLIENTES = 10  # Número de clientes
NUM_PRODUCTORES = 5  # Número de productores
CAPACIDAD_CAJAS = 3  # Máximo de clientes atendidos simultáneamente en las cajas
PRIORIDADES = ["Alta", "Media", "Baja"]
PESOS_PRIORIDAD = {"Alta": 0.5, "Media": 1, "Baja": 2}  # Pesos para ajustar tiempos

# Semáforos
semaforo_cajas = threading.Semaphore(CAPACIDAD_CAJAS)

# Listas compartidas
productos = []  # Lista de productos generados
clientes = []   # Lista de clientes generados

# Función para que un productor genere productos
def productor(nombre):
    prioridad_producto = random.choice(PRIORIDADES)
    tiempo_creacion = random.randint(1, 10)
    producto = {
        "nombre": f"{nombre}-Producto",
        "prioridad_producto": prioridad_producto,
        "tiempo": tiempo_creacion,
        "timestamp_creacion": time.time()
    }
    productos.append(producto)
    print(f"Productor {nombre} generó: {producto}")

# Función para procesar productos
def procesar_producto(producto):
    print(f"Procesando {producto['nombre']} - Prioridad: {producto['prioridad_producto']}, Tiempo: {producto['tiempo']}s")
    time.sleep(producto["tiempo"])

# Función para que un cliente sea atendido en una caja
def cliente_en_caja(cliente, tiempos_espera):
    with semaforo_cajas:  # Controlar la capacidad de las cajas
        tiempo_espera = time.time() - cliente["timestamp_creacion"]
        tiempos_espera.append(tiempo_espera)

        print(f"Atendiendo {cliente['nombre']} - Prioridad: {cliente['prioridad']}, Tiempo: {cliente['tiempo']}s, Espera: {tiempo_espera:.2f}s")
        time.sleep(cliente["tiempo"])
        print(f"Finalizado {cliente['nombre']}")

# Función principal
def main():
    # Inicio del programa
    tiempo_inicio_programa = time.time()

    # Generar clientes aleatorios
    for i in range(NUM_CLIENTES):
        prioridad_cliente = random.choice(PRIORIDADES)
        tiempo_compra = random.randint(1, 10)
        cliente = {
            "nombre": f"Cliente-{i+1}",
            "prioridad": prioridad_cliente,
            "tiempo": tiempo_compra,
            "timestamp_creacion": time.time()
        }
        clientes.append(cliente)

    # Generar productos con productores
    hilos_productores = []
    for i in range(NUM_PRODUCTORES):
        hilo = threading.Thread(target=productor, args=(f"Productor-{i+1}",))
        hilos_productores.append(hilo)
        hilo.start()

    # Esperar a que los productores terminen
    for hilo in hilos_productores:
        hilo.join()

    # Ordenar productos por SJF con prioridad (sin función externa)
    productos_ordenados = sorted(
        productos,
        key=lambda p: p["tiempo"] * PESOS_PRIORIDAD[p["prioridad_producto"]]  # Ordenamiento por tiempo ajustado
    )

    # Procesar productos
    for producto in productos_ordenados:
        procesar_producto(producto)

    # Ordenar clientes por SJF con prioridad (sin función externa)
    clientes_ordenados = sorted(
        clientes,
        key=lambda c: c["tiempo"] * PESOS_PRIORIDAD[c["prioridad"]]  # Ordenamiento por tiempo ajustado
    )

    # Procesar clientes en las cajas
    hilos_cajas = []
    tiempos_espera = []
    for cliente in clientes_ordenados:
        hilo = threading.Thread(target=cliente_en_caja, args=(cliente, tiempos_espera))
        hilos_cajas.append(hilo)
        hilo.start()

    # Esperar a que todos los clientes sean atendidos
    for hilo in hilos_cajas:
        hilo.join()

    # Calcular métricas
    tiempo_total_programa = time.time() - tiempo_inicio_programa
    tiempo_medio_espera = sum(tiempos_espera) / len(tiempos_espera)

    # Mostrar métricas
    print("\n--- Métricas ---")
    print(f"Tiempo total del programa: {tiempo_total_programa:.2f}s")
    print(f"Tiempo medio de espera en cajas: {tiempo_medio_espera:.2f}s")
    print("Todos los clientes han sido atendidos y productos procesados.")

# Ejecutar el programa
if __name__ == "__main__":
    main()
