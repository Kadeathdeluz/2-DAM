# Clase Producto (representa un producto de un tipo, con un tiempo de horneado y un peso)
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

    # Método string para representar el objeto Producto
    def __str__(self):
        return f"Producto: {self.tipo}, Tiempo: {self.tiempo} seg, Peso: {self.peso}"
    
    """
    ------------------------------------------------------------------
    Métodos para convertir los objetos a String y los String a objetos
    ------------------------------------------------------------------
    """

    # Método para convertir el objeto a string en formato CSV
    def to_csv(self):
        """
        Devuelve una representación en forma de texto del producto en formato CSV.
        :return: Cadena con formato "tipo,tiempo,peso"
        """
        return f"{self.tipo},{self.tiempo},{self.peso}"
    
    # Método para convertir un string en un objeto Producto
    @staticmethod
    def from_csv(cadena: str):
        """
        Convierte una cadena en un objeto Producto.
        :param cadena: Cadena con formato "tipo,tiempo,peso"
        :return: Objeto Producto
        """
        tipo, tiempo, peso = cadena.split(",")
        return Producto(str(tipo), int(tiempo), int(peso))