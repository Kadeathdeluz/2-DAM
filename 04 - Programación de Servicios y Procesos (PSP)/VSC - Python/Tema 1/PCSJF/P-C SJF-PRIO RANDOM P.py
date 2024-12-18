"""
Enunciado: Sistema de gestión de pedidos con SJF y prioridad
Una empresa de distribución tiene varios productores (tiendas) que generan pedidos con las siguientes características:

Nombre: Identifica la tienda y el pedido generado.
Prioridad: Puede ser Alta, Mediana o Baja.
Duración: Tiempo que tarda en procesarse el pedido (simulado con time.sleep).
El sistema debe gestionar y procesar estos pedidos siguiendo estas reglas:

Cada productor generará un número aleatorio de pedidos (entre 1 y 5), con prioridad y tiempo de duración asignados de forma aleatoria:
La prioridad puede ser Alta, Mediana o Baja.
El tiempo de duración estará entre 1 y 10 segundos.
Los pedidos se deben procesar siguiendo la política SJF con prioridad, donde:
El tiempo ajustado para el orden de procesamiento se calcula como:
tiempo ajustado
=
tiempo original
×
peso de la prioridad
tiempo ajustado=tiempo original×peso de la prioridad
Pesos de las prioridades:
Alta: 0.5.
Mediana: 1.
Baja: 2.
Los pedidos con menor tiempo ajustado se procesan primero.
El sistema debe permitir procesar un máximo de tres pedidos al mismo tiempo, utilizando semáforos para controlar esta capacidad.
El sistema debe garantizar que todos los pedidos se procesen antes de finalizar.
Implementa el algoritmo que gestione los pedidos desde su generación hasta su procesamiento.
"""

import threading
import time
import random

# Configuración
NUM_PRODUCTORES = 3  # Número de productores (tiendas)
CAPACIDAD_MAXIMA = 3  # Máximo de pedidos procesándose al mismo tiempo
PRIORIDADES = ["Alta", "Mediana", "Baja"]
PESOS_PRIORIDAD = {"Alta": 0.5, "Mediana": 1, "Baja": 2}  # Pesos para ajustar tiempo

# Lista compartida para los pedidos
pedidos = []

# Semáforo para limitar el número de pedidos procesándose
semaforo = threading.Semaphore(CAPACIDAD_MAXIMA)

# Función para que un productor genere pedidos aleatorios
def productor(nombre):
    num_pedidos = random.randint(1, 5)  # Cantidad aleatoria de pedidos
    for i in range(num_pedidos):
        prioridad = random.choice(PRIORIDADES)
        tiempo = random.randint(1, 10)
        pedido = {"nombre": f"{nombre}-Pedido-{i+1}", "prioridad": prioridad, "tiempo": tiempo}
        pedidos.append(pedido)
        print(f"{nombre} generó: {pedido}")

# Función para calcular el tiempo ajustado (criterio SJF con prioridad)
def calcular_tiempo_ajustado(pedido):
    return pedido["tiempo"] * PESOS_PRIORIDAD[pedido["prioridad"]]

# Función para procesar un pedido
def procesar_pedido(pedido):
    with semaforo:  # Controlar capacidad máxima
        print(f"Iniciando {pedido['nombre']} - Prioridad: {pedido['prioridad']}, Tiempo: {pedido['tiempo']}s")
        time.sleep(pedido["tiempo"])  # Simula el tiempo de procesamiento
        print(f"Finalizado {pedido['nombre']}")

# Crear productores y generar pedidos
hilos_productores = []
for i in range(NUM_PRODUCTORES):
    hilo = threading.Thread(target=productor, args=(f"Productor-{i+1}",))
    hilos_productores.append(hilo)
    hilo.start()

# Esperar a que todos los productores terminen
for hilo in hilos_productores:
    hilo.join()

# Ordenar los pedidos según SJF con prioridad
pedidos_ordenados = sorted(pedidos, key=calcular_tiempo_ajustado)

"""
Se puede eliminar la funcion calcular_tiempo_ajustado con lambda
pedidos_ordenados = sorted(
    pedidos,
    key=lambda pedido: pedido["tiempo"] * PESOS_PRIORIDAD[pedido["prioridad"]]
)
"""


# Procesar los pedidos en el orden adecuado
hilos_consumidores = []
for pedido in pedidos_ordenados:
    hilo = threading.Thread(target=procesar_pedido, args=(pedido,))
    hilos_consumidores.append(hilo)
    hilo.start()

# Esperar a que todos los pedidos sean procesados
for hilo in hilos_consumidores:
    hilo.join()

print("Todos los pedidos han sido procesados.")

