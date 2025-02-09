class Producto:
    def __init__(self, tipo: str, tiempo: int, peso: int):
        """
        Inicializa un producto con su tipo, tiempo de horneado y peso.
        :param tipo: Nombre del producto (str)
        :param tiempo: Tiempo de horneado en segundos (int)
        :param peso: Peso del producto en ciclos (int)
        """
        self.tipo = tipo
        self.tiempo = tiempo
        self.peso = peso

    def __str__(self):
        return f"Producto: {self.tipo}, Tiempo: {self.tiempo} seg, Peso: {self.peso}"