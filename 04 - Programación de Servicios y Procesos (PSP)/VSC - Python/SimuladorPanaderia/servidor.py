import socket
import threading
from horno import Horno, EstadoHorno
from pedido import Pedido
from producto import Producto
import time

class ServidorPanaderia:
    def __init__(self, num_hornos, max_ciclos, host='localhost', puerto=12345):
        self.host = host
        self.puerto = puerto
        self.hornos = [Horno(max_ciclos) for _ in range(num_hornos)]
        self.pedidos_pendientes = []  # Lista de pedidos en espera
        self.lock = threading.Lock()  # Control de concurrencia
        self.servidor_activo = False

    def iniciar_servidor(self):
        """
        Inicia el servidor y escucha conexiones entrantes.
        """
        self.servidor_activo = True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.puerto))
        server_socket.listen(5)
        print(f"[SERVIDOR] Servidor iniciado en {self.host}:{self.puerto}, esperando conexiones...")

        while self.servidor_activo:
            try:
                cliente_socket, direccion = server_socket.accept()
                print(f"[NUEVO CLIENTE] Conexión establecida desde {direccion}")
                threading.Thread(target=self.manejar_cliente, args=(cliente_socket,)).start()
            except Exception as e:
                print(f"[ERROR] Ocurrió un problema: {e}")
                break
        
        server_socket.close()
        print("[SERVIDOR] Servidor detenido.")

    def manejar_cliente(self, cliente_socket):
        """
        Maneja la comunicación con un cliente y recibe pedidos.
        """
        try:
            mensaje = cliente_socket.recv(1024).decode()
            
            productos = eval(mensaje)  # Convierte a lista de tuplas (Producto, cantidad)
            pedido = Pedido([(Producto(producto.nombre, producto.tiempo), cantidad) for producto, cantidad in productos]) # NOTA: cambiar la recepción del pedido
            
            print(f"[CLIENTE] Pedido recibido: {pedido}")
            self.asignar_pedido(pedido)
            cliente_socket.send(f"[SERVIDOR] Pedido {pedido.id_pedido} recibido".encode())
        except Exception as e:
            print(f"[ERROR CLIENTE] {e}")
        finally:
            cliente_socket.close()

    def asignar_pedido(self, pedido):
        """
        Intenta asignar un pedido a un horno disponible, si no hay, lo pone en espera.
        :param pedido: Pedido a asignar a un horno.
        """
        with self.lock:
            for horno in self.hornos:
                if horno.estado == EstadoHorno.OK:
                    if horno.asignar_pedido(pedido):
                        threading.Thread(target=horno.cocinar_pedido).start()
                        return
            self.pedidos_pendientes.append(pedido)
            print(f"[SERVIDOR] No hay hornos disponibles, pedido {pedido.id_pedido} en espera.")

    def gestionar_hornos(self):
        """
        Monitorea los hornos y asigna pedidos en espera cuando haya disponibilidad.
        Si un horno requiere mantenimiento, lo envía a mantenimiento.
        """
        while self.servidor_activo:
            with self.lock:
                for horno in self.hornos:
                    if horno.estado == EstadoHorno.MANT:
                        threading.Thread(target=horno.mantenimiento).start()
                    elif horno.estado == EstadoHorno.OK and self.pedidos_pendientes:
                        pedido = self.pedidos_pendientes.pop(0) # Tomar el primer pedido en espera
                        if horno.asignar_pedido(pedido):
                            threading.Thread(target=horno.cocinar_pedido).start()
            time.sleep(1)

    def detener_servidor(self):
        """Detiene el servidor y cierra todas las conexiones activas."""
        self.servidor_activo = False
        print("[SERVIDOR] Servidor detenido.")

def configuracion_inicial():
    """
    Configuración inicial del servidor.
    Solicita al usuario el número de hornos y el número máximo de ciclos de uso.
    """
    while True:
        try:
            num_hornos = int(input("Ingrese el número de hornos: "))
            max_ciclos = int(input("Ingrese el número máximo de ciclos de uso de los hornos: "))
            return num_hornos, max_ciclos
        except ValueError:
            print("Por favor, ingrese valores enteros válidos.")

if __name__ == "__main__":
    num_hornos, max_ciclos = configuracion_inicial() # Solicitar al usuario la configuración inicial
    servidor = ServidorPanaderia(num_hornos, max_ciclos) # Inicializa el servidor con los parámetros ingresados por el usuario
    threading.Thread(target=servidor.gestionar_hornos).start()
    servidor.iniciar_servidor()