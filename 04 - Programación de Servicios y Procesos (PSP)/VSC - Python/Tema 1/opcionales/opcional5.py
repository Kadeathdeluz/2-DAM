import threading
import random

def dividir(argumento):
    resultado = argumento/2
    nombre_hilo = threading.current_thread().name
    mensaje = f"Soy el thread con nombre {nombre_hilo}. Mi identificador es: {threading.current_thread().ident} y el resultado del número dividido es: {resultado}."
    print(mensaje)

def multiplicar(argumento):
    resultado = argumento*2
    mensaje = f"Soy el thread con nombre {threading.current_thread().name}. Mi identificador es: {threading.current_thread().ident} y el resultado del número multiplicado es: {resultado}."
    print(mensaje)

if __name__ == "__main__":
    # Variable aleatoria que contiene un número entre 20 y 100
    argumento_aleatorio = random.randint(20,100)
    print("El número aleatorio es:",argumento_aleatorio)
    
    # Lista que contendrá los hilos
    lista_hilos = []

    # Nota: Es importante en la creación [target=funcion, args=(parámetro1, par2...)] porque de lo contrario es el MainThread el que ejecuta siempre la función
    # Si por ejemplo hacemos [target=funcion(parámetro1, par2...)] estamos llamando directamente a la función y es el MainThread el que la ejecuta

    # Crea 5 hilos (1, 2, 3, 4 y 5) que ejecutan el método dividir(), se les cambia el nombre TRAS crearlos
    for i in range(1,6):
        nuevo_hilo = threading.Thread(target=dividir, args=(argumento_aleatorio,))
        nuevo_hilo.name = "HiloDiv"+str(i)
        lista_hilos.append(nuevo_hilo)
        print(nuevo_hilo.name)
        nuevo_hilo.start()

    # Crea 5 hilos (6, 7, 8, 9 y 10) que ejecutan el método multiplicar(), se les cambia el nombre al crearlos
    for i in range(6,11):
        nuevo_hilo = threading.Thread(target=multiplicar, args=(argumento_aleatorio,), name="HiloMulti" + str(i))
        lista_hilos.append(nuevo_hilo)
        nuevo_hilo.start()
    
    # Cada hilo espera a que los demás terminen (menos llamadas que ejecutra el join justo después de iniciar el hilo)
    for hilo in lista_hilos:
        hilo.join()
