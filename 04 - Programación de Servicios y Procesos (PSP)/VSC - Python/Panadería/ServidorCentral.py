import socket
import threading
import queue
import time
from enum import Enum

''' Imports locales '''
import Pedido # Importar la clase Pedido del archivo Pedido.py
from enums import EstadoHorno # Importar la clase EstadoHorno de la carpeta enums
import Horno # Importar la clase Horno del archivo Horno.py

# Clase del servidor
class ServidorPanaderia:
    def __init__(self, host="localhost", puerto=12345, ciclos_maximos_horno=5):
        self.host = host
        self.puerto = puerto
        self.hornos = [Horno(i, ciclos_maximos_horno) for i in range(3)]  # 3 hornos
        self.cola_pedidos = queue.PriorityQueue()  # Para organizar por tiempos
        self.clientes = []
        self.lock = threading.Lock()

    # Crea el socket, lo enlaza al host y puerto, y se pone a escuchar en dicho socket
    def iniciar_servidor(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.puerto))
        server_socket.listen(5)
        print(f"Servidor iniciado en {self.host}:{self.puerto}")

        while True:
            cliente_socket, direccion = server_socket.accept()
            print(f"Cliente conectado desde {direccion}")
            self.clientes.append(cliente_socket)
            threading.Thread(target=self.manejar_cliente, args=(cliente_socket,)).start()

    def manejar_cliente(self, cliente_socket):
        while True:
            try:
                datos = cliente_socket.recv(1024).decode()
                if not datos:
                    break

                print(f"Pedido recibido: {datos}")
                id_pedido, tipo_producto, cantidad, tiempo_horneado = datos.split(",")
                pedido = Pedido(
                    id_pedido=int(id_pedido),
                    tipo_producto=tipo_producto,
                    cantidad=int(cantidad),
                    tiempo_horneado=int(tiempo_horneado),
                )

                self.agregar_pedido(pedido)
                cliente_socket.send("Pedido recibido y en cola".encode())
            except Exception as e:
                print(f"Error manejando cliente: {e}")
                break

        cliente_socket.close()

    def agregar_pedido(self, pedido):
        self.lock.acquire()
        try:
            self.cola_pedidos.put((pedido.tiempo_total, pedido))
            print(f"Pedido {pedido.id_pedido} agregado a la cola")
        finally:
            self.lock.release()

    def procesar_pedidos(self):
        while True:
            if not self.cola_pedidos.empty():
                _, pedido = self.cola_pedidos.get()

                horno_disponible = None
                for horno in self.hornos:
                    if horno.estado == EstadoHorno.OK:
                        horno_disponible = horno
                        break

                if horno_disponible:
                    print(f"Procesando pedido {pedido.id_pedido} en horno {horno_disponible.id_horno}")
                    horno_disponible.asignar_pedido()

                    time.sleep(pedido.tiempo_total)  # Simular tiempo de horneado

                    horno_disponible.liberar_horno()
                    print(f"Pedido {pedido.id_pedido} completado en horno {horno_disponible.id_horno}")
                else:
                    print("No hay hornos disponibles, esperando...")
                    time.sleep(1)

    def iniciar_procesamiento(self):
        threading.Thread(target=self.procesar_pedidos).start()


# === Funciones de configuración ===

# Función para la configuración inicial del servidor: define los tiempos de horneado de los productos, cantidad de hornos y tiempo máximo de ciclos
def configuracion_inicial():
    PRODUCTOS = definir_tiempos_horneado()
    CANTIDAD_HORNOS = definir_cantidad_hornos()
    CICLOS_MAXIMOS = definir_ciclos_maximos()
    return {PRODUCTOS, CANTIDAD_HORNOS, CICLOS_MAXIMOS}

# Función para definir los tiempos de horneado de los productos mediante teclado, devuelve un Enum con los productos y los tiempos de horneado
def definir_tiempos_horneado():
    print("=== A continuación se le solicitan los tiempos de horneado ===")
    while True:
        try:
            tiempo_pan = int(input("Ingrese el tiempo de horneado para 'Pan': ").strip())
            tiempo_croissant = int(input("Ingrese el tiempo de horneado para 'Croissant': ").strip())
            tiempo_pastel = int(input("Ingrese el tiempo de horneado para 'Pastel': ").strip())
            break
        except ValueError:
            print("Error: Todos los tiempos deben ser números enteros. Inténtelo de nuevo.\n")

    return Enum('Producto', [
        ('PAN', tiempo_pan),
        ('CROISSANT', tiempo_croissant),
        ('PASTEL', tiempo_pastel)
    ])

# Función para definir la cantidad de hornos mediante teclado, devuelve un entero con la cantidad de hornos
def definir_cantidad_hornos():
    print("=== A continuación se le solicita la cantidad de hornos ===")
    while True:
        try:
            cantidad_hornos = int(input("Ingrese la cantidad de hornos: ").strip())
            break
        except ValueError:
            print("Error: La cantidad de hornos debe ser un número entero. Inténtelo de nuevo.\n")

    return cantidad_hornos

# Función para definir el tiempo máximo de ciclos mediante teclado, devuelve un entero con el tiempo máximo de ciclos
def definir_ciclos_maximos():
    print("=== A continuación se le solicita el tiempo máximo de ciclos ===")
    while True:
        try:
            ciclos_maximos = int(input("Ingrese el tiempo máximo de ciclos: ").strip())
            break
        except ValueError:
            print("Error: El tiempo máximo de ciclos debe ser un número entero. Inténtelo de nuevo.\n")

    return ciclos_maximos

# Iniciar el servidor
if __name__ == "__main__":
    # Configuración inicial: tiempos de horneado, cantidad de hornos y ciclos máximos
    PRODUCTOS,CANTIDAD_HORNOS, CICLOS_MAXIMOS = configuracion_inicial()
    
    servidor = ServidorPanaderia()
    threading.Thread(target=servidor.iniciar_procesamiento).start()
    servidor.iniciar_servidor()