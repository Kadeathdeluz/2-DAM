"""
Enunciado: Sistema de Productores y Consumidores con Prioridad y Semáforo
Imagina un sistema en el que un conjunto de trabajadores son responsables de producir y consumir tareas. Cada tarea tiene una prioridad (Alta, Media, Baja) y un tiempo de procesamiento aleatorio. Los trabajadores deben procesar las tareas en el orden de SJF con Prioridad, es decir, primero los que tienen mayor prioridad y, dentro de las mismas prioridades, los que menos tiempo tardan en procesarse.

El sistema debe implementar lo siguiente:

Productores/Consumidores: Los mismos trabajadores generan tareas y luego las consumen (es decir, son productores y consumidores al mismo tiempo).
SJF con Prioridad: Las tareas deben ser procesadas primero por prioridad, y dentro de las mismas prioridades, se debe procesar primero la tarea que menos tiempo de procesamiento requiera.
Semáforo: Se debe usar un semáforo para controlar el acceso concurrente a un recurso compartido (una "cola de tareas"). Solo un número limitado de tareas puede ser procesado al mismo tiempo.
Generación Aleatoria: Tanto las prioridades como los tiempos de procesamiento de las tareas deben generarse de forma aleatoria.
Especificaciones:
Prioridades: Las tareas pueden tener las siguientes prioridades: Alta, Media, Baja.
Tiempos: El tiempo de procesamiento de las tareas debe ser un número aleatorio entre 1 y 5 segundos.
Número de Trabajadores: El sistema debe tener al menos 5 trabajadores (puedes configurarlo).
Número Máximo de Tareas Simultáneas: Debe haber un máximo de 3 tareas procesándose al mismo tiempo (puedes configurarlo).
Cola de Tareas: El sistema debe mantener una cola de tareas que se vaya llenando con las tareas generadas por los trabajadores.
Requerimientos:
Implementa la solución utilizando hilos para los trabajadores.
Los trabajadores deben generar tareas de forma aleatoria y luego procesarlas siguiendo el algoritmo SJF con Prioridad.
Usa un semaforo para controlar cuántas tareas pueden ser procesadas simultáneamente.
Implementa el acceso sincronizado a la cola de tareas para evitar problemas de concurrencia.
El tiempo de procesamiento de cada tarea se debe mostrar en consola al ser procesada.
"""

import threading
import time
import random

# Configuración
NUM_TRABAJADORES = 5  # Número de trabajadores
MAX_TAREAS = 10  # Número máximo de tareas a procesar
PESOS_PRIORIDAD = {"Alta": 0.5, "Media": 1, "Baja": 2}  # Pesos para ajustar tiempos
PRIORIDADES = ["Alta", "Media", "Baja"]
MAX_RECURSO = 3  # Número máximo de tareas procesadas a la vez (semaforo)

# Semáforo
semaforo_tareas = threading.Semaphore(MAX_RECURSO)

# Cola de tareas y Lock para sincronización
cola_tareas = []
lock_cola = threading.Lock()

# Métricas
inicio_programa = time.time()
inicio_generacion = 0
total_tareas_generadas = 0
total_espera_consumidor = 0

# Función para generar una tarea
def generar_tarea(nombre):
    global total_tareas_generadas, inicio_generacion
    if total_tareas_generadas == 0:
        inicio_generacion = time.time()  # Iniciar el tiempo de generación cuando se genera la primera tarea
    prioridad = random.choice(PRIORIDADES)
    tiempo = random.randint(1, 5)  # El tiempo de procesamiento de la tarea
    tarea = {
        "nombre": f"Tarea-{nombre}",
        "prioridad": prioridad,
        "tiempo": tiempo,
        "timestamp_creacion": time.time()
    }
    
    with lock_cola:  # Bloquear acceso a la cola de tareas
        cola_tareas.append(tarea)
    
    print(f"{nombre} generó tarea: {tarea}")
    total_tareas_generadas += 1

# Función para procesar una tarea
def procesar_tarea(tarea):
    global total_espera_consumidor
    tiempo_espera = time.time() - tarea["timestamp_creacion"]
    total_espera_consumidor += tiempo_espera
    print(f"Procesando {tarea['nombre']} - Prioridad: {tarea['prioridad']}, Tiempo: {tarea['tiempo']}s")
    time.sleep(tarea["tiempo"])

# Función para calcular el tiempo ajustado en base a la prioridad
def calcular_tiempo_ajustado(tarea):
    return tarea["tiempo"] * PESOS_PRIORIDAD[tarea["prioridad"]]

# Función para el trabajador (que es productor y consumidor)
def trabajador(nombre):
    # El trabajador genera tareas
    generar_tarea(nombre)

    # Mientras haya tareas en la cola, las procesa
    while True:
        with lock_cola:  # Bloquear el acceso a la cola de tareas
            if not cola_tareas:
                break  # Si no hay tareas, el trabajador deja de trabajar

            # Ordenamos las tareas por SJF con prioridad
            cola_tareas.sort(key=calcular_tiempo_ajustado)

            # Extraemos la tarea con mayor prioridad y menor tiempo
            tarea_a_procesar = cola_tareas.pop(0)
        
        # Esperar para acceder al recurso (semaforo)
        with semaforo_tareas:
            procesar_tarea(tarea_a_procesar)

# Función principal
def main():
    # Iniciar hilos de trabajadores
    hilos_trabajadores = []
    for i in range(NUM_TRABAJADORES):
        hilo = threading.Thread(target=trabajador, args=(f"Trabajador-{i+1}",))
        hilos_trabajadores.append(hilo)
        hilo.start()

    # Esperar a que todos los trabajadores terminen
    for hilo in hilos_trabajadores:
        hilo.join()

    # Métricas de tiempo
    fin_programa = time.time()
    tiempo_total_programa = fin_programa - inicio_programa
    tiempo_total_generacion = fin_programa - inicio_generacion
    tiempo_promedio_espera_consumidor = total_espera_consumidor / total_tareas_generadas if total_tareas_generadas > 0 else 0

    print("\n--- Todas las tareas han sido procesadas ---")
    print(f"Tiempo total del programa: {tiempo_total_programa:.2f} segundos")
    print(f"Tiempo total de generación de tareas: {tiempo_total_generacion:.2f} segundos")
    print(f"Tiempo total de espera de los consumidores: {total_espera_consumidor:.2f} segundos")
    print(f"Tiempo promedio de espera por tarea: {tiempo_promedio_espera_consumidor:.2f} segundos")

# Ejecutar el programa
if __name__ == "__main__":
    main()
