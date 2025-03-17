# Imports base
import threading
import socket
import random

# Imports de módulos de encriptación
import base64
import uuid
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes

from producto import Producto
from pedido import Pedido

class ClientePanaderia(threading.Thread):
    HOST = "127.0.0.1"
    PORT = 5000
    _id_counter = 0  # Contador para asignar un ID único a cada cliente

    def __init__(self):
        super().__init__()
        ClientePanaderia._id_counter += 1
        self.id_cliente = uuid.uuid4().int  # ID único para el client
        self.name = f"Cliente {self.id_cliente}"
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pedidos_realizados = []  # Lista para almacenar los pedidos enviados

        self.cliente_activo = True

    def run(self):
        try:
            self.socket_cliente.connect((self.HOST, self.PORT))
            # Recibir clave pública del servidor
            self.recibir_clave_publica_servidor()

            # Genera la clave AES y la envia cifrada con RSA
            self.generar_clave_aes()
            self.enviar_clave_aes()
            # AQUÍ CONTINUAR
            self.socket_cliente.send(self.name.encode()) # Lo primero que enviamos es el nombre del hilo Cliente
            print(f"[Cliente {self.id_cliente}] Conectado al servidor")
            
            # Recibir productos disponibles desde el servidor
            productos_disponibles = self.socket_cliente.recv(1024).decode()
            productos_disponibles = eval(productos_disponibles)  # Convertir de cadena a conjunto
            # print(f"[Cliente {self.id_cliente}] Productos disponibles: {productos_disponibles}")

            # Simulación de realizar pedidos
            self.realizar_pedido(productos_disponibles)
            # time.sleep(random.randint(1, 3))

            print(f"[Cliente {self.id_cliente}] Esperando a que el servidor cierre la conexión...")
            
            # El cliente queda bloqueado hasta que su pedido termina
            while self.cliente_activo:
                data = self.socket_cliente.recv(1024)
                
                if data == (b''):
                    self.cliente_activo = False
                    print(f"Cliente inactivo.")
                    break
                
                print(f"[Cliente {self.id_cliente}] Mensaje recibido: {data.decode()} del servidor.")
                
        except Exception as e:
            print(f"[Cliente {self.id_cliente}] Error: {e}")
        finally:
            print(f"[Cliente {self.id_cliente}] Conexión cerrada")
            self.socket_cliente.close()
    
    """
    ---------------------------------------------------------------
    Funciones iniciales para establecer las claves de encriptación
    ---------------------------------------------------------------
    """
    # Recibe la clave pública del servidor
    def recibir_clave_publica_servidor(self):
        """
        Recibe la clave pública RSA del servidor.
        """
        clave_publica = self.socket_cliente.recv(1024) # Recibe la clave pública del servidor
        self.key_rsa = RSA.import_key(clave_publica) # Clave pública RSA
        self.rsa_cipher = PKCS1_OAEP.new(self.key_rsa) # Cifrador RSA
    
    # Genera una clave AES para encriptar los mensajes
    def generar_clave_aes(self):
        """
        Genera una clave AES.
        """
        self.key_aes = get_random_bytes(16)
    
    # Envia la clave AES cifrada con la clave pública RSA del servidor
    def enviar_clave_aes(self):
        """
        Envia la clave AES cifrada con la clave pública RSA del servidor.
        """
        encrypted_key = self.rsa_cipher.encrypt(self.key_aes)
        encrypted_key_b64 = base64.b64encode(encrypted_key)
        self.socket_cliente.send(encrypted_key_b64)
    
    """
    ----------------------------
    Funciones para encriptación
    ----------------------------
    """
    # Función para encriptar mensajes con la clave simétrica AES
    def aes_encrypt(self, data):
        """
        Cifra un mensaje con AES.
        return: Mensaje cifrado
        """
        # cipher_aes = AES.new(self.key_aes, AES.MODE_EAX)
        cipher_aes = AES.new(self.key_aes, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode())
        return base64.b64encode(cipher_aes.nonce + tag + ciphertext).decode()
    
    # Función para desencriptar mensajes con la clave simétrica AES
    def aes_decrypt(self, mensaje_cifrado):
        """
        Descifra un mensaje con AES.
        return: Mensaje descifrado
        """
        mensaje_bytes = base64.b64decode(mensaje_cifrado)
        
        nonce = mensaje_bytes[:16]
        tag = mensaje_bytes[16:32]
        ciphertext = mensaje_bytes[32:]

        cipher_aes = AES.new(self.key_aes, AES.MODE_EAX, nonce=nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag).decode()
        return data
    
    """
    -------------------------------------------
    Funciones para comunicación con el servidor
    -------------------------------------------
    """
    # Realiza un pedido al servidor dados unos productos disponibles
    def realizar_pedido(self, productos_disponibles):
        if not productos_disponibles:
            print(f"[Cliente {self.id_cliente}] No hay productos disponibles para pedir.")
            return
        
        # Seleccionar un producto aleatorio
        producto_disponible = random.choice(list(productos_disponibles))
        producto: Producto = Producto.from_csv(producto_disponible) # Producto seleccionado
        # print(f"[Cliente {self.id_cliente}] PRODUCTO seleccionado: {producto}")

        id_pedido = 0 # ID 0 indica que el pedido se está creando
        cantidad = random.randint(1, 10) # Cantidad aleatoria (1-10)
        pedido: Pedido = Pedido(id_pedido, producto, cantidad) # Pedido creado

        # Formato esperado por el servidor: "PEDIDO id_pedido,tipo_producto,tiempo_producto,peso_producto,cantidad"
        pedido_info = f"PEDIDO {pedido.id_pedido},{pedido.producto.to_csv()},{pedido.cantidad}"
        print(f"[Cliente {self.id_cliente}] Realizando pedido: {pedido_info}...")
        self.socket_cliente.send(pedido_info.encode())

        print(f"[Cliente {self.id_cliente}] Pedido enviado, esperando respuesta del servidor...")
        respuesta = self.socket_cliente.recv(1024).decode() # El cliente espera la respuesta del servidor
        print(f"[Cliente {self.id_cliente}] RESPUESTA [{respuesta}] del servidor")
        self.pedidos_realizados.append(pedido.id_pedido)

    # Consulta el estado de un pedido al servidor
    def consultar_estado_pedido(self, id_pedido):
        consulta = f"CONSULTAR {id_pedido}"
        self.socket_cliente.send(consulta.encode())
        respuesta = self.socket_cliente.recv(1024).decode()
        print(f"[Cliente {self.id_cliente}] Estado del pedido {id_pedido}: {respuesta}")

# Función auxiliar para mostrar las opciones de los clientes (no se llama)
def opciones_cliente(clientes):
    while True:
        id_consulta = input("Seleccione un ID de cliente para consultar el estado de sus pedidos (o 'salir' para terminar): ")
        if id_consulta.lower() == "salir":
            break
        
        cliente_seleccionado = next((c for c in clientes if c.id_cliente == id_consulta), None)
        if cliente_seleccionado:
            for pedido in cliente_seleccionado.pedidos_realizados:
                cliente_seleccionado.consultar_estado_pedido(pedido)
        else:
            print("Cliente no encontrado.")


if __name__ == "__main__":
    iniciar = input("Presione enter para iniciar los clientes...") # Espera para iniciar los clientes
    
    clientes = []

    # Crear 5 clientes y iniciarlos
    for _ in range(10):
        cliente = ClientePanaderia()
        cliente.start()
        clientes.append(cliente)
    
    for cliente in clientes:
        cliente.join()