import tkinter as tk
from tkinter import ttk, messagebox
import conexion  # Asegúrate de que conexion.py está en el mismo directorio
from botones import configurar_estilos



class InventarioApp:
    def __init__(self, container):
        """
        container: Frame donde se dibujará la interfaz (desde el menú principal).
        """
        self.container = container
        # Limpia el contenedor para cargar la nueva interfaz
        for widget in self.container.winfo_children():
            widget.destroy()
        self.container.configure(bg="white")
        configurar_estilos(self.container)
        
        
        # Conexión a la base de datos
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()
        
        # -------------------------------------------
        # Título "INVENTARIO"
        # -------------------------------------------
        title_frame = tk.Frame(self.container, bg="#ECECEC", height=40, padx=10, pady=5)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(title_frame, text="INVENTARIO", font=("Helvetica", 14, "bold"), bg="#ECECEC")\
            .pack(side=tk.LEFT)
        
        # -------------------------------------------
        # Frame principal (dividido en dos secciones)
        # -------------------------------------------
        main_frame = tk.Frame(self.container, bg="white")
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Sección Izquierda (1/3): Búsqueda y lista de artículos
        left_frame = tk.Frame(main_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 1) Barra de búsqueda (por código o nombre)
        search_frame = tk.Frame(left_frame, bg="white", padx=10, pady=10)
        search_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(search_frame, text="Buscar Artículo (ID o Nombre):", font=("Helvetica", 10), bg="white")\
            .pack(side=tk.LEFT)
        self.buscar_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.buscar_var, width=20, font=("Helvetica", 10))\
            .pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Buscar", style="Gris.TButton",width=6,
                  command=self.buscar_articulo).pack(side=tk.LEFT, padx=5)
        
        # 2) Treeview (muestra todos los campos del artículo)
        cols = ("codigo", "nombre", "precio", "costo", "existencia", "reorden", "categoria", "proveedor", "unidad")
        self.tree = ttk.Treeview(left_frame, columns=cols, show="headings", height=20)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        headings = [
            ("codigo", "Código", 100),
            ("nombre", "Nombre", 200),
            ("precio", "Precio", 80),
            ("costo", "Costo", 80),
            ("existencia", "Existencia", 80),
            ("reorden", "Reorden", 80),
            ("categoria", "ID Cat.", 80),
            ("proveedor", "ID Prov.", 80),
            ("unidad", "ID Und.", 80)
        ]
        for col, txt, w in headings:
            self.tree.heading(col, text=txt, anchor="center")
            self.tree.column(col, width=w, anchor="center")
        scroll_y = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        scroll_y.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_articulo_lista)
        
        # Sección Derecha (2/3): Botones y formulario de artículos
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame para botones (Nuevo, Eliminar, Guardar)
        btn_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        btn_right_frame.pack(side=tk.TOP, fill=tk.X)
        ttk.Button(btn_right_frame, text="Limpiar Datos",style="Azul.TButton", command=self.nuevo_articulo)\
            .pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_right_frame, text="Eliminar",style="Peligro.TButton", command=self.eliminar_articulo)\
            .pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_right_frame, text="Guardar",style="Exito.TButton", width=8, command=self.guardar_articulo)\
            .pack(side=tk.LEFT, padx=5)
        
        # Frame del formulario
        form_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        form_right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Variables del formulario
        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.costo_var = tk.StringVar()
        self.existencia_var = tk.StringVar()
        self.reorden_var = tk.StringVar()
        self.cat_var = tk.StringVar()
        self.prov_var = tk.StringVar()
        self.und_var = tk.StringVar()
        
        # Etiquetas y entradas (dispuestas en grid)
        labels = [
            ("Código:", self.codigo_var, 0),
            ("Nombre:", self.nombre_var, 1),
            ("Precio:", self.precio_var, 2),
            ("Costo:", self.costo_var, 3),
            ("Existencia:", self.existencia_var, 4),
            ("Reorden:", self.reorden_var, 5),
            ("ID Categoría:", self.cat_var, 6),
            ("ID Proveedor:", self.prov_var, 7),
            ("ID Unidad:", self.und_var, 8)
        ]
        for text, var, row in labels:
            tk.Label(form_right_frame, text=text, font=("Helvetica", 10), bg="white")\
                .grid(row=row, column=0, sticky=tk.E, padx=5, pady=5)
            tk.Entry(form_right_frame, textvariable=var, width=25, font=("Helvetica", 10))\
                .grid(row=row, column=1, padx=5, pady=5)
        
        # Carga inicial de artículos
        self.cargar_lista_articulos()

    # --------------------------------------------------
    # Funciones para la sección IZQUIERDA
    # --------------------------------------------------
    def cargar_lista_articulos(self, filtro=""):
        """Carga en el Treeview los artículos desde la BD."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        sql = (
            "SELECT codigo, nombre, precio, costo, existencia, reorden, "
            "id_categoria, id_proveedor, id_unidad FROM Articulo"
        )
        params = ()
        if filtro:
            sql += " WHERE codigo LIKE %s OR nombre LIKE %s"
            filtro_param = f"%{filtro}%"
            params = (filtro_param, filtro_param)
        self.cursor.execute(sql, params)
        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def buscar_articulo(self):
        filtro = self.buscar_var.get().strip()
        self.cargar_lista_articulos(filtro)

    def seleccionar_articulo_lista(self, event):
        sel = self.tree.focus()
        if not sel:
            return
        values = self.tree.item(sel, "values")
        (
            codigo, nombre, precio, costo, existencia,
            reorden, idc, idp, idu
        ) = values
        self.codigo_var.set(codigo)
        self.nombre_var.set(nombre)
        self.precio_var.set(precio)
        self.costo_var.set(costo)
        self.existencia_var.set(existencia)
        self.reorden_var.set(reorden)
        self.cat_var.set(idc)
        self.prov_var.set(idp)
        self.und_var.set(idu)

    # --------------------------------------------------
    # Funciones para la sección DERECHA
    # --------------------------------------------------
    def nuevo_articulo(self):
        """Limpia el formulario para un nuevo registro."""
        for var in [
            self.codigo_var, self.nombre_var, self.precio_var, self.costo_var,
            self.existencia_var, self.reorden_var, self.cat_var,
            self.prov_var, self.und_var
        ]:
            var.set("")

    def guardar_articulo(self):
        # Obtener valores
        codigo = self.codigo_var.get().strip()
        nombre = self.nombre_var.get().strip()
        precio = self.precio_var.get().strip()
        costo = self.costo_var.get().strip()
        existencia = self.existencia_var.get().strip()
        reorden = self.reorden_var.get().strip()
        idc = self.cat_var.get().strip()
        idp = self.prov_var.get().strip()
        idu = self.und_var.get().strip()

        # Validaciones básicas
        if not codigo or not nombre:
            messagebox.showwarning("Validación", "Código y Nombre son obligatorios.")
            return
        # Insert o Update
        self.cursor.execute("SELECT 1 FROM Articulo WHERE codigo = %s", (codigo,))
        if self.cursor.fetchone():
            sql = (
                "UPDATE Articulo SET nombre=%s, precio=%s, costo=%s, existencia=%s, "
                "reorden=%s, id_categoria=%s, id_proveedor=%s, id_unidad=%s WHERE codigo=%s"
            )
            params = (nombre, precio, costo, existencia, reorden, idc, idp, idu, codigo)
            msg = "Artículo actualizado correctamente."
        else:
            sql = (
                "INSERT INTO Articulo (codigo, nombre, precio, costo, existencia, reorden, "
                "id_categoria, id_proveedor, id_unidad) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            )
            params = (codigo, nombre, precio, costo, existencia, reorden, idc, idp, idu)
            msg = "Artículo insertado correctamente."
        try:
            self.cursor.execute(sql, params)
            self.db.commit()
            messagebox.showinfo("Éxito", msg)
            self.nuevo_articulo()
            self.cargar_lista_articulos()
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    def eliminar_articulo(self):
        codigo = self.codigo_var.get().strip()
        if not codigo:
            messagebox.showwarning("Validación", "No hay Código para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar artículo {codigo}?"):
            return
        try:
            self.cursor.execute("DELETE FROM Articulo WHERE codigo = %s", (codigo,))
            self.db.commit()
            messagebox.showinfo("Éxito", "Artículo eliminado correctamente.")
            self.nuevo_articulo()
            self.cargar_lista_articulos()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))

# Para probar de forma independiente:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Inventario")
    root.state("zoomed")
    InventarioApp(root)
    root.mainloop()
