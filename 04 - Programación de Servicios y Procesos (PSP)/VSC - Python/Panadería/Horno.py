import threading
from enums import EstadoHorno

# Clase Horno, hereda de Thread
class Horno (threading.Thread):
    def __init__(self, id_horno, ciclos_maximos):
        self.id_horno = id_horno
        self.estado = EstadoHorno.OK
        self.ciclos_usados = 0
        self.ciclos_maximos = ciclos_maximos

    # Asigna el horno a un pedido
    def asignar_pedido(self):
        if self.estado == EstadoHorno.OK:
            self.estado = EstadoHorno.WAIT
            return True
        return False

    # Libera el horno después de un ciclo, o lo manda a mantenimiento si ha alcanzado el máximo de ciclos
    def liberar_horno(self):
        self.ciclos_usados += 1
        if self.ciclos_usados >= self.ciclos_maximos:
            self.estado = EstadoHorno.MANT
        else:
            self.estado = EstadoHorno.OK

    # Método para realizar mantenimiento del horno
    def realizar_mantenimiento(self):
        self.ciclos_usados = 0
        self.estado = EstadoHorno.OK