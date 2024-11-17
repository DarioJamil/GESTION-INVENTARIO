class Producto:
    def __init__(self, nombre: str, categoria: str, precio: float, cantidad: int):
        self.__nombre = nombre
        self.__categoria = categoria
        self.__precio = precio
        self.__cantidad = cantidad

    # Getters
    def get_nombre(self) -> str:
        return self.__nombre

    def get_categoria(self) -> str:
        return self.__categoria

    def get_precio(self) -> float:
        return self.__precio

    def get_cantidad(self) -> int:
        return self.__cantidad

    # Setters
    def set_precio(self, precio: float):
        if precio > 0:
            self.__precio = precio
        else:
            raise ValueError("El precio debe ser mayor que 0.")

    def set_cantidad(self, cantidad: int):
        if cantidad >= 0:
            self.__cantidad = cantidad
        else:
            raise ValueError("La cantidad debe ser mayor o igual que 0.")

    # String producto
    def __str__(self):
        return f"Producto: {self.__nombre}, Categoría: {self.__categoria}, Precio: ${self.__precio:.2f}, Cantidad: {self.__cantidad}"






