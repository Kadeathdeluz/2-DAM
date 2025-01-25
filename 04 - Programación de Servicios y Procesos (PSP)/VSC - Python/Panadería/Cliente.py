import socket
import threading
import random
import time

# Clase para simular clientes de la panadería
class ClientePanaderia(threading.Thread):
    def __init__(self, host="localhost", puerto=12345):
        self.host = host
        self.puerto = puerto
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def conectar(self):
        try:
            self.socket_cliente.connect((self.host, self.puerto))
            print(f"Conectado al servidor en {self.host}:{self.puerto}")
        except Exception as e:
            print(f"Error al conectar con el servidor: {e}")

    def enviar_pedido(self, id_pedido, tipo_producto, cantidad, tiempo_horneado):
        try:
            mensaje = f"{id_pedido},{tipo_producto},{cantidad},{tiempo_horneado}"
            self.socket_cliente.send(mensaje.encode())
            respuesta = self.socket_cliente.recv(1024).decode()
            print(f"Respuesta del servidor: {respuesta}")
        except Exception as e:
            print(f"Error al enviar el pedido: {e}")

    def cerrar_conexion(self):
        self.socket_cliente.close()
        print("Conexión cerrada.")

# Función para simular múltiples clientes
def simular_clientes():
    tipos_productos = ["Pan", "Pastel", "Croissant"]
    tiempos_horneado = {"Pan": 5, "Pastel": 8, "Croissant": 6}  # Tiempos en segundos

    clientes = []

    # Crear y conectar 3 clientes
    for i in range(3):
        cliente = ClientePanaderia()
        cliente.conectar()
        clientes.append(cliente)

    # Simular pedidos desde cada cliente
    for i in range(10):  # 10 pedidos aleatorios
        cliente = random.choice(clientes)
        tipo_producto = random.choice(tipos_productos)
        cantidad = random.randint(1, 5)
        tiempo_horneado = tiempos_horneado[tipo_producto]

        print(f"Cliente enviando pedido: Producto={tipo_producto}, Cantidad={cantidad}")
        cliente.enviar_pedido(id_pedido=i + 1, tipo_producto=tipo_producto, cantidad=cantidad, tiempo_horneado=tiempo_horneado)

        time.sleep(random.uniform(0.5, 2))  # Esperar entre pedidos

    # Cerrar conexiones
    for cliente in clientes:
        cliente.cerrar_conexion()

if __name__ == "__main__":
    simular_clientes()