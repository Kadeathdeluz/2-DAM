from enum import Enum

class EstadoHorno(Enum):
    """
    Clase enum para los posibles estados de un horno.
    """
    DISPONIBLE = "DISPONIBLE"
    OCUPADO = "OCUPADO"
    MANTENIMIENTO = "MANTENIMIENTO"