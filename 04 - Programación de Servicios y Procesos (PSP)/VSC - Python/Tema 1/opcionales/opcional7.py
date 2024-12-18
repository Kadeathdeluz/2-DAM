import threading
import random

# Las variables representan a los candidatos A y B, y se incrementan con cada voto
candidateA = 0
candidateB = 0

# Función que define cómo se realiza la votación (sección crítica)
# Recibe como parámetros el número de la iteración (el hilo) y el lock global
def vote(iteration, lock):
    global candidateA, candidateB

    # Pasamos a proteger la sección crítica con el bloque try-except-finally y el lock
    # Primero adquirimos el lock
    lock.acquire()
    try:
        # Determinamos a quién vota cada hilo en función de si el random devuelve True o False (como únicamente hay dos posibilidades, no tiene sentido otro tipo de random)
        if random.choice([True, False]):
            candidateA += 1
            print("Soy el votante", iteration, "y he votado a A")
        else:
            candidateB += 1
            print("Soy el votante", iteration, "y he votado a B")
    except:
        print("Algo ha ido mal y el votante", iteration, "no ha podido votar.")
    
    #Finalmente, al terminar el try liberamos el lock
    finally: lock.release()

# Main: Se crean 10 hilos que "votan" al candidato A o B de manera aleatoria
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    # Creamos el lock pertinente para la sección crítica
    lock = threading.Lock()
    # Lista de hilos
    threads_list = []

    # Crea 10 hilos y cada uno llama a la función vote() pasando el número de iteración y el lock global como argumento
    for i in range (1,11):
        new_thread = threading.Thread(target=vote, args=(i,lock))
        threads_list.append(new_thread)
        new_thread.start()

    # Cada hilo espera a que los demás terminen
    for thread in threads_list:
        thread.join()

    # Mostrar los resultados finales
    print("\n-------------------------- RESULTADOS --------------------------\n")
    print(" ------ Las votaciones han quedado de la siguiente manera ------ ")
    print("Total de votantes:", candidateA+candidateB)
    print("Votos para el candidato A:", candidateA)
    print("Votos para el candidato B:", candidateB)