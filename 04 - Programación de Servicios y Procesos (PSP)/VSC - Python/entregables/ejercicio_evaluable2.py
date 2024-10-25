import threading
import random
"""
    Nota: Puesto que se crean 15 hilos y pueden darse los casos en que se intente devolver un libro estando todos disponibles,
    o querer tomar un libro sin quedar libros disponibles, se ha optado por implementar el contador de forma que identifique de manera inequívoca a cada hilo (de su clase).
    Esto es, aunque el hilo no realice la acción, el contador se incrementa con cada hilo de dicha clase. Y se ha creado un mensaje descriptivo en caso de no poder realizar la acción.
    P.e.: los prestamos dicen algo como "no se ha podido realizar el préstamo" y las devoluciones "no se ha podido realizar la devolución". Ya que, en caso contrario, en la ejecución pueden aparecer menos mensajes
    que hilos creados realmente. Y, podría darse el caso en que únicamente apareciera un mensaje (que el último hilo-15 realice un préstamo), o incluso 0 mensajes (que todos los hilos intenten realizar una devolución
    sin que previamente haya habido préstamos).

    @Author: Roldán Sanchis Martínez
"""
# ------- Variables globales {-------
# Representan los libros disponibles (10 al inicio del día) y los préstamos realizados durante el día (comienzan en 0)
libros_disponibles = 10
usuarios_prestamo = 0

# Creamos una variable global para cada tipo de Cliente
tomar_k = 1
devolver_k = 1

# ----------------------------------}

# Actualiza la cantidad disponible de libros (-1 para Prestamos y +1 para Devoluciones)
def actualizar_libros_disponibles(cantidad):
    global libros_disponibles
    libros_disponibles += cantidad

# Actualiza la cantidad de Prestamos únicamente si se trata de un Prestamo
def actualizar_usuarios_prestamo():
    global usuarios_prestamo
    usuarios_prestamo += 1

# Clase Cliente con un nombre
class Cliente:
    def __init__ (self, nombre, lock):
        self.nombre = nombre
        self.lock = lock

    def run(self):
        threading.Thread.__name__ = self.nombre

# Para que las clases Prestamo y Devolucion hereden de Cliente se utiliza la siguiente sintaxis:
# class ClaseHijo(ClasePadre)

# Clase Prestamo que representa a un Cliente que realiza un Prestamo (libros_disponibles -1, usuarios_prestamo +1)
class Prestamo(Cliente):
    
    def __init__(self, lock):
        super().__init__(f"Hilo_tomar_{tomar_k}", lock)

    def run(self):
        super().run()

        global tomar_k
        # Únicamente tomará un libro si hay libros disponibles
        if libros_disponibles > 0:
            with self.lock:
                actualizar_usuarios_prestamo()
                actualizar_libros_disponibles(-1)
                print("El hilo",self.nombre,"ha tomado un libro")
        else:
            print("El hilo",self.nombre,"no ha tomado un libro porque no quedaban")
        # En caso de crear un Prestamo, incrementamos tomar_k para que el siguiente tenga otro nombre
        tomar_k += 1
    


# Clase Devolucion que representa a un Cliente que realiza una Devolucion (libros_disponibles +1)
class Devolucion(Cliente):
    
    def __init__(self,lock):
        super().__init__(f"Hilo_devolver_{devolver_k}", lock)

    def run(self):
        super().run()

        global devolver_k
        # Únicamente devolverá un libro si no están todos los libros devueltos
        if libros_disponibles < 10:
            with self.lock:
                actualizar_libros_disponibles(1)
                print("El hilo",self.nombre,"ha devuelto un libro")
        else:
            print("El hilo",self.nombre,"no tiene libros para devolver")
        devolver_k += 1

    # En caso de crear una Devolucion, incrementamos devolver_k para que la siguiente tenga otro nombre
    

# Main: Se crean 15 hilos que representan
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    # Creamos el lock pertinente para las secciones críticas
    lock = threading.Lock()

    # Lista de hilos (15 hilos)
    lista_hilos = []
    # Crea los 15 hilos y los ejecuta en función de su clase
    for i in range(1,16):
        # Determinamos el tipo de hilo con un random que elige uno de los dos valores (True -> Prestamo o False -> Devolucion)
        if random.choice([True, False]):
            cliente = Prestamo(lock)
        else:
            cliente = Devolucion(lock)
        # Finalmente creamos el hilo que será Prestamo o Devolucion y pasaremos el lock que será "self.lock"
        nuevo_hilo = threading.Thread(target=cliente.run())
        lista_hilos.append(nuevo_hilo)
        nuevo_hilo.start()
    
    # Cada hilo espera a que los demás terminen (menos llamadas que ejecutra el join justo después de iniciar el hilo)
    for hilo in lista_hilos:
        hilo.join()
    
    # Mostrar los resultados finales
    print("\n-------------------------- RESULTADOS --------------------------\n")
    print(f"Al final del día, hay {libros_disponibles} libros disponibles.")
    print(f"Se han realizado {usuarios_prestamo} préstamos en total.")