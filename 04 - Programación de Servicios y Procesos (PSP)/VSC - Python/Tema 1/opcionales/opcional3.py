import threading

# Función definida en el ejercicio opcional 1, cuenta las vocales de un frase dada.
def vowelCount(phrase):
    count = 0
    for word in phrase:
        if word in "aeiouAEIOU":
            count+=1
    return count

# Función que ejecutará cada hilo, como es la misma frase, todos los hilos devolverán el mismo resultado, pero distinto texto
def hilo_hace(id_hilo, phrase):
    vowels = vowelCount(phrase)
    nombre_hilo = "Hilo (" + str(id_hilo) + "):"
    print(nombre_hilo, "El número de vocales en la frase es: ", vowels)

# Main
if __name__ == "__main__":
    phrase = str(input("Escribe una frase: "))
    # Lista que contendrá los hilos
    hilos = []

    #Crea 3 hilos, los almacena en la lista y ejecuta la función en paralelo (3 veces, una por hilo)
    for i in range(3):
        nuevo_hilo = threading.Thread(target=hilo_hace, args=(i,phrase,))
        hilos.append(nuevo_hilo)
        nuevo_hilo.start()
