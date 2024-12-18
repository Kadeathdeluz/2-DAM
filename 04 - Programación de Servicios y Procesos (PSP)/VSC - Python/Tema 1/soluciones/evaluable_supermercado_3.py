
#CORREGIDO

import threading
import random
import time

cajas = threading.Semaphore(5)  # Semáforo para las 5 cajas abiertas
lock = threading.Lock()  # Lock para proteger los recursos
barrera = threading.Barrier(15)  # Barrera para sincronización
TIEMPO_PROMOCION_ACTIVA = 1  # Duración en segundos de la promoción activa
TIEMPO_PROMOCION_INACTIVA = 2  # Tiempo entre activaciones de la promoción


class PromocionManager:
    """Clase que gestiona el estado de la promoción y su temporizador."""

    def __init__(self):
        self.promocion = False
        self.timer = None

    def activaPromo(self):
        """Activa la promoción y programa su desactivación."""
        with lock:
            self.promocion = True
        print("¡Promoción activada!")

        # Programar la desactivación de la promoción
        self.timer = threading.Timer(TIEMPO_PROMOCION_ACTIVA, self.desactivaPromo)
        self.timer.start()

    def desactivaPromo(self):
        """Desactiva la promoción y programa su reactivación."""
        with lock:
            self.promocion = False
        print("La promoción ha finalizado")

        # Programar la reactivación de la promoción
        self.timer = threading.Timer(TIEMPO_PROMOCION_INACTIVA, self.activaPromo)
        self.timer.start()

    def cancelarTimer(self):
        """Cancela el temporizador activo."""
        if self.timer:
            self.timer.cancel()
            print("\nEl temporizador activo ha sido cancelado.")


def pasarPorCaja(hilo, promocion_manager):
    """Simula que un cliente pasa por caja."""
    tiempo_atencion = random.randint(1, 3)

    try:
        print(f"{hilo} espera en la caja")
        cajas.acquire()  # Adquiere el semáforo
        print(f"{hilo} está siendo atendido...")
        time.sleep(tiempo_atencion)
        with lock:  # Accede a recursos compartidos
            if promocion_manager.promocion: #También se podría haber definido una función GET
                print(f"{hilo} ha aprovechado la promoción")
            else:
                print(f"{hilo} no ha aprovechado la promoción")
        cajas.release()  # Libera el semáforo
        print(f"{hilo} deja la caja libre")
        barrera.wait()  # Espera a que todos los clientes hayan pasado por caja
    except Exception as e:
        print(f"Ha ocurrido un error al atender a {hilo}: {e}")


if __name__ == "__main__":
    clientes = []
    promocion_manager = PromocionManager()

    # Iniciar la promoción inactiva y programar la activación
    promocion_manager.timer = threading.Timer(TIEMPO_PROMOCION_INACTIVA, promocion_manager.activaPromo)
    promocion_manager.timer.start()

    # Crear y lanzar hilos de clientes
    for i in range(15):
        nuevo_hilo = threading.Thread(target=pasarPorCaja, args=(f"Cliente {i + 1}", promocion_manager))
        nuevo_hilo.start()
        clientes.append(nuevo_hilo)

    # Esperar a que todos los clientes terminen
    for cliente in clientes:
        cliente.join()

    # Cancelar el temporizador antes de cerrar
    promocion_manager.cancelarTimer()

    print("\nEl supermercado ha cerrado por hoy")