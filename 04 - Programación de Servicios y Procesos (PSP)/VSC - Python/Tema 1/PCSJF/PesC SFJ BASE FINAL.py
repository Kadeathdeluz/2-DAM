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

# Variable de control para el número de productos vendidos
productos_comprados = 0
productos_comprados_lock = threading.Lock()  # Para evitar condiciones de carrera

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
    global productos_comprados
    # while inventario or len(inventario) < 20:  # Mientras haya productos o no se hayan creado 20 productos
    while productos_comprados < 30:
        with semaforo_cajas:  # Controla la cantidad de clientes simultáneamente
            if not inventario:  # Si no hay productos, que el cliente también cree productos
                producto = {
                    "nombre": random.choice(PRODUCTOS_DISPONIBLES),
                    "prioridad": random.choice(PRIORIDADES),
                    "tiempo_consumo": random.randint(1, 5)
                }
                inventario.append(producto)
                print(f"{cliente['nombre']} generó: {producto}")
            
            # Si hay productos, consumimos uno de ellos
            if inventario:
                producto = random.choice(inventario)  # Elegir un producto al azar
                inventario.remove(producto)  # Eliminar producto del inventario
                print(f"{cliente['nombre']} compró: {producto['nombre']} - Prioridad: {cliente['prioridad']}")

                tiempo_total = cliente['tiempo'] + producto['tiempo_consumo']
                print(f"Tiempo total de compra de {cliente['nombre']}: {tiempo_total}s")

                # Incrementar el contador de productos vendidos de manera segura
                with productos_comprados_lock:
                    productos_comprados += 1

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

    # Generación de productos por los productores al inicio pa que no esté vacío
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
     # while inventario:  # Mientras haya productos disponibles infinito
    while productos_comprados < 30:
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
# Función para aplicar la promoción
def aplicar_promocion(producto):
    global promocion_activa
    if promocion_activa:
        precio_descuento = PRECIOS[producto["nombre"]] * 0.5  # Descuento del 50%
        print(f"PROMO: {producto['nombre']} tiene descuento, nuevo precio: {precio_descuento} euros")
        return precio_descuento
    else:
        return PRECIOS[producto["nombre"]]
                # Aplicar la promoción si es que está activa
                precio_final = aplicar_promocion(producto)

                # Incrementar el contador de productos vendidos de manera segura
                with productos_comprados_lock:
                    productos_comprados += 1
                    contador_promocion += 1  # Incrementamos el contador para la promoción

                    # Si se han vendido 5 productos, activar la promoción
                    if contador_promocion == 5:
                        promocion_activa = True
                        print(f"¡PROMOCIÓN ACTIVADA! Los siguientes productos tienen un 50% de descuento.")
                        contador_promocion = 0  # Resetear el contador

Con timer:
# Función para activar y desactivar la promoción cada 10 segundos
def promocion_ciclo():
    global promocion_activa
    while productos_comprados < 30:  # Se detiene cuando se han vendido 30 productos
        time.sleep(10)  # Esperar 10 segundos
        promocion_activa = True  # Activar la promoción
        print("¡PROMOCIÓN ACTIVADA! 50% de descuento en productos.")
        time.sleep(5)  # Mantener la promoción activa durante 5 segundos
        promocion_activa = False  # Desactivar la promoción
        print("¡PROMOCIÓN DESACTIVADA! Los productos vuelven a su precio normal.")

    # Iniciar el hilo de la promoción
    hilo_promocion = threading.Thread(target=promocion_ciclo)
    hilo_promocion.start()

"""