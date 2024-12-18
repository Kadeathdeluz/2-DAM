# Importación de módulos
import threading
import random
import time

# Variables globales
libros_disponibles = 10  # Cantidad inicial de libros en la biblioteca.
usuarios_prestamos = 0   # Total de préstamos realizados durante el día.
lock = threading.Lock()  # Lock para prevenir problemas de concurrencia.


class Biblioteca(threading.Thread):
    """
    Clase base que define la estructura para las operaciones de biblioteca.
    Hereda de Thread.
    """
    def __init__(self, nombre_hilo):
        super().__init__(name=nombre_hilo)  # Llamar al constructor de Thread para inicializar el hilo con su nombre.
        self.nombre_hilo = nombre_hilo
    
    def run(self):
        """Método que se ejecuta cuando el hilo inicia. Llama al método ejecutar_accion"""
        self.ejecutar_accion()  # Llama al método que será implementado por las clases hijas
    
    def ejecutar_accion(self):   
        """Método que será implementado por las clases hijas"""
        pass

class ClientePrestamo(Biblioteca):
    """
    Clase que maneja las operaciones de préstamo de libros.
    Reduce la cantidad de libros disponibles e incrementa el contador de préstamos totales.
    """
    def ejecutar_accion(self):
        global libros_disponibles, usuarios_prestamos # Acceder a las variables globales.
        
        try: # Control de excepciones
            with lock: # Uso de 'with' junto con lock para evitar que varios hilos puedan modificar las variables globales a la vez.
                if libros_disponibles > 0: # Verificar que hay libros disponibles para prestar.
                    libros_disponibles -= 1 # Reducir el total de libros disponibles en 1.
                    usuarios_prestamos += 1 # Aumentar el total de préstamos en 1.
                    print(f"{self.nombre_hilo}: Libro prestado exitosamente. "
                          f"Quedan {libros_disponibles} libros.")
                else: # Mensaje para el caso de que no hayan libros disponibles.
                    print(f"{self.nombre_hilo}: No hay libros disponibles para prestar.")
                
                time.sleep(0.1) # Pausa para simular tiempo de procesamiento.
        
        except Exception as e: # Capturar y mostrar posibles errores de ejecución en el hilo.
            print(f"Error en {self.nombre_hilo}: {str(e)}")

class ClienteDevolucion(Biblioteca):
    """
    Clase que maneja las operaciones de devolución de libros.
    Incrementa la cantidad de libros disponibles en el caso de haber préstamos activos.
    """
    def ejecutar_accion(self):
        global libros_disponibles # Acceder a las variables globales.
        
        try: # Control de excepciones
            with lock: # Proteger la sección crítica con lock.
                if libros_disponibles < 10: # Verificar que haya libros prestados.
                    libros_disponibles += 1 # Aumentar el total de libros disponibles en 1.
                    print(f"{self.nombre_hilo}: Libro devuelto exitosamente. "
                          f"Ahora hay {libros_disponibles} libros.")
                else: # Mensaje para el caso de que no hayan libros prestados.
                    print(f"{self.nombre_hilo}: No se pueden devolver libros en este momento.")
                
                time.sleep(0.1) # Pausa para simular tiempo de procesamiento.
        
        except Exception as e: # Capturar posibles errores.
            print(f"Error en {self.nombre_hilo}: {str(e)}")

def crear_y_ejecutar_hilos():
    """
    Crea y ejecuta 15 hilos aleatorios que realizan operaciones de préstamo o devolución.
    Mantiene contadores separados para cada tipo de hilo.
    Devuelve la lista de hilos creados.
    """
    hilos = [] # Crear lista para almacenar los hilos.
    contador_prestamos = 1    # Contador para nombrar hilos de préstamo.
    contador_devoluciones = 1 # Contador para nombrar hilos de devolución.
    
    # Crear 15 hilos
    for _ in range(15):
        # Decidir aleatoriamente si el hilo será de préstamo (True) o devolución (False).
        if random.choice([True, False]):
            # Crear un hilo de préstamo usando contador_prestamos
            nombre_hilo = f"Hilo_tomar_{contador_prestamos}" # Nombrar para el hilo de préstamo.
            hilo = ClientePrestamo(nombre_hilo) # Crear un nuevo hilo de ClientePrestamo con el nombre personalizado.
            contador_prestamos += 1 # Incrementar solo el contador de préstamos
        else:
            # Crear un hilo de devolución usando contador_devoluciones
            nombre_hilo = f"Hilo_devolver_{contador_devoluciones}" # NOmbrar el hilo de devolución.
            hilo = ClienteDevolucion(nombre_hilo) # Crear un nuevo hilo de ClienteDevolucion con el nombre personalizado.
            contador_devoluciones += 1 # Incrementar el contador de devoluciones.
        hilos.append(hilo) # Añadir el hilo a la lista para poder hacer join después.
    
    # Iniciar la ejecución de cada hilo.
    for hilo in hilos:
        hilo.start() 
        
    
    return hilos # Devolver la lista de hilos creados.

if __name__ == "__main__":
    """
    Punto de entrada principal del programa.
    Simula la apertura de la biblioteca creando los hilos, esperando su finalización y mostrando los resultados.
    """
    # Mostrar mensaje de inicio y estado inicial
    print("=== Iniciando simulación de biblioteca ===")
    print(f"Libros iniciales: {libros_disponibles}")
    
    # Crear y ejecutar los hilos
    hilos = crear_y_ejecutar_hilos()
    
    # Esperar a que todos los hilos terminen antes de mostrar el resultado final
    for hilo in hilos:
        hilo.join()
    
    # Mostrar el estado final de la biblioteca
    print("\n=== Simulación finalizada ===")
    print(f"Libros disponibles al final del día: {libros_disponibles}")
    print(f"Total de préstamos realizados: {usuarios_prestamos}")