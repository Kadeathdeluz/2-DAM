"""
Enunciado
Diseña un sistema de gestión en el que cada hilo actúe como una entidad capaz de consumir productos y, después de consumirlos, generar nuevos productos para el inventario. Los productos serán consumidos siguiendo la política SJF con prioridad, en la cual:

Los productos en el inventario se ordenan por tiempo ajustado, determinado por la prioridad del producto:
Alta: tiempo multiplicado por 0.5.
Media: tiempo sin cambios.
Baja: tiempo multiplicado por 2.
El inventario compartido tiene una capacidad máxima, lo que requiere que las entidades esperen si está lleno antes de agregar nuevos productos.
Solo se permite un número limitado de entidades activas simultáneamente, controlado por un semáforo.
Objetivo: Implementar un sistema multihilo que garantice la sincronización adecuada entre las entidades y el inventario, asegurando que se respete la política SJF con prioridad.
"""
import threading
import time
import random

# Configuración
NUM_ENTIDADES = 5  # Número de entidades (hilos)
CAPACIDAD_ACTIVA = 3  # Máximo de entidades activas simultáneamente
CAPACIDAD_INVENTARIO = 10  # Capacidad máxima del inventario
PRIORIDADES = ["Alta", "Media", "Baja"]
PESOS_PRIORIDAD = {"Alta": 0.5, "Media": 1, "Baja": 2}  # Pesos para ajustar tiempos

# Semáforos y locks
semaforo_entidades = threading.Semaphore(CAPACIDAD_ACTIVA)  # Limitar entidades activas
lock_inventario = threading.Lock()  # Lock para proteger el inventario

# Inventario compartido
inventario = []

# Función para calcular el tiempo ajustado de un producto según su prioridad
def calcular_tiempo_ajustado(producto):
    return producto["tiempo"] * PESOS_PRIORIDAD[producto["prioridad"]]

# Función de una entidad que consume y luego produce
def entidad(nombre, max_iteraciones):
    global inventario
    for iteracion in range(max_iteraciones):
        # Consumir un producto
        with semaforo_entidades:
            producto = None
            with lock_inventario:
                if inventario:
                    # Ordenar el inventario por tiempo ajustado (SJF con prioridad)
                    inventario.sort(key=calcular_tiempo_ajustado)
                    # Extraer el producto con menor tiempo ajustado
                    producto = inventario.pop(0)
                    print(f"{nombre} consumió: {producto}")
                else:
                    print(f"{nombre} no encontró productos para consumir.")
                    time.sleep(1)
                    continue

        # Simular tiempo de consumo
        tiempo_consumo = producto["tiempo"] * PESOS_PRIORIDAD[producto["prioridad"]]
        time.sleep(tiempo_consumo)
        print(f"{nombre} terminó de consumir {producto['nombre']}")

        # Producir un nuevo producto
        prioridad = random.choice(PRIORIDADES)
        tiempo_produccion = random.randint(1, 5)
        nuevo_producto = {
            "nombre": f"{nombre}-Producto-{time.time()}",
            "prioridad": prioridad,
            "tiempo": tiempo_produccion,
        }

        # Agregar el nuevo producto al inventario
        with lock_inventario:
            if len(inventario) < CAPACIDAD_INVENTARIO:
                inventario.append(nuevo_producto)
                print(f"{nombre} produjo: {nuevo_producto}")
            else:
                print(f"Inventario lleno. {nombre} no pudo agregar un nuevo producto.")

        # Simular tiempo de producción
        time.sleep(tiempo_produccion)

    print(f"{nombre} completó todas sus iteraciones.")

# Función principal
def main():
    # Inicializar el inventario con algunos productos iniciales
    for i in range(5):
        inventario.append({
            "nombre": f"Producto-Inicial-{i+1}",
            "prioridad": random.choice(PRIORIDADES),
            "tiempo": random.randint(1, 5),
        })

    print("Inventario inicial:", inventario)

    # Crear y comenzar los hilos
    hilos = []
    max_iteraciones = 5  # Número máximo de iteraciones por entidad
    for i in range(NUM_ENTIDADES):
        hilo = threading.Thread(target=entidad, args=(f"Entidad-{i+1}", max_iteraciones))
        hilos.append(hilo)
        hilo.start()

    # Esperar a que todos los hilos terminen
    for hilo in hilos:
        hilo.join()

    print("Proceso completado. Inventario final:", inventario)

# Ejecutar el programa
if __name__ == "__main__":
    main()
