import threading
import random

# ------- Variables globales ------- {
# Representan los libros disponibles (10 al inicio del día) y los préstamos realizados durante el día (comienzan en 0)
libros_disponibles = 10
usuarios_prestamo = 0

# Creamos una variable global para cada tipo de Cliente
tomar_k = 1
devolver_k = 1

# Lock global
global_lock = threading.Lock()

# ---------------------------------- }

# ----------- Clasees ------------------ {
# Clase Cliente con un nombre
class Cliente(threading.Thread):
    def __init__ (self, nombre, lock):
        super().__init__()
        self.nombre = nombre
        self.lock = lock

# Clase Prestamo que representa a un Cliente que realiza un préstamo
class Prestamo(Cliente):
    def __init__(self, lock):
        global tomar_k
        super().__init__(f"Hilo_tomar_{tomar_k}", lock)
        tomar_k += 1

    def run(self):
        global libros_disponibles, usuarios_prestamo
        try:
            with self.lock:
                if(libros_disponibles > 0):
                    libros_disponibles -= 1
                    usuarios_prestamo += 1
                    print(f"El hilo {self.nombre} ha tomado un libro.")
                else:
                    print(f"El hilo {self.nombre} NO ha podido tomar un libro.")
        except Exception as err:
            print("ERROR PRÉSTAMO:", err)

# Clase Devolucion que representa a un Cliente que realiza una devolución
class Devolucion(Cliente):
    def __init__(self,lock):
        global devolver_k
        super().__init__(f"Hilo_devolver_{devolver_k}",lock)
        devolver_k += 1
    def run(self):
        global libros_disponibles
        try:
            with self.lock:
                if(libros_disponibles < 10):
                    libros_disponibles += 1
                    print(f"El hilo {self.nombre} ha devuelto un libro.")
                else:
                    print(f"El hilo {self.nombre} NO ha podido devolver un libro.")
        except Exception as err:
            print("ERROR DEVOLUCIÓN:", err)


# Main: Se crean 15 hilos que representan
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    
    # Lista de hilos (15 hilos)
    lista_hilos = []

    # Crea los 15 hilos y los ejecuta en función de su clase
    for _ in range(15):
        if(random.choice([True,False])):
            nuevo_hilo = Prestamo(global_lock)
        else:
            nuevo_hilo = Devolucion(global_lock)
        
        lista_hilos.append(nuevo_hilo)
        nuevo_hilo.start()
    
    for hilo in lista_hilos:
        hilo.join()
    
    # Mostrar los resultados finales
    print("\n-------------------------- RESULTADOS --------------------------\n")
    print(f"Al final del día, hay {libros_disponibles} libros disponibles.")
    print(f"Se han realizado {usuarios_prestamo} préstamos en total.")