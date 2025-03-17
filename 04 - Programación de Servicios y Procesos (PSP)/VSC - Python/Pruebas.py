import random
import threading
import time

# Clase Producto (representa un producto de un tipo, con un tiempo de horneado y un peso) ✅
class Producto:
    def __init__(self, tipo: str, tiempo: int, peso: int):
        """
        Inicializa un producto con su tipo, tiempo de horneado y peso.
        :param tipo: Nombre del producto (str)
        :param tiempo: Tiempo de horneado en segundos (int)
        :param peso: Peso del producto en ciclos (int)
        """
        self.tipo = tipo
        self.tiempo = tiempo
        self.peso = peso

    def __str__(self):
        return f"Producto: {self.tipo}, Tiempo: {self.tiempo} seg, Peso: {self.peso}"

# Clase Pedido (representa un pedido con un Producto y una cantidad)
class Pedido:
    def __init__(self, producto: Producto, cantidad: int):
        """
        Inicializa un pedido con un producto y una cantidad.
        :param producto: Producto del pedido
        :param cantidad: Cantidad del producto
        """
        self.producto = producto
        self.cantidad = cantidad
    def __str__(self):
        return f"Producto: {self.producto.tipo}, Cantidad: {self.cantidad}"

# Clase Cliente (hereda de Thread)
class ClientePanaderia(threading.Thread):
    # Contador de ID autoincremental para asignar IDs únicos a los clientes
    _id_counter = 0

    def __init__(self):
        super().__init__()
        # Asigna un ID único al cliente y lo incrementa para el siguiente
        self.id_cliente = ClientePanaderia._id_counter
        ClientePanaderia._id_counter += 1

        self.pedidos = []  # Lista de pedidos realizados por el cliente

    def run(self):
        # Realiza 3 pedidos con una cantidad aleatoria de productos de cada tipo
        for _ in range(3):
            # Por cada producto disponible, selecciona una cantidad aleatoria
            for producto in ["Pan", "Galleta", "Pastel", "Dona"]:

                self.pedidos.append(Pedido(producto, random.randint(0, 10)))
        time.sleep(100)  # Espera 100 segundos para simular el tiempo de espera de los pedidos
        
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
                    print(f"Pedido: {pedido}")
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

class ThreadCounter:
    def __init__(self):
        self._counter = 0
        self._lock = threading.Lock()
    def count(self, thread_num):
        while True:
            with self._lock:
                self._counter += 1
                print(f"[Thread {thread_num}] Counter: {self._counter}")
                time.sleep(1)
                print(f"[Thread {thread_num}] Counter: {self._counter} after sleep")
            time.sleep(2)
"""
    def increment(self):
        with self._lock:
            self._counter += 1

    def decrement(self):
        with self._lock:
            self._counter -= 1

    def value(self):
        with self._lock:
            return self._counter
"""

# Simulación de 5 clientes
if __name__ == "__main__":
    """
    clientes = []

    # Crea 5 clientes de ejemplo y los inicia
    for _ in range(5):
        cliente = ClientePanaderia()
        cliente.start()
        clientes.append(cliente)
    
    opciones_cliente(clientes)
    """
    # tc = ThreadCounter()
    # for i in range(10):
      #  threading.Thread(target=tc.count, args=(i,)).start()
    while True:

            # Bucle: Solicita al usuario el número de hornos
            while True:
                try:
                    num_hornos = int(input("Ingrese el número de hornos: "))
                    if num_hornos > 0:
                        break
                    print("Error: Debe haber al menos un horno.")
                except ValueError:
                    print("Error: Entrada inválida. Asegúrese de ingresar un número entero.")
            
            # Bucle: Solicita al usuario el número de ciclos antes del mantenimiento
            while True:
                try:
                    max_ciclos_horno = int(input("Ingrese el máximo de ciclos por horno antes del mantenimiento: "))
                    if max_ciclos_horno > 0:
                        break
                    print("Error: El número de ciclos debe ser mayor a 0.")
                except ValueError:
                    print("Error: Entrada inválida. Asegúrese de ingresar un número entero.")
            
            # Bucle: Solicita al usuario el algoritmo de planificación
            while True:
                try:
                    algoritmo = input("Seleccione el algoritmo de planificación (FIFO/SJF): ").strip().upper()
                    if algoritmo in ["FIFO", "SJF"]:
                        break
                    print("Opción inválida. Por favor, elija entre FIFO o SJF.")
                except ValueError:
                    print("Error: Entrada inválida. Asegúrese de ingresar valores numéricos correctos.")
            break # Sale del bucle si se ingresan valores válidos
    print(f"Numero de hornos: {num_hornos}")
    print(f"Maximo de ciclos por horno: {max_ciclos_horno}")
    print(f"Algoritmo de planificacion: {algoritmo}")