# Imports globales
import threading
import time
# Imports locales
from estado_pedido import EstadoPedido
from estado_horno import EstadoHorno
from pedido import Pedido

class Horno(threading.Thread):
    """
    Clase que representa un horno de la panadería.
    """
    _id_counter = 0  # Contador autoincremental para asignar IDs únicos a los hornos

    def __init__(self, max_ciclos: int, servidor_callback: callable):
        """
        Inicializa un horno con un ID único y un número máximo de ciclos de uso.
        :param max_ciclos: Número máximo de ciclos de uso antes de requerir mantenimiento.
        """
        super().__init__()
        Horno._id_counter += 1  # Incrementa el contador de IDs
        self.id_horno: int = Horno._id_counter
        self.estado: EstadoHorno = EstadoHorno.DISPONIBLE
        self.ciclos_uso: int = 0
        self.max_ciclos: int = max_ciclos
        self.pedido_actual: Pedido = None
        self.lock: threading.Lock = threading.Lock()
        self.evento_pedido: threading.Event = threading.Event()  # Evento para notificar cuando hay un pedido
        self.daemon = True  # Permite que el hilo termine cuando el programa principal finalice

        # Variables para estadísticas
        self.tiempo_en_uso: float = 0
        self.productos_horneados: int = 0
        self.servidor_callback: callable = servidor_callback  # Callback para notificar al servidor

    def run(self):
        """
        Hilo principal del horno. Espera pedidos y los procesa.
        """
        while True:
            self.evento_pedido.wait()  # Espera hasta que se asigne un pedido
            with self.lock:
                if self.pedido_actual:
                    self.cocinar_pedido()

    def cocinar_pedido(self):
        """
        Cocina el pedido asignado.
        """
        self.estado = EstadoHorno.OCUPADO
        # print(f"Horno {self.id_horno} horneando Pedido {self.pedido_actual.id_pedido} "f"({self.pedido_actual.cantidad}x {self.pedido_actual.producto.tipo})")
        inicio = time.time()  # Marca el inicio del horneado

        time.sleep(self.pedido_actual.tiempo_total)  # Simula el horneado

        self.ciclos_uso += self.pedido_actual.cantidad * self.pedido_actual.producto.peso
        # print(f"Horno {self.id_horno} terminó de hornear Pedido {self.pedido_actual.id_pedido}")
        
        # Estadísticas
        self.tiempo_en_uso += time.time() - inicio  # Registra tiempo de uso
        self.productos_horneados += self.pedido_actual.cantidad  # Cuenta productos horneados

        self.pedido_actual.estado = EstadoPedido.LISTO  # Marca el pedido como listo
        
        # Notificar al servidor cuando se completa un pedido
        self.servidor_callback(self.id_horno, self.pedido_actual, self.tiempo_en_uso, self.productos_horneados)
        
        self.pedido_actual = None

        if self.ciclos_uso >= self.max_ciclos:
            self.mantenimiento()
        else:
            self.estado = EstadoHorno.DISPONIBLE

        self.evento_pedido.clear()  # Espera el siguiente pedido

    def asignar_pedido(self, pedido: Pedido):
        """
        Asigna un pedido al horno si está disponible.
        :param pedido: Pedido a asignar.
        :return: True si el pedido se asignó, False si el horno estaba ocupado.
        """
        with self.lock:
            if self.estado == EstadoHorno.DISPONIBLE:
                self.pedido_actual = pedido
                self.evento_pedido.set()  # Notifica al hilo que hay un pedido
                return True
            return False  # Horno ocupado o en mantenimiento

    def mantenimiento(self):
        """
        Realiza el mantenimiento del horno y lo deja disponible nuevamente.
        """
        print(f"Horno {self.id_horno} en mantenimiento.")
        self.estado = EstadoHorno.MANTENIMIENTO
        time.sleep(5)  # Simula el tiempo de mantenimiento
        self.ciclos_uso = 0
        self.estado = EstadoHorno.DISPONIBLE
        print(f"Horno {self.id_horno} disponible nuevamente.")

    def __str__(self):
        return (f"Horno <{self.id_horno}>: Estado={self.estado.name}, "
                f"Ciclos={self.ciclos_uso}/{self.max_ciclos}, "
                f"Productos horneados={self.productos_horneados}, "
                f"Tiempo en uso={self.tiempo_en_uso:.2f}s")