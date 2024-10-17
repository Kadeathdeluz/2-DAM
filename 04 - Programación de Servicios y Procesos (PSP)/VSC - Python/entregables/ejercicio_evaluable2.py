import threading
import random
import time

# ------- Variables globales {-------
# Representan los libros disponibles (10 al inicio del día) y los préstamos realizados durante el día
libros_disponibles = 10
usuarios_prestamo = 0

# Creamos una variable global para cada tipo de Cliente
tomar_k = 1
devolver_k = 1

# Creamos el lock pertinente para las secciones críticas
lock = threading.Lock()
# ----------------------------------}

# Actualiza la cantidad disponible de libros (-1 para Prestamos y +1 para devoluciones)
def actualizar_libros_disponibles(cantidad):
    global libros_disponibles
    with lock:
        libros_disponibles += cantidad

# Actualiza la cantidad de Prestamos únicamente si se trata de un Prestamo
def actualizar_usuarios_prestamo():
    global usuarios_prestamo
    with lock:
        usuarios_prestamo += 1

# Clase Cliente con un nombre
class Cliente:
    def __init__ (self, nombre):
        self.nombre = nombre

# Para que las clases Prestamo y Devolucion hereden de Cliente se utiliza la siguiente sintaxis:
# class ClaseHijo(ClasePadre)

# Clase Prestamo que representa a un Cliente que realiza un Prestamo (libros_disponibles -1, usuarios_prestamo +1)
class Prestamo(Cliente):
    global tomar_k

    super().__init__(f"Hilo_toma_{tomar_k}")
    actualizar_usuarios_prestamo()
    actualizar_libros_disponibles(-1)

    # En caso de crear un Prestamo, incrementamos tomar_k para que el siguiente tenga otro nombre
    tomar_k += 1


# Clase Devolucion que representa a un Cliente que realiza una Devolucion (libros_disponibles +1)
class Devolucion(Cliente):
    global devolver_k

    super().__init__(f"Hilo_devolver_{devolver_k}")
    actualizar_libros_disponibles(1)

    # En caso de crear una Devolucion, incrementamos devolver_k para que la siguiente tenga otro nombre
    devolver_k += 1

# Main: Se crean 15 hilos que representan
if __name__ == "__main__":
    pass