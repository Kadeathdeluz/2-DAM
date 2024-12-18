import threading
import random

# Las variables representan a los candidatos A y B, y se incrementan con cada voto
candidateA = 0
candidateB = 0

# Clase que realiza los votos mediante su método run
class VotingThread():
    def __init__(self, lock):
        self.lock = lock
    
    # Se realiza la votación (sección crítica) dentro del run del hilo
    def run(self, iteration):
        global candidateA, candidateB

        # Pasamos a proteger la sección crítica con with lock
        with self.lock:
            # Manejo de excepciones dentro del bloque with
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




# Main: Se crean 10 hilos que "votan" al candidato A o B de manera aleatoria
if __name__ == "__main__":
    print("\n-------------------------- EJECUCIÓN --------------------------\n")
    # Creamos el lock pertinente para la sección crítica
    lock = threading.Lock()
    # Lista de hilos
    threads_list = []

    # Crea 10 hilos y cada uno vota dentro de su run(), pasando el número de iteración como argumento, el lock se pasa como argumento de __init__ al crearlo
    for i in range (1,11):
        votant = VotingThread(lock)
        new_thread = threading.Thread(target=votant.run, args=(i,))
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