from producto import Producto
class Inventario:
    def __init__(self):
        self.__productos = []

    def agregar_producto(self, producto: Producto):
        for prod in self.__productos:
            if prod.get_nombre().lower() == producto.get_nombre().lower():
                raise ValueError("El producto ya existe en el inventari.")
        self.__productos.append(producto)

    def actualizar_producto(self, nombre: str, precio: float = None, cantidad: int = None):
        producto = self.buscar_producto(nombre)
        if precio is not None:
            producto.set_precio(precio)
        if cantidad is not None:
            producto.set_cantidad(cantidad)

    def eliminar_producto(self, nombre: str):
        producto = self.buscar_producto(nombre)
        self.__productos.remove(producto)

    # def mostrar_inventario(self):
    #     if not self.__productos:
    #         print("El inventario está vacío.")
    #     else:
    #         for producto in self.__productos:
    #             print(producto)

    def buscar_producto(self, nombre: str) -> Producto:
        for producto in self.__productos:
            if producto.get_nombre().lower() == nombre.lower():
                return producto
        raise ValueError("Producto no encontrado.")