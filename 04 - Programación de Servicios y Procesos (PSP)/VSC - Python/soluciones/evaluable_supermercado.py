
#CORREGIDO

import threading
import random
import time

cajas = threading.Semaphore(5)  # Semaforo imita a las 5 cajas abiertas
lock = threading.Lock()  # Lock para proteger los recursos
promocion = False  # Variable que dice si esta activada la promo
# Barrera para esperar que acaben los procesos e inicie el final del hilo principal
barrera = threading.Barrier(15)
promofin = False  # Boolean para finalizar los Timer y que acabe el programa
TIEMPO_PROMOCION_ACTIVA = 5  # Duración en segundos de la promoción activa
TIEMPO_PROMOCION_INACTIVA = 10  # Tiempo entre activaciones de la promoción

def activaPromo():  # Funcion para activar la promo
    global promocion, promofin

    if promofin:  # Finaliza bucle promo
        return

    with lock:  # Bloquea los recursos
        promocion = True  # Activa la promo
    print("¡Promoción activada!")
    # Timer para activar la funcion de desactivar la promo
    desactivar = threading.Timer(TIEMPO_PROMOCION_ACTIVA, desactivarPromo)
    desactivar.start()  # Inicio del timer


def desactivarPromo():  # Funcion para desactivar la promo
    global promocion, promofin

    if promofin:  # Finaliza bucle promo
        return

    with lock:  # bloquea los recursos
        promocion = False  # Desactiva la promo
    print("La promoción ha finalizado")
    # Timer para desactivar la funcion de desactivar la promo
    activar = threading.Timer(TIEMPO_PROMOCION_INACTIVA, activaPromo)
    activar.start()  # Inicio del timer


def pasarPorCaja(hilo):

    # Tiempo aleatorio que tada en ser atendido
    tiempoAtencio = random.randint(1, 3)

    try:
        print(f"{hilo} espera en la caja")
        cajas.acquire()  # Adquiere el Semaforo
        print(f"{hilo} está siendo atendido...")
        time.sleep(tiempoAtencio)
        with (lock):  # Bloquea recursos y al finalizar los desbloquea
            if promocion:
                print(f"{hilo} ha aprovechado la promoción")
            else:
                print(f"{hilo} no ha aprovechado la promoción")
        cajas.release()  # Libera el semaforo
        print(f"{hilo} deja la caja libre")
        barrera.wait()  # Suma a la barrera una iteración
    except Exception:
        print(f"Ha ocurrido un error al atender a {hilo}")


if __name__ == "__main__":

    clientes = []
    activar = threading.Timer(TIEMPO_PROMOCION_INACTIVA, activaPromo)
    activar.start()

    for i in range(15):

        nuevo_hilo = threading.Thread(target=pasarPorCaja, args=(f"Cliente {i + 1}",))
        nuevo_hilo.start()
        clientes.append(nuevo_hilo)

    for cliente in clientes:
        cliente.join()
    promofin = True  # Finaliza bucle promo para poder cerrar el programa

    print("\nEl supermercado ha cerrado por hoy")
