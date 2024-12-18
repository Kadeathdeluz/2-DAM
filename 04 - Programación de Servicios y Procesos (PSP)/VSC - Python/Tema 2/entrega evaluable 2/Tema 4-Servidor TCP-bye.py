import socket
import sys
import threading

# Método que ejecutará cada hilo creado por el servidor para comunicarse con cada cliente
def manejar_cliente(socket_cliente, addr_cliente):
    fin_mensaje = ''
    print(f"Conexión exitosa con el cliente. {addr_cliente}")

    # Bloque try-except para tratamiento de excepciones
    try:
        # Bloque with para liberar automáticamente el socket (incluso en caso de error)
        with socket_cliente:  # El socket se cerrará automáticamente al salir del bloque
            cerrar = False
            while not cerrar:
                data = socket_cliente.recv(1024)  # El servidor queda bloqueado esperando datos del cliente
                if data.decode() == fin_mensaje:  # Si el mensaje está vacío, cerramos la comunicación
                    cerrar = True
                else:
                    print(f'El cliente {addr_cliente} nos ha escrito: {data.decode()}')  # Imprimimos el mensaje
                    socket_cliente.sendall(b"Mensaje recibido")  # Enviamos confirmación al cliente
    except Exception as e:
        print(f"Error con el cliente {addr_cliente}: <<{e}>>")
    print(f"Fin de conversación con: {addr_cliente}")


# Main: el servidor realiza sus acciones: crea el socket, vincula el socket al host y puerto especificados y comienza a escuchar.
if __name__ == '__main__':

    #Decidimos la IP y el puerto del servidor
    HOST = '127.0.0.1'  # La IP del servidor es la loca de la máquina
    PORT = 5000        # El puerto tiene que ser superior a 1024, por debajo estan reservados

    # Bloque try-except para tratamiento de excepciones
    try:
        # El servidor crea el socket (TCP) en el que escucha peticiones de clientes
        socket_escucha = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket servidor creado')
    except socket.error:
        # En caso de error, printea un mensaje y cierra el programa
        print('Fallo en la creación del socket servidor')
        sys.exit()

    # Bloque try-except para tratamiento de excepciones
    try:
        # Vincula el socket al host y el puerto especificados
        socket_escucha.bind((HOST, PORT)) # Definimosel punto de enlace del servidor.
                                        # El servidor está preparado en la IP 127.0.0.1 y puerto 5000
    except socket.error as e:
        # En caso de error, printea el error y cierra el programa
        print('Error socket: %s' %e)
        sys.exit()
    
    socket_escucha.listen(5) # El servidor puede escuchar hasta 5 clientes
                            #(marca la cantidad de clientes en cola antes de rechazar la petición).
    print(f"El servidor está escuchando en {HOST}:{PORT}...")

    # Bloque try-except-finally para cerrar automáticamente el socket_escucha si se produce algún error
    try:
        # Bucle "infinito" de escucha del servidor
        while True :
            socket_atiende, addr_cliente = socket_escucha.accept() #El Servidor queda bloquedo en esta línea
                                                    # esperando a que un cliente se conecte a su IP y puerto
            # Si un cliente se conecta guardamos en socket_atiende el nuevo socket
            # y en addr_cliente la información del cliente (IP y puerto del cliente)
            print(f"Escuchando al cliente {addr_cliente}.")

            # Creamos un nuevo hilo del servidor para atender al nuevo cliente
            hilo_conversacion = threading.Thread(target=manejar_cliente, args=(socket_atiende,addr_cliente))
            hilo_conversacion.start()

    except Exception as e:
        print(f"\nError al atender a un cliente: <<{e}>>\n")
    finally:
        socket_escucha.close()
        print("Socket del servidor cerrado")