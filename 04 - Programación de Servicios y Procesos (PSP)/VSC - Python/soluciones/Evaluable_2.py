'''
Autor: Alexandra Savu 2º DAM
Acabado: 20/10/2024

Evaluable 2:
    Crea un programa que simule el funcionamiento de una biblioteca
'''
#importamos las librerias necesarias para hacer funcionar nuestro programa
import threading
import random

#variables globales compartidas por todos los hilos
libros_disponibles = 10
usuarios_prestamo = 0
contador_prestamo = 1 
contador_devolucion = 1

#Lock para sincronizar correctamente las variables con todos los hilos
lock = threading.Lock()


#Clase base común a ser heredada por otras
class Biblioteca:
    #Constructor de la clase
    def __init__(self,nombre):
       self.nombre = nombre

       
#Clase que hereda de Biblioteca y maneja los prestamos de libros              
class ClientePrestamo(Biblioteca):
    #Constructor de la clase
    def __init__(self):  
        #Llamamos al nombre del objeto
        self.nombre = threading.current_thread().name 
        #Hacemos referencia al metodo de la misma clase      
        self.prestamo()
        
    #Metodo para gestionar el prestamo de un libro 
    def prestamo(self):
        #Llamamos a las variables globales para poder utilizarlas
        global libros_disponibles
        global usuarios_prestamo
        
        #Bloque try para manejar las excepciones y errores
        #También usamos el with junto con el lock para evitar problemas de concurrencia y manejar errores
        try:  
            with lock:
                #Usamos una condición para verificar si hay libros disponibles para prestar
                if libros_disponibles > 0:
                    libros_disponibles -=1
                    usuarios_prestamo +=1               
                    print(f"{ self.nombre}: Se ha prestado un libro")
                else:
                    #Si no hay libros disponibles salta un error                
                    print(f"{ self.nombre}:Error. No quedan libros disponibles para prestar")
        except Exception as e:
            #Manejamos los errores en caso de que se de
            print(f"Error al procesar el prestamo: {e}") 




#Clase para el manejo de las devoluciones que hereda de la clase Biblioteca        
class ClienteDevolucion(Biblioteca):
    #Constructor de la clase
    def __init__(self):
        self.nombre = threading.current_thread().name #Llamamos al nombre del objeto
        #Hacemos referencia al metodo de la misma clase  
        self.devolucion()      
    
    #Metodo para la devolución de libros (solo si hay libros prestados)   
    def devolucion(self):
        #Referencia a las variables globales
        global libros_disponibles
        global usuarios_prestamo
        
        #Bloque try para manejar las excepciones y errores
        #También usamos el with junto con el lock para evitar problemas de concurrencia y manejar errores
        try:
            with lock:
                #Condición de devolución. Solo se puede devolver si hay libros prestados
                if libros_disponibles < 10:
                    libros_disponibles+=1               
                    print(f"{self.nombre}: Se ha devuelto un libro")
                #Salta error si no hay libros prestados que se puedan devolver
                elif libros_disponibles == 10:    
                    print(f"{ self.nombre}: Error. No hay libros para devolver.")
        except Exception as e:
            print(f"Error al procesar la devolución {e}") #Salta error al manejar la devolución




#Hilo principal para la creación de hilos de devolucion y prestamo
if __name__ == "__main__":
    #Lista para manejar los hilos
    hilos = []
    
    #Creamos 15 hilos que representará un usuario prestando o devolviendo un libro
    for i in range (15):
        #Acción aleatoria: 1 prestamo, 2 devolución
        accion = random.choice([1,2])

        #Dependiendo del numero, tomamos una acción u otra
        if accion == 1:
            #Creamos un hilo que llamará a la clase de prestamos           
            hilo = threading.Thread(target = ClientePrestamo, name = "Hilo_tomar" + str(contador_prestamo))#Utilizamos el contador_prestamo para ponerle el nombre al hilo
            #Lo añadimos a la lista y lo iniciamos
            hilos.append(hilo)
            hilo.start()
            #Contador que nos ayudara a llevar cuenta de los prestamos y enumerarlos para luego utlizarlo para el nombre del hilo
            contador_prestamo +=1           
        elif accion == 2:
            #Creamos un hilo que llama a la clase de devoluciones
            hilo = threading.Thread(target = ClienteDevolucion, name = "Hilo_devolver" + str(contador_devolucion))#Utilizamos el contador_devoluciones para ponerle el nombre al hilo
            #Lo añadimos a la lista y lo iniciamos
            hilos.append(hilo)
            hilo.start()
            #Contador que nos ayudará a llevar cuenta de las devoluciones
            contador_devolucion += 1
               
    #Esperamos que todos los hilos terminen para mostrar el resultado final
    for hilo in hilos:
        hilo.join()
    
    #Mostramos el resultado final
    print(f"Libros disponibles: {libros_disponibles}\nPrestamos realizados: {usuarios_prestamo}")