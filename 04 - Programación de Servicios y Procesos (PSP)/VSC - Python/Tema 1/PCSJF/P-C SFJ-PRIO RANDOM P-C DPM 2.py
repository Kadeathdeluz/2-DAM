"""
Enunciado: Imagina que estás trabajando en un sistema de gestión de pedidos de un almacén. El almacén tiene varios productores que generan pedidos y varios consumidores que procesan esos pedidos.

Los productores y los consumidores deben seguir una política de SJF con prioridad para organizar los pedidos que se generan y procesan.

Detalles:

Productores: Los productores generan pedidos con una prioridad y un tiempo de producción aleatorios. La prioridad de cada pedido puede ser Alta, Media o Baja. El tiempo de producción es el tiempo que tarda el productor en generar un pedido.
Consumidores: Los consumidores procesan los pedidos. Al igual que los productores, los consumidores también tienen una prioridad y un tiempo de procesamiento aleatorios. El tiempo de procesamiento es el tiempo que tarda un consumidor en procesar un pedido después de recibirlo.
SJF con prioridad: Los pedidos deben ser procesados y generados siguiendo un algoritmo SJF con prioridad, donde la prioridad de un pedido se utiliza para modificar el tiempo de proceso y determinar el orden de ejecución. El tiempo total de cada pedido (ya sea producción o procesamiento) se ajusta según la prioridad, con las siguientes ponderaciones:

Alta: Multiplicado por 0.5 (reduce el tiempo).
Mediana: Multiplicado por 1 (sin cambio).
Baja: Multiplicado por 2 (aumenta el tiempo).
Restricciones:

Los productores pueden generar múltiples pedidos, pero el número de pedidos que cada productor puede generar es aleatorio.
Los consumidores pueden procesar pedidos hasta que todos los pedidos generados sean procesados. La cantidad de consumidores y productores es dinámica, pero se debe garantizar que los consumidores solo procesen los pedidos después de que los productores los hayan generado.
Se debe utilizar un semáforo para controlar la cantidad de pedidos que se procesan simultáneamente.
Requisitos:

Los pedidos deben ordenarse por el tiempo total ajustado (que combina el tiempo de producción y la prioridad) usando el algoritmo SJF con prioridad.
El sistema debe asegurar que no se procesen más pedidos simultáneamente de los que el sistema puede manejar.
Los productores y consumidores deben trabajar en hilos paralelos, y se debe esperar a que todos los hilos terminen antes de mostrar el resultado final.
Objetivo: Implementar un sistema de hilos que simule el proceso de generación y procesamiento de pedidos con la política de SJF con prioridad. Utilizar semáforos para controlar el procesamiento y asegurar que los pedidos sean procesados en el orden correcto según el algoritmo SJF.
"""
import threading
import time
import random

# Configuración
NUM_PRODUCTORES = 5  # Número de productores
NUM_CONSUMIDORES = 10  # Número de consumidores
CAPACIDAD_CAJAS = 3  # Máximo de pedidos procesados simultáneamente
PRIORIDADES = ["Alta", "Media", "Baja"]
PESOS_PRIORIDAD = {"Alta": 0.5, "Media": 1, "Baja": 2}  # Pesos para ajustar tiempos

# Semáforo para controlar la capacidad de procesamiento simultáneo de pedidos
semaforo_cajas = threading.Semaphore(CAPACIDAD_CAJAS)

# Listas compartidas
productos = []  # Lista de productos generados
consumidores = []   # Lista de consumidores

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

# Función para que un consumidor procese un pedido
def consumidor_en_almacen(consumidor, tiempos_espera):
    with semaforo_cajas:  # Controlar la capacidad de procesamiento simultáneo
        tiempo_espera = time.time() - consumidor["timestamp_creacion"]
        tiempos_espera.append(tiempo_espera)

        print(f"Procesando pedido de {consumidor['nombre']} - Prioridad: {consumidor['prioridad']}, Tiempo: {consumidor['tiempo']}s, Espera: {tiempo_espera:.2f}s")
        time.sleep(consumidor["tiempo"])  # Simula el tiempo de procesamiento del pedido
        print(f"Pedido de {consumidor['nombre']} procesado.")

# Función para calcular el tiempo ajustado en base a la prioridad (productos)
def calcular_tiempo_ajustado_producto(producto):
    return producto["tiempo"] * PESOS_PRIORIDAD[producto["prioridad_producto"]]

# Función para calcular el tiempo ajustado en base a la prioridad (consumidores)
def calcular_tiempo_ajustado_consumidor(consumidor):
    return consumidor["tiempo"] * PESOS_PRIORIDAD[consumidor["prioridad"]]

# Función principal
def main():
    # Inicio del programa
    tiempo_inicio_programa = time.time()

    # Generar consumidores aleatorios
    for i in range(NUM_CONSUMIDORES):
        prioridad_consumidor = random.choice(PRIORIDADES)
        tiempo_consumo = random.randint(1, 10)
        consumidor = {
            "nombre": f"Consumidor-{i+1}",
            "prioridad": prioridad_consumidor,
            "tiempo": tiempo_consumo,
            "timestamp_creacion": time.time()
        }
        consumidores.append(consumidor)

    # Generar productos con productores
    hilos_productores = []
    for i in range(NUM_PRODUCTORES):
        hilo = threading.Thread(target=productor, args=(f"Productor-{i+1}",))
        hilos_productores.append(hilo)
        hilo.start()

    # Esperar a que los productores terminen
    for hilo in hilos_productores:
        hilo.join()

    # Ordenar productos por SJF con prioridad usando la función auxiliar
    productos_ordenados = sorted(
        productos,
        key=calcular_tiempo_ajustado_producto  # Ordenamiento por tiempo ajustado
    )

    # Procesar productos
    for producto in productos_ordenados:
        procesar_producto(producto)

    # Ordenar consumidores por SJF con prioridad usando la función auxiliar
    consumidores_ordenados = sorted(
        consumidores,
        key=calcular_tiempo_ajustado_consumidor  # Ordenamiento por tiempo ajustado
    )

    # Procesar consumidores (en lugar de clientes)
    hilos_cajas = []
    tiempos_espera = []
    for consumidor in consumidores_ordenados:
        hilo = threading.Thread(target=consumidor_en_almacen, args=(consumidor, tiempos_espera))
        hilos_cajas.append(hilo)
        hilo.start()

    # Esperar a que todos los consumidores procesen los pedidos
    for hilo in hilos_cajas:
        hilo.join()

    # Calcular métricas
    tiempo_total_programa = time.time() - tiempo_inicio_programa
    tiempo_medio_espera = sum(tiempos_espera) / len(tiempos_espera)

    # Mostrar métricas
    print("\n--- Métricas ---")
    print(f"Tiempo total del programa: {tiempo_total_programa:.2f}s")
    print(f"Tiempo medio de espera en procesamiento de pedidos: {tiempo_medio_espera:.2f}s")
    print("Todos los consumidores han procesado los pedidos.")

# Ejecutar el programa
if __name__ == "__main__":
    main()
