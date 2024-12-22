import socket
import sys

# Host y puerto del servidor
HOST = '127.0.0.1'
PORT = 4500

# Clase Cliente que hereda de threading.Thread
class HiloCliente():
    pass
    def __init__():
        pass
    def run(self):
        pass

# Acciones que realiza el cliente: Crea el socket e intenta conectarse con dicho host y puerto
def programa_cliente():

    # Bloque try-except para tratamiento de excepciones
    try:
        # El cliente crea el socket de tipo TCP (SOCK_STREAM)
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM -> TCP
        print('Socket cliente creado')
    except socket.error:
        # En caso de error, printea un mensaje y cierra el programa
        print('Fallo en la creación del socket ciente')
        sys.exit()
    
    # El cliente intenta conectarse al socket creado en la dirección especificada
    socket_cliente.connect((HOST, PORT))
        
    mensaje = 'Conectado con el servidor' # El programa cliente nos pide que escribamos algo

    # Bloque with para asegurar que en caso de error, se libere el socket creado (y para evitar cerrarlo manualmente)
    with socket_cliente:
        while mensaje != 'bye' and mensaje != '':
            socket_cliente.sendall(mensaje.encode()) #Codificamos el mensaje a bytes y le indicamos que lo envie todo
            #numBytes = s.sendall(mensaje.encode())
            #print (numBytes)
            data = socket_cliente.recv(1024) #línea bloqueante, esperamos que el servidor nos conteste
            print('Recibido del servidor:' + data.decode())
            mensaje = input('Escribe tu mensaje (Para finalizar escribe: bye)--> ')
        socket_cliente.close()


if __name__ == '__main__':
    programa_cliente()