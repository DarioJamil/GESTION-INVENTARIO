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

       # Contenedor para los botones
        botones_frame = tk.Frame(root)
        botones_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        #sticky="w" en el grid de botones_frame: Esto asegura que el contenedor de botones se pegue al borde izquierdo del contenedor principal.
        #padx=5 en el grid de botones_frame: Agrega un margen de 5 píxeles entre el borde izquierdo de la ventana y el primer botón.
        #  botones_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="w", padx=5)

        # Botones dentro del contenedor
        tk.Button(botones_frame, text="Agregar", command=self.agregar_producto).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(botones_frame, text="Buscar", command=self.buscar_producto).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(botones_frame, text="Actualizar", command=self.actualizar_producto).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(botones_frame, text="Eliminar", command=self.eliminar_producto).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(botones_frame, text="Limpiar", command=self.limpiar_producto).grid(row=0, column=5, padx=5, pady=5)
        # tk.Button(root, text="Guardar en archivo", command=self.guardar_en_archivo).grid(row=6, column=0, columnspan=2, pady=10)

      # Frame para contener la tabla y los scrollbars
        tabla_frame = tk.Frame(root)
        tabla_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Tabla para mostrar productos
        self.tabla = ttk.Treeview(tabla_frame, columns=("Nombre", "Categoría", "Precio", "Cantidad"), show="headings")

        # Configurar encabezados de columnas
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Categoría", text="Categoría")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.heading("Cantidad", text="Cantidad")

        self.tabla.column("Nombre", width=150, anchor="center")
        self.tabla.column("Categoría", width=100, anchor="center")
        self.tabla.column("Precio", width=80, anchor="center")
        self.tabla.column("Cantidad", width=80, anchor="center")

        # Scrollbar vertical
        scrollbar_vertical = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar_vertical.set)

        # Scrollbar horizontal
        scrollbar_horizontal = ttk.Scrollbar(tabla_frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(xscrollcommand=scrollbar_horizontal.set)

        # Posicionamiento de la tabla y los scrollbars dentro del Frame
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew")
        # self.tabla.pack(side="left", fill="both", expand=True)
        # scrollbar_vertical.pack(side="right", fill="y")
        # scrollbar_horizontal.pack(side="bottom", fill="x")

        #Configurar el contenedor para que la tabla y scrollbars crezcan con la ventana
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)

        # Evento para seleccionar fila
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.tabla.bind("<KeyRelease>", self.seleccionar_fila)

        # Mostrar productos iniciales
        self.mostrar_inventario()

    def seleccionar_fila(self, event):
        # Obtener la fila seleccionada
        item = self.tabla.focus()
        if not item:
            return  # Si no hay selección, salir

        # Obtener los valores de la fila seleccionada
        valores = self.tabla.item(item, "values")
        if valores:
            # Rellenar los campos del formulario
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, valores[0])

            self.categoria_entry.delete(0, tk.END)
            self.categoria_entry.insert(0, valores[1])

            self.precio_entry.delete(0, tk.END)
            self.precio_entry.insert(0, valores[2])

            self.cantidad_entry.delete(0, tk.END)
            self.cantidad_entry.insert(0, valores[3])


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
            
    def limpiar_producto(self):
        self.nombre_entry.delete(0, tk.END)
        self.categoria_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)

        # Opcional: Notificar al usuario
        # messagebox.showinfo("Formulario limpio", "Los campos han sido limpiados.")

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
