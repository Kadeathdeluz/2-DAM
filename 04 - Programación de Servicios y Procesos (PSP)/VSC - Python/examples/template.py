import threading
import random
import time

# Número de hilos a lanzar
num_threads = 15

# Clases y métodos: algunos ejemplos
class ThreadClassName(threading.Thread):
    def __init__(self, name, attribute):
        super().__init__(name= name)
        self.name = name
        self.attribute = attribute
    
    def run(self):
        print(f"Soy el hilo {self.name} y mi atributo es {self.attribute}")

class ClassName:
    pass

class SubClassName(ClassName):
    pass

def createThreads(num_threads: int):
    
    count = 1
    threads_list = []

    for _ in range(num_threads):
        new_thread = ThreadClassName(name= f"Hilo-{count}",attribute=random.choice(["red","blue","green","yellow","orange"]))
        threads_list.append(new_thread)
        new_thread.start()
        count+= 1
    

    return threads_list

# Main:
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    threads_list = createThreads(num_threads)

    for thread in threads_list:
        thread.join()

    # Mostrar los resultados finales
    print("\n-------------------------- RESULTADOS --------------------------\n")

    print(f"Se han creado {num_threads} hilos")