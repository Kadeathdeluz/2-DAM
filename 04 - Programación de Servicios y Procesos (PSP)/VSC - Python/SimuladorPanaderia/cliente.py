import socket
import threading
import random
from producto import Producto

class ClientePanaderia(threading.Thread):
    HOST = 'localhost'
    PUERTO = 12345

    def __init__(self):
        super().__init__()
        self.host = self.HOST
        self.puerto = self.PUERTO
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        """Inicia el cliente."""
        self.conectar()
        
        # Simulación de un pedido
        productos_disponibles = [
            Producto("Pan", 5, 1),
            Producto("Croissant", 6, 2),
            Producto("Pastel", 10, 3)
        ]
        
        pedido = [(random.choice(productos_disponibles), random.randint(1, 5)) for _ in range(3)]
        self.enviar_pedido(pedido)
        
        self.cerrar_conexion()
    
    def conectar(self):
        """Conecta el cliente al servidor."""
        try:
            self.socket_cliente.connect((self.host, self.puerto))
            print(f"[CLIENTE] Conectado al servidor en {self.host}:{self.puerto}")
        except Exception as e:
            print(f"[ERROR CLIENTE] No se pudo conectar: {e}")

    def enviar_pedido(self, productos):
        """Envía un pedido con una lista de productos."""
        try:
            pedido_data = str([(producto, cantidad) for producto, cantidad in productos]) # NOTA: Cambiar el envío
            self.socket_cliente.send(pedido_data.encode())
            respuesta = self.socket_cliente.recv(1024).decode()
            print(f"[CLIENTE] Respuesta del servidor: {respuesta}")
        except Exception as e:
            print(f"[ERROR CLIENTE] No se pudo enviar el pedido: {e}")

    def cerrar_conexion(self):
        """Cierra la conexión con el servidor."""
        self.socket_cliente.close()
        print("[CLIENTE] Conexión cerrada.")

if __name__ == "__main__":
    cliente = ClientePanaderia()
    cliente.start()
