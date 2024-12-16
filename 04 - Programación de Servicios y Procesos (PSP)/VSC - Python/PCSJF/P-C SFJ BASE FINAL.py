"""
Imagina un sistema en el que productores generan productos y consumidores compran esos productos. Los productos tienen características específicas como tipo, prioridad y tiempo de consumo, y los clientes tienen también sus propias prioridades y tiempos asociados.

Detalles del sistema
Productores:

Hay un único productor que genera 20 productos aleatorios.
Cada producto tiene las siguientes características:
Tipo: Puede ser Pera, Plátano o Fresa.
Prioridad: Alta, Media o Baja.
Tiempo de consumo: Aleatorio entre 1 y 5 segundos.
Consumidores:

Hay 15 consumidores.
Cada consumidor tiene:
Nombre: Cliente-1, Cliente-2, ..., Cliente-15.
Prioridad: Alta, Media o Baja.
Tiempo de hacer la compra: Aleatorio entre 1 y 5 segundos.
Un consumidor consume un producto aleatorio del inventario. El tiempo total que tarda en caja es la suma del tiempo de hacer la compra y el tiempo de consumir el producto.
Cajas:

Hay 3 cajas disponibles, lo que significa que solo pueden atenderse 3 consumidores simultáneamente. El resto de consumidores debe esperar hasta que haya una caja disponible.
Política de atención:

Los consumidores son atendidos en orden SJF con prioridad, donde la prioridad ajusta los tiempos según los siguientes pesos:
Alta: Tiempo ajustado = tiempo × 0.5.
Media: Tiempo ajustado = tiempo × 1.
Baja: Tiempo ajustado = tiempo × 2.
Precios de los productos:

Pera: 5 euros.
Plátano: 10 euros.
Fresa: 15 euros.
Requisitos del programa
Los 20 productos deben ser generados al inicio por el productor y almacenados en un inventario.

Los consumidores deben elegir productos aleatorios del inventario hasta que se agoten.

Las cajas deben limitar el número de consumidores simultáneos a 3.

Los consumidores deben ser atendidos en el orden de SJF con prioridad, calculando tiempos ajustados según su prioridad.

LOS CLIENTES PUEDEN REPETIR (según sjf prio, algunos inanición)

Al finalizar el programa, debe mostrarse lo siguiente:

Tiempo total transcurrido desde el inicio del programa.
Tiempo medio de espera en las cajas.
Qué productos compró cada cliente.
Ganancia total de las cajas.
Gasto total de cada cliente.
El programa debe terminar cuando se hayan agotado todos los productos.

EXTRAS AL FINAL
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
PRODUCTOS_DISPONIBLES = ["Pera", "Platano", "Fresa"]
PRECIOS = {"Pera": 5, "Platano": 10, "Fresa": 15}

# Semáforo para controlar el número de clientes atendidos simultáneamente
semaforo_cajas = threading.Semaphore(CAPACIDAD_CAJAS)

# Listas compartidas
inventario = []  # Lista de productos generados
clientes = []   # Lista de clientes generados
productos_vendidos = []  # Para almacenar lo que cada cliente compra

# Función para que un productor genere productos
def productor(nombre):
    while len(inventario) < 20:  # Generar hasta 20 productos
        producto = {
            "nombre": random.choice(PRODUCTOS_DISPONIBLES),
            "prioridad": random.choice(PRIORIDADES),
            "tiempo_consumo": random.randint(1, 5)
        }
        inventario.append(producto)
        print(f"Productor {nombre} generó: {producto}")

# Función para que un cliente compre un producto
def cliente_en_caja(cliente):
    while inventario:  # Mientras haya productos en el inventario
        with semaforo_cajas:  # Controla la cantidad de clientes simultáneamente
            if inventario:  # Verificar si hay productos disponibles
                producto = random.choice(inventario)  # Elegir un producto al azar
                inventario.remove(producto)  # Eliminar producto del inventario
                print(f"{cliente['nombre']} compró: {producto['nombre']} - Prioridad: {cliente['prioridad']}")
                
                tiempo_total = cliente['tiempo'] + producto['tiempo_consumo']
                print(f"Tiempo total de compra de {cliente['nombre']}: {tiempo_total}s")
                
                productos_vendidos.append({
                    "cliente": cliente['nombre'],
                    "producto": producto['nombre'],
                    "precio": PRECIOS[producto['nombre']],
                    "tiempo_espera": tiempo_total
                })
                time.sleep(tiempo_total)  # Simula el tiempo de la compra

# Función para calcular el tiempo ajustado del cliente
def calcular_tiempo_ajustado_cliente(cliente):
    return cliente["tiempo"] * PESOS_PRIORIDAD[cliente["prioridad"]]

# Función principal
def main():
    # Generación de productos por los productores
    hilos_productores = []
    for i in range(NUM_PRODUCTORES):
        hilo = threading.Thread(target=productor, args=(f"Productor-{i+1}",))
        hilos_productores.append(hilo)
        hilo.start()

    # Esperamos a que todos los productores terminen
    for hilo in hilos_productores:
        hilo.join()

    # Generación de clientes
    for i in range(NUM_CLIENTES):
        prioridad_cliente = random.choice(PRIORIDADES)
        tiempo_compra = random.randint(1, 10)
        cliente = {
            "nombre": f"Cliente-{i+1}",
            "prioridad": prioridad_cliente,
            "tiempo": tiempo_compra
        }
        clientes.append(cliente)

    # Procesar los clientes en las cajas
    while inventario:  # Mientras haya productos disponibles
        # Reordenar los clientes por tiempo ajustado con prioridad antes de procesarlos
        clientes_ordenados = sorted(clientes, key=calcular_tiempo_ajustado_cliente)

        hilos_cajas = []
        for cliente in clientes_ordenados:
            hilo = threading.Thread(target=cliente_en_caja, args=(cliente,))
            hilos_cajas.append(hilo)
            hilo.start()
        

        # Esperar a que todos los clientes sean atendidos
        for hilo in hilos_cajas:
            hilo.join()

    # Calcular métricas
    tiempo_total_programa = sum([producto["tiempo_espera"] for producto in productos_vendidos])
    tiempo_medio_espera = tiempo_total_programa / len(productos_vendidos) if productos_vendidos else 0
    ganancia_total = sum([producto["precio"] for producto in productos_vendidos])

    # Mostrar métricas
    print("\n--- Métricas ---")
    print(f"Tiempo total del programa: {tiempo_total_programa:.2f}s")
    print(f"Tiempo medio de espera: {tiempo_medio_espera:.2f}s")
    print(f"Ganancia total: {ganancia_total} euros")
    for cliente in productos_vendidos:
        print(f"{cliente['cliente']} compró {cliente['producto']} por {cliente['precio']} euros")

# Ejecutar el programa
if __name__ == "__main__":
    main()

"""
LAMBDA ahorra función:
clientes_ordenados = sorted(clientes, key=lambda cliente: cliente["tiempo"] * PESOS_PRIORIDAD[cliente["prioridad"]])

