# Clase Pedido
class Pedido:
    def __init__(self, id_pedido):
        """
        Inicializa un pedido con un ID único.
        """
        self.id_pedido = id_pedido
        self.info_pedido = []  # Lista de productos en el pedido
        self.tiempo_total = 0  # Tiempo total del pedido (calculado)

    def agregar_producto(self, tipo_producto, cantidad, tiempo_por_unidad):
        """
        Agrega un producto al pedido.
        :param tipo_producto: Tipo de producto (ProductoEnum)
        :param cantidad: Cantidad solicitada del producto
        :param tiempo_por_unidad: Tiempo de horneado por unidad
        """
        producto = {
            "tipo_producto": tipo_producto,
            "cantidad": cantidad,
            "tiempo": tiempo_por_unidad
        }
        self.info_pedido.append(producto)
        self.recalcular_tiempo_total()

    def recalcular_tiempo_total(self):
        """
        Recalcula el tiempo total del pedido sumando los tiempos de todos los productos.
        """
        self.tiempo_total = sum(
            item["cantidad"] * item["tiempo"] for item in self.info_pedido
        )

    def __str__(self):
        """
        Devuelve una representación del pedido.
        """
        productos_info = "\n".join(
            f"- {item['tipo_producto'].value}: {item['cantidad']} unidades, {item['tiempo']} seg/unidad"
            for item in self.info_pedido
        )
        return (
            f"Pedido ID: {self.id_pedido}\n"
            f"Productos:\n{productos_info}\n"
            f"Tiempo Total: {self.tiempo_total} segundos"
        )