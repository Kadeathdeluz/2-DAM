import socket
import threading
import random
from pedido import Pedido
from producto import Producto

class ClientePanaderia(threading.Thread):
    # Constantes de conexión
    HOST = "127.0.0.1"
    PORT = 5000
    # Contador de ID autoincremental para asignar IDs únicos a los clientes
    _id_counter = 0

    def __init__(self):
        super().__init__()
        # Asigna un ID único al cliente y lo incrementa para el siguiente
        self.id_cliente = ClientePanaderia._id_counter
        ClientePanaderia._id_counter += 1

        self.pedidos = []  # Lista de pedidos realizados por el cliente
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        """Inicia el cliente."""
        # Intenta conectarse al servidor
        self.conectar()
        
        # Solicita los productos disponibles al servidor
        self.socket_cliente.send("Dime productos disponibles".encode())

        # Recibe la lista de productos disponibles del servidor
        productos_disponibles = eval(self.socket_cliente.recv(1024).decode())  # Recibe la lista de productos disponibles
        
        # Realiza un pedido de todos los productos disponibles en una cantidad aleatoria (0-10)
        productos = []

        # Realiza 3 pedidos con una cantidad aleatoria de productos de cada tipo
        for _ in range(3):
            # Por cada producto disponible, selecciona una cantidad aleatoria
            for producto in productos_disponibles:
                productos.append(producto, random.randint(0, 10))
            
            # Crea un pedido con los productos seleccionados (Producto, cantidad)
            self.realizar_pedido(Pedido(productos))
            productos = [] # Limpia la lista de productos para el siguiente pedido

        # Finalmente, cierra la conexión
        self.cerrar_conexion()
    
    def conectar(self):
        """Conecta el cliente al servidor."""
        try:
            self.socket_cliente.connect((self.HOST, self.PUERTO))
            print(f"[CLIENTE] Conectado al servidor en {self.HOST}:{self.PUERTO}")
        except Exception as e:
            print(f"[ERROR CLIENTE] No se pudo conectar: {e}")

    def realizar_pedido(self, pedido):
        """Envía un pedido con una lista de productos."""
        self.pedidos.append(pedido) # Agrega el pedido a la lista de pedidos del cliente
        try:
            pedido_data = str([(producto, cantidad) for producto, cantidad in pedido]) # NOTA: Cambiar el envío
            self.socket_cliente.send(pedido_data.encode()) # Envia el pedido al servidor
            respuesta = self.socket_cliente.recv(1024).decode() # Espera la respuesta del servidor
            print(f"[CLIENTE] Respuesta del servidor: {respuesta}")
        except Exception as e:
            print(f"[ERROR CLIENTE] No se pudo enviar el pedido: {e}")

    def consultar_estado_pedido(self, id_pedido):
        """Consulta el estado de un pedido."""
        self.socket_cliente.send(f"Estado pedido {id_pedido}".encode())
        respuesta = self.socket_cliente.recv(1024).decode()
        print(f"[CLIENTE] Respuesta del servidor: {respuesta}")
    
    def cerrar_conexion(self):
        """Cierra la conexión con el servidor."""
        self.socket_cliente.close()
        print("[CLIENTE] Conexión cerrada.")

def opciones_cliente(clientes):
    """Muestra las opciones disponibles para el cliente."""
    ids = ""
    # Muestra los IDs de los clientes disponibles
    for cliente in clientes:
        ids += "ID:" + str(cliente.id_cliente) + "\n"
    print(f"Clientes disponibles: {ids}")
    
    while True:
        try:
            # Solicita al usuario seleccionar un cliente
            id_cliente = int(input("Seleccione un cliente (ID):"))
            print("Opciones disponibles:")
            print("1. Consultar estado de pedidos")
            print("2. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                # Consultar el estado de los pedidos
                cliente = next(cliente for cliente in clientes if cliente.id_cliente == id_cliente) # Obtiene el cliente seleccionado
                for pedido in cliente.pedidos:
                    id_pedido = pedido.id_pedido
                    cliente.consultar_estado_pedido(id_pedido)
                break
            elif opcion == "2":
                # Simplemente sale
                print("Saliendo...")
                break
            else:
                print("Opción inválida. Intente de nuevo.")
        except ValueError:
            print("ID de cliente inválido. Intente de nuevo.")
        except StopIteration:
            print("Cliente no encontrado. Intente de nuevo.")
        except Exception as e:
            print(f"[ERROR] {e}")

# Simulación de 5 clientes
if __name__ == "__main__":

    clientes = []

    # Crea 5 clientes de ejemplo y los inicia
    for _ in range(5):
        cliente = ClientePanaderia()
        cliente.start()
        clientes.append(cliente)
    
    opciones_cliente(clientes)
    while True:
        try:
            id_consulta = input("Seleccione un id de cliente para consultar el estado de sus pedidos: ")
        except Exception as e:
            print(f"[ERROR CLIENTE] {e}")
        finally:
            pass #Seguir aquí