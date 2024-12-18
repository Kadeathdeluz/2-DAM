import threading

# Método que
def tarea_animal(nombre, patas, vuela):
    vuelo = "vuela" if vuela else "no vuela"
    informacion = f"{nombre} es un animal con {patas} patas y {vuelo}."
    print(informacion)

# Main: se crean 3 hilos, se inician, ejecutan el método tarea_animal y esperan a que todos terminen
if __name__ == "__main__":

    #Listas a utilizar
    animales = ["Perro","Pájaro","Araña"]
    patas = [4,2,8]
    vuela = [False,True,False]
    
    # Lista que contendrá los hilos
    hilos = []

    #Crea 3 hilos (animales con su nombre) y ejecuta el método tarea_animal() para cada uno
    for i in range(3):
        nuevo_animal = threading.Thread(target=tarea_animal(animales[i],patas[i], vuela[i]))
        nuevo_animal.name = animales[i]
        hilos.append(nuevo_animal)
        nuevo_animal.start()
        nuevo_animal.join()

