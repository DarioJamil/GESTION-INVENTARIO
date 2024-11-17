import tkinter as tk
from tkinter import messagebox, ttk
from producto import Producto
from inventario import Inventario


class VentanaInventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Inventario")
        self.inventario = Inventario()

        # Cargar productos desde el archivo
        self.cargar_desde_archivo()

        # Campos de texto
        tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry = tk.Entry(root)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Categoría:").grid(row=1, column=0, padx=5, pady=5)
        self.categoria_entry = tk.Entry(root)
        self.categoria_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Precio:").grid(row=2, column=0, padx=5, pady=5)
        self.precio_entry = tk.Entry(root)
        self.precio_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Cantidad:").grid(row=3, column=0, padx=5, pady=5)
        self.cantidad_entry = tk.Entry(root)
        self.cantidad_entry.grid(row=3, column=1, padx=5, pady=5)

        # Botones
        tk.Button(root, text="Agregar", command=self.agregar_producto).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(root, text="Buscar", command=self.buscar_producto).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(root, text="Actualizar", command=self.actualizar_producto).grid(row=5, column=0, padx=5, pady=5)
        tk.Button(root, text="Eliminar", command=self.eliminar_producto).grid(row=5, column=1, padx=5, pady=5)
        tk.Button(root, text="Guardar en archivo", command=self.guardar_en_archivo).grid(row=6, column=0, columnspan=2, pady=10)

       # Tabla para mostrar productos
        self.tabla = ttk.Treeview(root, columns=("Nombre", "Categoría", "Precio", "Cantidad"), show="headings")
        self.tabla.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        # Configurar encabezados de columnas
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Categoría", text="Categoría")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.heading("Cantidad", text="Cantidad")
        
        self.tabla.column("Nombre", width=150, anchor="center")
        self.tabla.column("Categoría", width=100, anchor="center")
        self.tabla.column("Precio", width=80, anchor="center")
        self.tabla.column("Cantidad", width=80, anchor="center")


        # Mostrar productos iniciales
        self.mostrar_inventario()

    def agregar_producto(self):
        try:
            nombre = self.nombre_entry.get()
            categoria = self.categoria_entry.get()
            precio = float(self.precio_entry.get())
            cantidad = int(self.cantidad_entry.get())
            producto = Producto(nombre, categoria, precio, cantidad)
            self.inventario.agregar_producto(producto)
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado.")
            self.mostrar_inventario()
            self.guardar_en_archivo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def buscar_producto(self):
        try:
            nombre = self.nombre_entry.get()
            producto = self.inventario.buscar_producto(nombre)
            messagebox.showinfo("Producto encontrado", str(producto))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_producto(self):
        try:
            nombre = self.nombre_entry.get()
            precio = float(self.precio_entry.get()) if self.precio_entry.get() else None
            cantidad = int(self.cantidad_entry.get()) if self.cantidad_entry.get() else None
            self.inventario.actualizar_producto(nombre, precio, cantidad)
            messagebox.showinfo("Éxito", f"Producto '{nombre}' actualizado.")
            self.mostrar_inventario()
            self.guardar_en_archivo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_producto(self):
        try:
            nombre = self.nombre_entry.get()
            self.inventario.eliminar_producto(nombre)
            messagebox.showinfo("Éxito", f"Producto '{nombre}' eliminado.")
            self.mostrar_inventario()
            self.guardar_en_archivo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def guardar_en_archivo(self):
        try:
            with open("inventario.txt", "w", encoding="utf-8") as archivo:
                for producto in self.inventario._Inventario__productos:
                    archivo.write(f"{producto.get_nombre()},{producto.get_categoria()},{producto.get_precio()},{producto.get_cantidad()}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def cargar_desde_archivo(self):
        try:
            with open("inventario.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    try:
                        # Separar datos por comas
                        partes = linea.strip().split(",")
                        nombre = partes[0].strip()
                        categoria = partes[1].strip()
                        precio = float(partes[2].strip())
                        cantidad = int(partes[3].strip())
                        
                        # Crear producto y agregar al inventario
                        producto = Producto(nombre, categoria, precio, cantidad)
                        self.inventario.agregar_producto(producto)
                    except (ValueError, IndexError) as e:
                        print(f"Error al procesar la línea '{linea.strip()}': {e}")
        except FileNotFoundError:
            # Si no existe el archivo, no se hace nada
            pass
        except Exception as e:
            messagebox.showerror("Error al cargar el archivo", str(e))



    def mostrar_inventario(self):
    # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    # Agregar productos a la tabla
        for producto in self.inventario._Inventario__productos:
            self.tabla.insert("", "end", values=(
                producto.get_nombre(), 
                producto.get_categoria(), 
                producto.get_precio(), 
                producto.get_cantidad()
            ))



if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaInventario(root)
    root.mainloop()
