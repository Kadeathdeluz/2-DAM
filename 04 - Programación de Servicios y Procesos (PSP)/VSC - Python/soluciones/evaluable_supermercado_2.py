
#CORREGIDO

import threading
import random
import time

cajas = threading.Semaphore(5)  # Semaforo imita a las 5 cajas abiertas
lock = threading.Lock()  # Lock para proteger los recursos
# Barrera para esperar que acaben los procesos e inicie el final del hilo principal
barrera = threading.Barrier(15)
TIEMPO_PROMOCION_ACTIVA = 1 # Duración en segundos de la promoción activa
TIEMPO_PROMOCION_INACTIVA = 2  # Tiempo entre activaciones de la promoción
# Referencia global al Timer activo
timer_activo = None


def activaPromo(ref_promocion):  # Funcion para activar la promo

    global timer_activo
    with lock:  # Bloquea los recursos
        ref_promocion[0] = True  # Activa la promo
    print("¡Promoción activada!")
    # Timer para activar la funcion de desactivar la promo
    timer_activo = threading.Timer(TIEMPO_PROMOCION_ACTIVA, desactivarPromo,args=(ref_promocion,))
    timer_activo.start()  # Inicio del timer


def desactivarPromo(ref_promocion):  # Funcion para desactivar la promo

    global timer_activo
    with lock:  # bloquea los recursos
        ref_promocion[0] = False  # Desactiva la promo
    print("La promoción ha finalizado")
    # Timer para desactivar la funcion de desactivar la promo
    timer_activo = threading.Timer(TIEMPO_PROMOCION_INACTIVA, activaPromo,args=(ref_promocion,))
    timer_activo.start()  # Inicio del timer


def pasarPorCaja(hilo, ref_promocion):

    # Tiempo aleatorio que tada en ser atendido
    tiempoAtencio = random.randint(1, 3)

    try:
        print(f"{hilo} espera en la caja")
        cajas.acquire()  # Adquiere el Semaforo
        print(f"{hilo} está siendo atendido...")
        time.sleep(tiempoAtencio)
        with (lock):  # Bloquea recursos y al finalizar los desbloquea
            if ref_promocion[0]:
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
    # Alternativa a utilizar una variable global, es utilizar una lista para tener una referencia mutable
    promo=[False]
    timer_activo = threading.Timer(TIEMPO_PROMOCION_INACTIVA, activaPromo,args=(promo,))
    timer_activo.start()

    for i in range(15):

        nuevo_hilo = threading.Thread(target=pasarPorCaja, args=(f"Cliente {i + 1}",promo))
        nuevo_hilo.start()
        clientes.append(nuevo_hilo)

    for cliente in clientes:
        cliente.join()
    
    # Cancelar el Timer activo si está en ejecución
    if timer_activo is not None:
        timer_activo.cancel()
        print("\nEl timer activo ha sido cancelado.")



    print("\nEl supermercado ha cerrado por hoy")
