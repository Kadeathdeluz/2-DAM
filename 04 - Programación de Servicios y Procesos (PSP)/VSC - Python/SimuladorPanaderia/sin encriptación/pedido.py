import uuid
from producto import Producto
from estado_pedido import EstadoPedido

class Pedido:

    def __init__(self, id_pedido: int, producto: Producto, cantidad: int):
        """
        Inicializa un pedido con un ID único y una lista de productos.
        :param id_pedido: ID del pedido (int) -> En caso de ser 0 indica que el pedido se está creando,
        en caso distinto a 0 indica que se está "creando" un pedido en el servidor
        :param producto: Producto del pedido (Producto)
        :param cantidad: Cantidad del producto (int)
        """
        # Como en el servidor se recibe el pedido en formato texto, hace falta crear un pedido con un ID específico (que será el ID del pedido )
        if id_pedido == 0:
            self.id_pedido = uuid.uuid4().int
        else:
            self.id_pedido = id_pedido

        self.producto: Producto = producto
        self.cantidad: int = cantidad
        self.estado: EstadoPedido = EstadoPedido.CREADO
        self.tiempo_total: int = self._calcular_tiempo_total()  # Calcula el tiempo total al crear el pedido

    def _calcular_tiempo_total(self):
        """
        Calcula el tiempo total de horneado del pedido (tiempo por cantidad).
        :return: Tiempo total en segundos.
        """
        return int(self.producto.tiempo) * self.cantidad

    def __str__(self):
        """
        Devuelve una representación en forma de texto del pedido.
        """
        return (
            f"Pedido ID: {self.id_pedido}\n"
            f"Producto: {self.producto.tipo}\n"
            f"Cantidad: {self.cantidad}\n"
            f"Estado: {self.estado.name}\n"
            f"Tiempo Total: {self.tiempo_total} segundos"
        )
    
    """
    ------------------------------------------------------------------
    Métodos para convertir los objetos a String y los String a objetos
    ------------------------------------------------------------------
    """

    # Método para convertir el objeto a string en formato CSV
    def to_csv(self):
        return f"{self.id_pedido},{self.producto.to_csv()},{self.cantidad},{self.estado.name}"
    
    # Método para convertir un string en un objeto Pedido
    @staticmethod
    def from_csv(cadena: str):
        """
        Convierte una cadena en un objeto Pedido.
        :param cadena: Cadena con formato "id_pedido,producto,cantidad,estado,tiempo_total"
        :return: Objeto Pedido
        """
        id_pedido, producto_tipo, producto_tiempo, producto_peso, cantidad, estado = cadena.split(",")
        producto_csv = f"{producto_tipo},{producto_tiempo},{producto_peso}"
        producto = Producto.from_csv(producto_csv)
        
        pedido = Pedido(int(id_pedido), producto, int(cantidad))
        pedido.estado = EstadoPedido[estado]
        
        return pedido