Promo cada 4 compras:
compras_totales = 0  # Contador de compras totales para controlar la promoción
    global compras_totales
               # Verificar si la promoción está activa (cada 4 compras)
                if compras_totales % 4 == 0:
                    print(f"PROMO para {cliente['nombre']}!!! El producto {producto['nombre']} a mitad de precio.")
                    precio = PRECIOS[producto['nombre']] / 2  # Precio con descuento
                else:
                    precio = PRECIOS[producto['nombre']]  # Precio normal

Ídem cada 10 segundos SIN TIMER, via time (QUE NO SALÍA, DIJO)
# Variables para gestionar la promoción
tiempo_promocion = 10  # Intervalo en segundos para cambiar la promoción (activar/desactivar)
hora_ultimo_cambio = time.time()  # Hora en la que se realizó el último cambio de promoción
promo_activa = False  # Estado inicial de la promoción

                (post if inventario, claro)
                if time.time() - hora_ultimo_cambio > tiempo_promocion:
                    promo_activa = not promo_activa  # Cambiar el estado de la promoción
                    hora_ultimo_cambio = time.time()  # Actualizar el tiempo de cambio
                    estado_promo = "ACTIVA" if promo_activa else "DESACTIVADA"
                    print(f"PROMO {estado_promo}!!!")

                               # Verificar si la promoción está activa
                if promo_activa:
                    print(f"PROMO para {cliente['nombre']}!!! El producto {producto['nombre']} a mitad de precio.")
                    precio = PRECIOS[producto['nombre']] / 2  # Precio con descuento
                else:
                    precio = PRECIOS[producto['nombre']]  # Precio normal


SJF sin prio lambda:
    if orden_por_prioridad:
        clientes_ordenados = sorted(clientes, key=calcular_tiempo_ajustado_cliente)
    else:
        clientes_ordenados = sorted(clientes, key=lambda cliente: cliente['tiempo'])

SJF sin prio función:
def calcular_tiempo_cliente(cliente):
    return cliente["tiempo"]
    ( clientes_ordenados = sorted(clientes, key=calcular_tiempo_cliente) pa llamar, claro)
"""