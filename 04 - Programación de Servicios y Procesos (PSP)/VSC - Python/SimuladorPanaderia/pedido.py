import random
from producto import Producto

class Pedido:
    _id_counter = 0  # Contador de ID autoincremental para asignar IDs únicos a los pedidos

    def __init__(self, productos):
        """
        Inicializa un pedido con un ID único y una lista de productos.
        :param productos: Lista de objetos Producto
        """
        Pedido._id_counter += 1
        self.id_pedido = Pedido._id_counter
        self.productos = productos  # Lista de tuplas (Producto, cantidad)
        self.tiempo_total = self._calcular_tiempo_total(self.productos)  # Calcula el tiempo total al crear el pedido

    def _calcular_tiempo_total(self, productos):
        """
        Calcula el tiempo total del pedido sumando los tiempos de todos los productos.
        :param productos: Lista de tuplas (Producto, cantidad)
        :return: Tiempo total del pedido
        """
        return sum(producto.tiempo * cantidad for producto, cantidad in productos)

    def __str__(self):
        """
        Devuelve una representación en forma de texto del pedido.
        """
        productos_info = "\n".join(
            f"- {producto.tipo}: {cantidad} unidades, {producto.tiempo} seg/unidad"
            for producto, cantidad in self.productos
        )
        return (
            f"Pedido ID: {self.id_pedido}\n"
            f"Productos:\n{productos_info}\n"
            f"Tiempo Total: {self.tiempo_total} segundos"
        )
    
"""
TEST DE LA CLASE PEDIDO

if __name__ == "__main__":
    # Ejemplo de uso de la clase Pedido
    lista_pedidos = []
    # Crear 5 pedidos con productos de ejemplo
    for i in range(5):
        pedido = Pedido(
            productos=[
                (Producto("Pan", 1, 1), random.choice([0, 5, 10, 15])),
                (Producto("Galleta", 2, 2), random.choice([0, 5, 10, 15])),
                (Producto("Torta", 3, 3), random.choice([0, 5, 10, 15]))
                ]
        )
        lista_pedidos.append(pedido)
        print(pedido)
"""
