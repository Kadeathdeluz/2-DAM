import threading
import random
import time

# Clases y métodos: algunos ejemplos
class ThreadClassName(threading.Thread):
    pass

class ClassName:
    def __init__(self, attribute):
        super().__init__()
        self.attribute = attribute
    
    def run(self):
        print("Texto")

class SubClassName(ClassName):
    pass

# Main:
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")

    # Mostrar los resultados finales
    print("\n-------------------------- RESULTADOS --------------------------\n")