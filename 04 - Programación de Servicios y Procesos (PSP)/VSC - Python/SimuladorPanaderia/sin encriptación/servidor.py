# Imports base
import threading
import socket
import queue
from estado_pedido import EstadoPedido
from producto import Producto
from horno import Horno
from pedido import Pedido
from estado_horno import EstadoHorno

# Imports encriptación
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES

class Servidor:
    HOST = "127.0.0.1"
    PORT = 5000

    # Constructor
    def __init__(self):
        """
        Inicializa el servidor.
        """
        self.configuracion_inicial()
        self.hornos = [Horno(self.max_ciclos_horno, self.registrar_estadisticas) for _ in range(self.num_hornos)] # Lista de hornos
        self.pedidos_espera = queue.Queue() if self.algoritmo == "FIFO" else queue.PriorityQueue() # Cola de pedidos en espera
        self.pedidos_totales = [] # Lista con todos los pedidos (permite actualizar el estado de los pedidos)
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.HOST, self.PORT))
        self.socket_servidor.listen(20)
        print(f"Servidor iniciado en {self.HOST}:{self.PORT}")

        self.productos_disponibles: list[Producto] = self.configurar_productos() # Lista de productos disponibles
        
        self.clientes_por_pedido = {} # Diccionario para almacenar los clientes asociados a cada pedido
        
        self.servidor_activo = True

        # Inicia los hornos
        for horno in self.hornos:
            horno.start()
        print(f"Hay {self.num_hornos} hornos disponibles con un máximo de {self.max_ciclos_horno} ciclos antes del mantenimiento y un algoritmo de planificación {self.algoritmo} seleccionado.")
    """
    Funciones de encriptación
    """
    # Función para generar las claves RSA
    def generar_claves_rsa(self):
        """
        Genera las claves RSA (asimétrica).
        """
        key = RSA.generate(2048)
        self.private_key = key
        self.public_key = key.publickey()
        self.private_cipher = PKCS1_OAEP.new(self.private_key)
    
    # Función para enviar la clave pública al cliente
    def enviar_clave_publica(self, cliente_socket: socket.socket):
        """
        Envía la clave pública al cliente.
        :param cliente_socket: Socket del cliente
        """
        cliente_socket.send(self.public_key.export_key())

    # Función para recibir la clave simétrica cifrada por la clave pública del servidor
    def recibir_clave_simetrica(self, cliente_socket: socket.socket):
        """
        Recibe la clave simétrica cifrada por la clave pública del servidor.
        :param cliente_socket: Socket del cliente
        """
        clave_aes_cifrada_b64 = cliente_socket.recv(2048)  # Aumentar el tamaño del buffer
        clave_aes_cifrada = base64.b64decode(clave_aes_cifrada_b64)
        self.aes_key = self.private_cipher.decrypt(clave_aes_cifrada)

    # Función para cifrar un mensaje con la clave simétrica AES
    def aes_encrypt(self, mensaje: str):
        """
        Cifra un mensaje con AES.
        :param mensaje: Mensaje a cifrar
        :return: Mensaje cifrado
        """
        cipher = AES.new(self.aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(mensaje.encode())
        nonce = cipher.nonce
        return base64.b64encode(nonce + tag + ciphertext).decode()

    # Función para desencriptar mensajes con la clave simétrica AES
    def aes_decrypt(self, mensaje_cifrado):
        """
        Descifra un mensaje con AES.
        """
        mensaje_bytes = base64.b64decode(mensaje_cifrado)
        
        nonce = mensaje_bytes[:16]
        tag = mensaje_bytes[16:32]
        ciphertext = mensaje_bytes[32:]

        cipher_aes = AES.new(self.aes_key, AES.MODE_EAX, nonce=nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag).decode()
        return data

    """
    Funciones del servidor
    """
    # Función para configurar los productos disponibles
    def configurar_productos(self):
        """
        Retorna una lista con los productos disponibles.
        """
        # Para no sobrecargar la configuración inical del servidor, se omite la selección de productos y se asignan valores fijos
        return [
            Producto("Croissant", 1, 1),
            Producto("Pan", 2, 3),
            Producto("Pastel", 3, 5)
        ]

    # Función para configurar los parámetros iniciales del servidor
    def configuracion_inicial(self):
        """
        Configura los parámetros iniciales del servidor.
        """
        # Bucle general para solicitar los parámetros iniciales
        while True:

            # Bucle: Solicita al usuario el número de hornos
            while True:
                try:
                    self.num_hornos = int(input("Ingrese el número de hornos: "))
                    if self.num_hornos > 0:
                        break
                    print("Error: Debe haber al menos un horno.")
                except ValueError:
                    print("Error: Entrada inválida. Asegúrese de ingresar un número entero.")
            
            # Bucle: Solicita al usuario el número de ciclos antes del mantenimiento
            while True:
                try:
                    self.max_ciclos_horno = int(input("Ingrese el máximo de ciclos por horno antes del mantenimiento: "))
                    if self.max_ciclos_horno > 0:
                        break
                    print("Error: El número de ciclos debe ser mayor a 0.")
                except ValueError:
                    print("Error: Entrada inválida. Asegúrese de ingresar un número entero.")
            
            # Bucle: Solicita al usuario el algoritmo de planificación
            while True:
                try:
                    self.algoritmo = input("Seleccione el algoritmo de planificación (FIFO/SJF): ").strip().upper()
                    if self.algoritmo in ["FIFO", "SJF"]:
                        break
                    print("Opción inválida. Por favor, elija entre FIFO o SJF.")
                except ValueError:
                    print("Error: Entrada inválida. Asegúrese de ingresar valores numéricos correctos.")
            break # Sale del bucle general si se ingresan valores válidos

    # Función para aceptar conexiones de clientes (el Servidor escucha)
    def aceptar_conexiones(self):
        """
        Acepta conexiones de clientes y crea un hilo para manejar cada cliente.
        """
        count = 0
        while self.servidor_activo:
            try:
                cliente_socket, _ = self.socket_servidor.accept() # El hilo principal se bloquea aquí esperando conexiones
                count += 1
                threading.Thread(target=self.manejar_cliente, args=(cliente_socket,), name=f"Thread {count}").start()
            except KeyboardInterrupt:
                self.cerrar_servidor()
                break
            except Exception as e:
                print(f"Error al aceptar la conexión: {e}")

    # Función para manejar un cliente
    def manejar_cliente(self, cliente_socket: socket.socket):
        """
        Maneja un cliente.
        :param cliente_socket: Socket del cliente
        """
        # En primer lugar, el servidor genera las claves RSA
        self.generar_claves_rsa()
        # Luego, envía la clave pública al cliente
        self.enviar_clave_publica(cliente_socket)
        # Por último, recibe la clave simétrica cifrada por la clave pública del servidor
        self.recibir_clave_simetrica(cliente_socket)

        try:
            self.nombre_cliente = cliente_socket.recv(1024).decode() # lo primero que recibimos es el nombre del cliente
            # Enviar lista de productos disponibles al cliente (con el formato que éste entiende para poder crear objetos Producto)
            productos = {producto.to_csv() for producto in self.productos_disponibles}
            cliente_socket.send(f"{productos}".encode())

            # Recibe las peticiones del cliente
            while True:
                # Recibimos datos del cliente
                datos = cliente_socket.recv(1024).decode().strip()
                print(f"Recibido: {datos} de {self.nombre_cliente} en {cliente_socket.getpeername()}")
                
                if datos.upper().startswith("CONSULTAR "):
                    # Consultar estado de los pedidos
                    pedido_id = datos[10:] # Elimina el comando "CONSULTAR " y obtiene el ID del pedido
                    estado_pedido = self.obtener_estado_pedido(pedido_id)
                    cliente_socket.send(estado_pedido.encode())
                
                elif datos.upper().startswith("PEDIDO "):
                    pedido_info = datos[7:] # Elimina el comando "PEDIDO " y obtiene la información del pedido
                    # Procesa el pedido
                    # print(f"Pedido recibido: {pedido_info} de {cliente_socket.getpeername()}")
                    pedido: Pedido = self.procesar_pedido(pedido_info)
                    # print(f"Pedido procesado: {pedido}")

                    if pedido:
                        self.clientes_por_pedido[pedido.id_pedido] = cliente_socket # Asocia el cliente al pedido
                        posicion = self.encolar_pedido(pedido) # Encola el pedido y obtiene la posición en la cola de espera
                        cliente_socket.send(f"Pedido recibido y en cola en la posición {posicion}, duración esperada {pedido.tiempo_total} s".encode())
                    else:
                        cliente_socket.send("Error en el pedido".encode())
                
                elif datos.upper() == "SALIR":
                    # Cerramos la conexión
                    cliente_socket.send("Cerrando conexión...\n".encode())
                    break
                
                else:
                    cliente_socket.send("Comando no reconocido. Use 'PEDIDO + Pedido()', 'CONSULTAR' o 'SALIR'.\n".encode())
                # Finalmente asignamos los pedidos a los hornos disponibles
                self.asignar_pedidos()

        except Exception as e:
            print(f"Error al manejar el cliente {self.nombre_cliente} en {cliente_socket.getpeername()}: {e}")
        finally:
            cliente_socket.close()

    # Obtiene el estado de los pedidos de la lista total de pedidos (que se mantiene actualizada para facilitar la consulta)
    def obtener_estado_pedido(self, id_pedido: str):
        """
        Obtiene el estado de los pedidos.
        :return: Cadena con el estado de los pedidos.
        """
        estado_pedido = next((f"Pedido {pedido.id_pedido}: {pedido.estado.name}" for pedido in self.pedidos_totales if str(pedido.id_pedido) == id_pedido), "Pedido no encontrado")
        return estado_pedido
    
    # Procesa el pedido recibido del cliente (y lo convierte en un objeto Pedido)
    def procesar_pedido(self, datos: str):
        """
        Convierte los datos recibidos en un objeto Pedido.
        :param datos: Cadena con formato "tipo_producto,cantidad"
        :return: Objeto Pedido o None si hay un error.
        """
        try:
            id_pedido, prod_tipo, prod_tiempo, prod_peso, cantidad = datos.split(",")
            cantidad = int(cantidad)

            # Impide que se pidan productos que no están disponibles o cantidades negativas
            tipos_disponibles = [producto.tipo for producto in self.productos_disponibles]

            if prod_tipo in tipos_disponibles and cantidad >= 0: # Los pedidos con 0 productos también se realizan (aunque no se van a hacer)
                pedido = Pedido(int(id_pedido), Producto(prod_tipo, int(prod_tiempo), int(prod_peso)), int(cantidad))
                return pedido
        except (ValueError, KeyError):
            pass
        return None
    
    # Función para encolar un pedido en la cola de espera (además, lo añade a la lista de pedidos totales)
    def encolar_pedido(self, pedido: Pedido):
        """
        Encola un pedido en la cola de espera.
        :param pedido: Pedido a encolar
        :return: Posición en la cola de espera
        """
        
        # print(f"HILO SERVIDOR {threading.current_thread().name} entrando en sección crítica")
        # Una vez se encola el pedido, pasa a estar "PENDIENTE"
        pedido.estado = EstadoPedido.PENDIENTE
        # print(f"HILO SERVIDOR {threading.current_thread().name} Pedido {pedido.id_pedido} en estado {pedido.estado.name}")
        self.pedidos_totales.append(pedido) # Además de agregarlo a la cola de espera, se agrega a la lista de pedidos totales

        # Algoritmo FIFO
        if self.algoritmo == "FIFO":
            self.pedidos_espera.put(pedido)
            posicion: int = self.pedidos_espera.qsize() # Posición en la cola de espera (al ser el último, es igual al tamaño de la cola)
        
        # Algoritmo SJF
        else:
            self.pedidos_espera.put((pedido.tiempo_total, pedido)) # Prioriza los pedidos con menor tiempo de horneado
            posicion:int  = self.calcular_posicion(pedido)
        return posicion
    
    # Función para asignar pedidos a los hornos disponibles
    def asignar_pedidos(self):
        """
        Asigna pedidos a los hornos disponibles.
        """
        while not self.pedidos_espera.empty():
            for horno in self.hornos:
                if horno.estado == EstadoHorno.DISPONIBLE:
                    pedido: Pedido = self.pedidos_espera.get()[1] if self.algoritmo == "SJF" else self.pedidos_espera.get()
                    pedido.estado = EstadoPedido.EN_PROCESO

                    self.actualizar_pedido_total(pedido, pedido.estado) # Actualiza el estado del pedido en la lista de pedidos totales

                    horno.asignar_pedido(pedido)
                    break
    
    # Función auxiliar para actualizar el estado del pedido en la lista de pedidos totales
    def actualizar_pedido_total(self, pedido: Pedido, estado: EstadoPedido):
        """
        Actualiza el estado de un pedido en la lista de pedidos totales.
        """
        for pedido_total in self.pedidos_totales:
            if pedido_total.id_pedido == pedido.id_pedido:
                pedido_total.estado = estado
                break

    # Función de tipo callable que permite a los hornos avisar de que un pedido está listo para registrar sus estadísticas
    def registrar_estadisticas(self, id_horno: int, pedido: Pedido, tiempo_en_uso: float, productos_horneados: int):
        """
        Registra las estadísticas de un horno.
        :param id_horno: ID del horno
        :param pedido: Pedido completado
        :param tiempo_en_uso: Tiempo total en uso
        :param productos_horneados: Cantidad de productos horneados
        """
        print(f"Horno {id_horno} completó Pedido {pedido.id_pedido}. Tiempo: {tiempo_en_uso:.2f}s, Productos: {productos_horneados}")
        pedido.estado = EstadoPedido.LISTO
        self.actualizar_pedido_total(pedido, pedido.estado) # Actualiza el estado del pedido en la lista de pedidos totales

        # Notifica al cliente que su pedido está listo y termina
        self.notificar_cliente(pedido)
        self.cerrar_servidor()
    
    # Función que notifica al cliente que su pedido está listo
    def notificar_cliente(self, pedido: Pedido):
        """
        Notifica al cliente que su pedido está listo.
        """
        try:
            cliente_socket = self.clientes_por_pedido[pedido.id_pedido] # Obtiene el socket del cliente asociado al pedido
            cliente_socket.send(f"Pedido {pedido.id_pedido} listo".encode()) # Notifica al cliente que su pedido está listo
        except Exception as e:
            print(f"Error al notificar al cliente: {e}")
    
    # Función para cerrar el servidor
    def cerrar_servidor(self):
        """
        Cierra el servidor.
        """
        self.servidor_activo = False
        self.socket_servidor.close()
        print(f"Servidor cerrado para el cliente {self.nombre_cliente}")

    # Función auxiliar para calcular la posición de un pedido en la cola de espera (SJF)
    def calcular_posicion(self, pedido: Pedido):
        """
        Calcula la posición en la cola de espera de un pedido.
        """
        # Obtener la lista de pedidos ordenados por prioridad
        pedidos_ordenados = sorted(list(self.pedidos_espera.queue), key=lambda x: x[0])

        # Buscar la posición real del pedido
        posicion = next((i + 1 for i, (_, p) in enumerate(pedidos_ordenados) if p == pedido), -1)
        
        return posicion

if __name__ == "__main__":
    servidor = Servidor()
    servidor.aceptar_conexiones()
