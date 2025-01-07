import socket
import threading

# Clase HiloServidor que hereda de threading.Thread que representa una instancia del Servidor (que se comunica con el Cliente)
class HiloServidor(threading.Thread):
    def __init__(self, socket_cliente, direccion_cliente):
        super().__init__()
        self.socket_cliente = socket_cliente
        self.direccion_cliente = direccion_cliente

    def run(self):
        # Cada hilo Servidor manejará a un hilo Cliente
        manejar_cliente(self)

# El servidor escucha a cada cliente en el socket que crea para cada hilo
def manejar_cliente(self):
    # Mensaje inicial cada vez que un cliente se conecta al Servidor
    print(f"Conexión establecida con {self.direccion_cliente}")
    try:
        contador = 0 # Contador para el número de mensajes
        while contador < 3:  # Bucle para recibir los 3 mensajes
            mensaje = self.socket_cliente.recv(1024).decode()
            if mensaje:  # Si hay mensaje
                contador += 1
                print(f"Mensaje recibido de {self.direccion_cliente}: {mensaje}")
                self.socket_cliente.sendall("OK".encode()) # Tras cada mensaje recibido, envía un OK
            else:
                break

        # Enviar la respuesta después de recibir los tres mensajes
        if contador == 3:
            self.socket_cliente.recv(1024).decode() # Recibe la confirmación de que se han enviado todos los mensajes
            self.socket_cliente.sendall(f"Comunicación correcta con el cliente {self.direccion_cliente},".encode())

    except Exception as e:
        print(f"Error con el cliente {self.direccion_cliente}: {e}")
    finally:
        print(f"Conexión cerrada con {self.direccion_cliente}")
        self.socket_cliente.close()

# Función principal para iniciar el servidor
if __name__ == "__main__":
    # Dirección: host y puerto
    HOST = "127.0.0.1"
    PORT = 4500

    try:
        # El Servidor crea el socket en el que escuchará (en dicho host y puerto)
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Vincula el socket a la dirección
        servidor.bind((HOST, PORT))
        # Recibe hasta 10 peticiones a la vez
        servidor.listen(10)
        print(f"Servidor escuchando en {HOST}:{PORT}")
    except Exception as e:
        # En caso de error, lanza un mensaje de error y termina
        print(f"Error iniciando el servidor: {e}")
        exit(1) # El servidor termina con mensaje de error

    try:
        while True:
            socket_cliente, direccion_cliente = servidor.accept() # El servidor queda bloqueado en esta línea esperando a que un cliente solicite conexión
            # Para cada nuevo cliente, creará un nuevo hilo Servidor en la nueva dirección
            hilo = HiloServidor(socket_cliente, direccion_cliente)
            hilo.start()
            # Para evitar que el servidor no termine, añadimos el control de excepciones que al recibir algo por teclado, cierre el servidor
    except Exception as e:
        print(f"Error en el Servidor: {e}")
    finally:
        # En cualquier caso, finalmente cierra el Servidor
        servidor.close()