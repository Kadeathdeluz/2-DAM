from enum import Enum
import threading
import time
from pedido import Pedido

class EstadoHorno(Enum):
    """
    Clase enum para los posibles estados de un horno.
    """
    OK = "DISPONIBLE"
    WAIT = "OCUPADO"
    MANT = "MANTENIMIENTO"

class Horno:
    """
    Clase que representa un horno de la panadería.
    """
    _id_counter = 0  # Contador autoincremental para asignar IDs únicos a los hornos

    def __init__(self, max_ciclos):
        """
        Inicializa un horno con un ID único y un número máximo de ciclos de uso.
        :param max_ciclos: Número máximo de ciclos de uso antes de requerir mantenimiento.
        """
        Horno._id_counter += 1 # Incrementa el contador de IDs
        self.id_horno = Horno._id_counter
        self.estado = EstadoHorno.OK
        self.ciclos_uso = 0
        self.max_ciclos = max_ciclos
        self.pedido_actual = None
        self.lock = threading.Lock()

    def asignar_pedido(self, pedido: Pedido):
        """
        Asigna un pedido al horno si está disponible.
        :param pedido: Pedido a asignar al horno.
        :return: True si el pedido se asignó correctamente, False si el horno está ocupado.
        """
        with self.lock:
            if self.estado == EstadoHorno.OK:
                self.estado = EstadoHorno.WAIT
                self.pedido_actual = pedido
                print(f"[HORNO {self.id_horno}] Pedido asignado.")
                return True
            return False

    def calcular_ciclo(self):
        """
        Calcula el número de ciclos que tomará hornear el pedido.
        :return: Número de ciclos requeridos para hornear el pedido.
        """
        if not self.pedido_actual:
            return 0
        return sum(producto.peso * cantidad for producto, cantidad in self.pedido_actual.productos)

    def cocinar_pedido(self):
        """
        Simula la cocción del pedido, manteniendo el horno ocupado.
        """
        if self.pedido_actual:
            print(f"[HORNO {self.id_horno}] Cocinando pedido por {self.pedido_actual.tiempo_total} segundos...")
            time.sleep(self.pedido_actual.tiempo_total)
            self.liberar_horno()

    def liberar_horno(self):
        """
        Libera el horno o lo pasa a mantenimiento tras verificar si requiere mantenimiento.
        """
        with self.lock:
            ciclos_actuales = self.calcular_ciclo()
            self.ciclos_uso += ciclos_actuales
            print(f"[HORNO {self.id_horno}] Pedido terminado. Ciclos de uso: {self.ciclos_uso}/{self.max_ciclos}")
            self.pedido_actual = None
            if self.ciclos_uso >= self.max_ciclos:
                self.estado = EstadoHorno.MANT
                print(f"[HORNO {self.id_horno}] Entra en mantenimiento.")
            else:
                self.estado = EstadoHorno.OK

    def mantenimiento(self):
        """
        Mantiene el horno en mantenimiento por un ciclo antes de volver a estar disponible.
        Vamos a asumir que el timepo que se tarda en realizar el mantenimiento es de 5 segundos (no está especificado en las instrucciones).
        """
        with self.lock:
            print(f"[HORNO {self.id_horno}] Realizando mantenimiento...")
            time.sleep(5)  # Simula el tiempo de mantenimiento
            self.ciclos_uso = 0
            self.estado = EstadoHorno.OK
            print(f"[HORNO {self.id_horno}] Mantenimiento finalizado. Disponible para nuevos pedidos.")

    def __str__(self):
        return f"Horno {self.id_horno}: Estado={self.estado.value}, Ciclos usados={self.ciclos_uso}/{self.max_ciclos}"
