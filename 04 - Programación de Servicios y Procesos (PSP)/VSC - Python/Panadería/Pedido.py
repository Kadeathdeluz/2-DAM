# Clase Pedido
class Pedido:
    def __init__(self, id_pedido, productos):
        self.id_pedido = id_pedido # ID único del pedido
        self.productos = productos  # Lista de productos en el pedido
        self.tiempo_total = self._calcular_tiempo_total() # Tiempo total del pedido (calculado)

    def _calcular_tiempo_total(self):
        """
        Recalcula el tiempo total del pedido sumando los tiempos de todos los productos.
        """
        return sum(
            item["cantidad"] * item["tiempo"] for item in self.productos
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