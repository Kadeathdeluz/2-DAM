import threading
import random
import time

"""
VARIABLES
"""
class Generador():
    pass

class Entrega():
    pass

# Main:
if __name__ == "__main__":
    # Tiempo inicial
    ini_time = time.time()
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    time.sleep(4)

    # Mostrar los resultados finales
    print("\n-------------------------- RESULTADOS --------------------------\n")
    # Tiempo final
    fin_time = time.time()
    # Tiempo total que dura la ejecución
    
    total_time = fin_time - ini_time
    print(f"La ejecución ha durado un total de {total_time} segundos.")