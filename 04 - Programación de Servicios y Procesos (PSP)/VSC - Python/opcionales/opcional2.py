# Optional Exercise 2 by Roldán Sanchis Martínez
# Library to use Path class
from pathlib import Path

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


if __name__ == "__main__":
    # Total count of vowels in the current document
    line = 1
    
    # Path to workspace, first .parent goes to ".../opcional" and the second one goes to ".../VSC - Python"
    workSpacePath = Path(__file__).parent.parent
    # From there we try to access the file
    try:
        # phrasesFile contains the phrases (r to read the document)
        phrasesFile = open(workSpacePath/"resources/phrases.txt","r")
        # Call vowelCount(phrase) on every phrase like this:
        for phrase in phrasesFile.readlines():
            # vowelCount of the current phrase adds to totalCount
            totalCount = vowelCount(phrase)
            #@TODO: Sustituir por escritura en nuevo fichero
            print("Frase", line,":", totalCount, "vocales")
            line += 1
    except OSError as e:
        print(f"File: ",e)
# Los comentarios y variables están en inglés para practicar, pero los textos están en español por el usuario