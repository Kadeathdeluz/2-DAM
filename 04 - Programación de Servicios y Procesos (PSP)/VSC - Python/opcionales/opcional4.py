import threading
import time

# Método que
def tarea_animal(nombre, patas, vuela):
    vuelo = "vuela" if vuela else "no vuela"
    informacion = f"{nombre} es un animal con {patas} patas y {vuelo}."
    print(informacion)

#Desarrollar el método principal para ejecutar la tarea anterior con un hilo para cada animal,
# se deben crear, iniciar y esperar a que terminen todos los hilos.
# Se deben utilizar bucles y listas para solucionar el ejercicio.
# Main
if __name__ == "__main__":

    #Listas a utilizar
    animales = ["Perro","Pájaro","Araña"]
    patas = [4,2,8]
    vuela = [False,True,False]
    
    # Lista que contendrá los hilos
    hilos = []

    #Crea 3 hilos, los almacena en la lista y ejecuta la función en paralelo (3 veces, una por hilo)
    for i in range(3):
        nuevo_hilo = threading.Thread(target=hilo_hace, args=(i,phrase,))
        hilos.append(nuevo_hilo)
        nuevo_hilo.start()

