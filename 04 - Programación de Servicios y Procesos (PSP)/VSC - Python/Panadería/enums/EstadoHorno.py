from enum import Enum

# Clase Enum para los estados de los hornos
class EstadoHorno(Enum):
    OK = "Disponible"
    WAIT = "Ocupado"
    MANT = "Mantenimiento"