# Optional Exercise 1 by Roldán Sanchis Martínez

# Counts the number of vowels contained in the given phrase
def vowelCount(phrase):
    # Vowel count
    count = 0
    # Use a for-each loop to count the vowels contained in the given phrase
    for word in phrase:
        # If the current word is a vowel increases the count by one
        if word in "aeiouAEIOU":
            count+=1
    return count

# Main
if __name__ == "__main__":
    print("Este programa cuenta el número de vocales (a/A, e/E, i/I, o/O, u/U) en una frase.")
    # Keyboard input
    phrase = str(input("Escribe una frase: "))
    vowels = vowelCount(phrase)
    print("El número de vocales en la frase es: ", vowels)

# Los comentarios y variables están en inglés para practicar, pero los textos están en español por el usuario