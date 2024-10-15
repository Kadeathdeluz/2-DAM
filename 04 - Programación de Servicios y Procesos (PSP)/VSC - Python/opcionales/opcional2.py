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
    # Now we try to access the file
    try:
        # fileToRead contains the phrases ("r" to read the document)
        fileToRead = open(workSpacePath/"resources/phrases.txt","r")
        # fileToWrite contains the vowelCount of every phrase ("w" to write the document)
        fileToWrite = open(workSpacePath/"resources/vowelsCount.txt","w")
        # fileToWrite = open(workSpacePath/"resources/vowelsCount.txt","a") #this can be used as an optional solution (using append mode "a")

        # Call vowelCount(phrase) on every phrase like this:
        for phrase in fileToRead.readlines():
            # vowelCount of the current phrase
            currentCount = vowelCount(phrase)
            # Text that contains the number of vowels in a phrase like "Frase X: Y vocales" where X is the line number and Y is the vowelCount
            text = "Frase " + str(line) + ": " + str(currentCount)
            fileToWrite.write(text)
            fileToWrite.write("\n")
            line += 1
        print("Documento creado/modificado correctamente.")

    except OSError as e:
        print(f"File: ",e)

    finally:
        # Finally closes the files
        fileToRead.close()
        fileToWrite.close()
# Los comentarios y variables están en inglés para practicar, pero los textos están en español por el usuario