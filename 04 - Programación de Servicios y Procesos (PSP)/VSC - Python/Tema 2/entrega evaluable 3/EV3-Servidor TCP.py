import socket
import sys
import threading

# Método que ejecutará cada hilo creado por el servidor para comunicarse con cada cliente
def manejar_cliente(socket_cliente, addr_cliente):
    # Tras 3 mensajes el servidor cierra la conexión
    count_final = 3
    print(f"Conexión exitosa con el cliente. {addr_cliente}")

    # Bloque try-except para tratamiento de excepciones
    try:
        # Bloque with para liberar automáticamente el socket (incluso en caso de error)
        with socket_cliente:  # El socket se cerrará automáticamente al salir del bloque
            while count_final > 0:
                data = socket_cliente.recv(1024)  # El servidor queda bloqueado esperando datos del cliente
                print(f'El cliente {addr_cliente} nos ha escrito: {data.decode()}')  # Imprimimos el mensaje
                socket_cliente.sendall(b"Mensaje recibido")  # Enviamos confirmación al cliente
                count_final -= 1
            
            # Finalmente, enviamos el mensaje de comunicación correcta
            mensaje = f"Comunicación correcta con el cliente {addr_cliente}."
            socket_cliente.sendall(mensaje.encode()) # Hace falta codificar el mensaje

    except Exception as e:
        print(f"Error con el cliente {addr_cliente}: <<{e}>>")
    print(f"Fin de conversación con: {addr_cliente}")

# Clase Servidor que hereda de threading.Thread
class HiloServidor(threading.Thread):
    # Recibe el socket del cliente y la dirección como atributos (el hilo se crea únicamente para ese cliente)
    def __init__(self,socket_cliente, addr_cliente):
        super().__init__()
        self.socket_cliente = socket_cliente
        self.addr_cliente = addr_cliente
    # Cada hilo maneja un cliente
    def run(self):
        manejar_cliente(self.socket_cliente, self.addr_cliente)

# Main: el servidor realiza sus acciones: crea el socket, vincula el socket al host y puerto especificados y comienza a escuchar.
if __name__ == '__main__':

    #Decidimos la IP y el puerto del servidor
    HOST = '127.0.0.1'  # La IP del servidor es localhost
    PORT = 4500        # El puerto tiene que ser superior a 1024, por debajo estan reservados

    # Bloque try-except para tratamiento de excepciones
    try:
        # El servidor crea el socket (TCP) en el que escucha peticiones de clientes
        socket_escucha = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket servidor creado')
    except socket.error:
        # En caso de error, imprime un mensaje y cierra el programa
        print('Fallo en la creación del socket servidor')
        sys.exit()

    # Bloque try-except para tratamiento de excepciones
    try:
        # Vincula el socket al host y el puerto especificados
        socket_escucha.bind((HOST, PORT)) # Definimos el punto de enlace del servidor.
                                        # El servidor está preparado en la IP 127.0.0.1 y puerto 4500
    except socket.error as e:
        # En caso de error, imprime el error y cierra el programa
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
            print(f"Iniciando conversación con el cliente {addr_cliente}...")

            # Creamos un nuevo hilo del servidor para atender al nuevo cliente
            hilo_conversacion = HiloServidor(socket_atiende,addr_cliente)
            hilo_conversacion.start()

    except Exception as e:
        print(f"\nError al atender a un cliente: <<{e}>>\n")
    finally:
        socket_escucha.close()
        print("Socket del servidor cerrado")