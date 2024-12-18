from pathlib import Path

def sumar(n1, n2):
    """Dados dos números, la función retorna la suma de todos los números comprendidos entre n1
    y n2"""
    resultado = 0
    for i in range(n1, n2 + 1):
        resultado += i
    return resultado

if __name__ == "__main__":
    resultado = 0
    
    #para abrir el fichero que se encuentra en el mismo path que el programa python
    fichero_path = Path(__file__).parent
    try:
        f1 = open(fichero_path/"solucion.txt","w")
        #La opción w crea el fichero, si no existe, y si existe sobrescrbe el contenido
    except OSError as e:
        print(f"Fichero1: ",e)
    else:
        try:
            f2 = open(fichero_path/"numeros.txt","r")
            #La opción r abre un ficer en formato sólo lectura
            for line in f2.readlines():
                n1, n2 = [int(x) for x in line.split(",")]
                resultado = sumar(n1,n2)
                print("La suma de los números entre", n1, "y", n2, "es:", resultado, file=f1)
        except OSError as e:
            print(f"Fichero2: ",e)