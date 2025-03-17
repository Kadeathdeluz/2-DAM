from enum import Enum

class EstadoPedido(Enum):
    """
    Clase enum para los posibles estados de un pedido.
    """
    CREADO = "CREADO" # Estado inicial del pedido
    PENDIENTE = "PENDIENTE" # Estado del pedido cuando está en espera de ser asignado a un horno
    EN_PROCESO = "EN PROCESO" # Estado del pedido cuando está siendo horneado
    LISTO = "LISTO" # Estado del pedido cuando ha sido horneado y está listo