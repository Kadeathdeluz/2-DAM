import socket
import threading
import random
import time

# Clase HiloCliente que hereda de threading.Thread que representa a un Cliente
class HiloCliente(threading.Thread):
    def __init__(self, id_cliente):
        super().__init__()
        self.id_cliente = id_cliente

    def run(self):
        # Método que lanzará cada hilo para "comportarse" como un Cliente
        hablar_con_servidor(self)

# El cliente crea el socket y se intenta conectar a la dirección indicada (host y puerto) y comunicarse con el Servidor
def hablar_con_servidor(self):
    try:
        # Crea el socket y trata de conectarse
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(("127.0.0.1", 4500))
        
        # Bucle para mandar mensajes (del 1 al 3)
        for i in range(1, 4):
            time.sleep(random.uniform(0.5, 1.5)) # Tiempo aleatorio para simular concurrencia
            mensaje = f"Mensaje {i} del cliente {self.id_cliente}".encode() # Mensaje del cliente codificado
            cliente.sendall(mensaje) # Manda el mensaje codificado
            print(f"Cliente {self.id_cliente} envió: {mensaje.decode()}") # Printea el mensaje que ha mandado
            
            # Espera la respuesta del Servidor tras enviar cada mensaje
            respuesta = cliente.recv(1024).decode()
            print(f"Cliente {self.id_cliente} recibió: {respuesta}") # Si el Servidor recibe el mensaje manda un "ok" que el cliente imprime
        cliente.sendall(b"OK") # Ok para avisar de que ha terminado la comunicación
        respuesta_final = cliente.recv(1024).decode() # respuesta final del servidor
        print(f"Cliente {self.id_cliente} recibió: {respuesta_final}") # Imprime el mensaje final
        
        cliente.close()  # Cierra la conexión después de enviar los tres mensajes y recibir la respuesta final
    except Exception as e:
        print(f"Error en el cliente {self.id_cliente}: {e}")

# Lanza num_clientes hilos cliente
def bateria_clientes(num_clientes):
    # Creamos num_clientes clientes como ejemplo
    clientes = [HiloCliente(i) for i in range(1, num_clientes+1)]
    for cliente in clientes:
        cliente.start()
    for cliente in clientes:
        cliente.join()

# Creamos e iniciamos varios clientes para probar el Servidor
if __name__ == "__main__":
    # Lanza los clientes
    bateria_clientes(5) # Elegimos 5 clientes como ejemplo, basta con cambiar el número