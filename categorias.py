import tkinter as tk
from tkinter import ttk, messagebox

class CategoriaApp:
    def __init__(self, container):
        """
        container: Frame donde se dibujará la interfaz (desde el menú principal).
        """
        self.container = container
        # Limpia el contenedor para cargar la nueva interfaz
        for widget in self.container.winfo_children():
            widget.destroy()
        self.container.configure(bg="white")
        
        # Simulación: registros de categorías (sin conexión a BD)
        # Cada categoría tendrá: id y nombre.
        self.categorias = [
            {"id": "C001", "nombre": "Electrónica"},
            {"id": "C002", "nombre": "Ropa"},
            {"id": "C003", "nombre": "Alimentos"}
        ]
        
        # -------------------------------------------
        # Título "CATEGORÍAS"
        # -------------------------------------------

        
        # -------------------------------------------
        # Frame principal (dividido en dos secciones)
        # -------------------------------------------
        main_frame = tk.Frame(self.container, bg="white")
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Sección Izquierda (para búsqueda y lista de categorías)
        left_frame = tk.Frame(main_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 1) Barra de búsqueda (por ID de categoría)
        search_frame = tk.Frame(left_frame, bg="white", padx=10, pady=10)
        search_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(search_frame, text="Buscar ID Categoría:", font=("Helvetica", 10), bg="white")\
            .pack(side=tk.LEFT)
        self.buscar_var = tk.StringVar()
        entry_buscar = tk.Entry(search_frame, textvariable=self.buscar_var, width=15, font=("Helvetica", 10))
        entry_buscar.pack(side=tk.LEFT, padx=5)
        btn_buscar = tk.Button(search_frame, text="Buscar", font=("Helvetica", 9, "bold"), bg="#A9A9A9",
                               command=self.buscar_categoria)
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        # 2) Treeview (muestra ID y Nombre de la categoría)
        self.tree = ttk.Treeview(left_frame, columns=("id", "nombre"), show="headings", height=20)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.heading("id", text="ID Categoría", anchor="center")
        self.tree.heading("nombre", text="Nombre", anchor="center")
        self.tree.column("id", width=120, anchor="center")
        self.tree.column("nombre", width=200, anchor="center")
        scroll_y = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        scroll_y.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_categoria_lista)
        
        # Sección Derecha (formulario y botones)
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame para botones (Nuevo, Eliminar, Guardar)
        btn_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        btn_right_frame.pack(side=tk.TOP, fill=tk.X)
        btn_nuevo = tk.Button(btn_right_frame, text="Nueva Categoría", font=("Helvetica", 10, "bold"),
                              bg="#87CEEB", fg="white", width=15, command=self.nueva_categoria)
        btn_nuevo.pack(side=tk.LEFT, padx=5)
        btn_eliminar = tk.Button(btn_right_frame, text="Eliminar", font=("Helvetica", 10, "bold"),
                                 bg="red", fg="white", width=8, command=self.eliminar_categoria)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        btn_guardar = tk.Button(btn_right_frame, text="Guardar", font=("Helvetica", 10, "bold"),
                                bg="green", fg="white", width=8, command=self.guardar_categoria)
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        # Frame del formulario
        form_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        form_right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Variables del formulario
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        
        # Etiquetas y entradas (dispuestas en grid)
        tk.Label(form_right_frame, text="ID Categoría:", font=("Helvetica", 10), bg="white")\
            .grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.id_entry = tk.Entry(form_right_frame, textvariable=self.id_var, width=25, font=("Helvetica", 10))
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_right_frame, text="Nombre Categoría:", font=("Helvetica", 10), bg="white")\
            .grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.nombre_entry = tk.Entry(form_right_frame, textvariable=self.nombre_var, width=25, font=("Helvetica", 10))
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Carga la lista de categorías en el Treeview de la sección izquierda
        self.cargar_lista_categorias()
    
    # --------------------------------------------------
    # Funciones para la sección IZQUIERDA
    # --------------------------------------------------
    def cargar_lista_categorias(self, filtro=""):
        """Carga en el Treeview (izquierdo) las categorías existentes.
        Si 'filtro' no está vacío, filtra por el ID de la categoría."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for categoria in self.categorias:
            if filtro:
                if filtro not in categoria["id"]:
                    continue
            self.tree.insert("", tk.END, values=(categoria["id"], categoria["nombre"]))
    
    def buscar_categoria(self):
        """Filtra las categorías por el ID usando el valor del Entry de búsqueda."""
        filtro = self.buscar_var.get().strip()
        self.cargar_lista_categorias(filtro)
    
    def seleccionar_categoria_lista(self, event):
        """Cuando se selecciona una categoría en el Treeview, carga sus datos en el formulario."""
        item = self.tree.focus()
        if not item:
            return
        valores = self.tree.item(item, "values")  # (id, nombre)
        if valores:
            id_cat, _ = valores
            self.cargar_datos_categoria(id_cat)
    
    # --------------------------------------------------
    # Funciones para la sección DERECHA
    # --------------------------------------------------
    def nueva_categoria(self):
        """Limpia el formulario para agregar una nueva categoría."""
        self.limpiar_formulario()
    
    def guardar_categoria(self):
        """
        Inserta o actualiza la categoría en el registro simulado.
        Se compara por ID.
        """
        id_cat = self.id_var.get().strip()
        nombre = self.nombre_var.get().strip()
        
        # Validaciones básicas
        if not id_cat:
            messagebox.showwarning("Validación", "El ID de la categoría es obligatorio.")
            return
        if not nombre:
            messagebox.showwarning("Validación", "El nombre de la categoría es obligatorio.")
            return
        
        existe = False
        for categoria in self.categorias:
            if categoria["id"] == id_cat:
                # Actualizar
                categoria["nombre"] = nombre
                existe = True
                messagebox.showinfo("Éxito", "Categoría actualizada correctamente.")
                break
        if not existe:
            # Insertar nueva categoría
            self.categorias.append({
                "id": id_cat,
                "nombre": nombre
            })
            messagebox.showinfo("Éxito", "Categoría insertada correctamente.")
        self.limpiar_formulario()
        self.cargar_lista_categorias()
    
    def eliminar_categoria(self):
        """Elimina la categoría cuyo ID se muestra en el formulario."""
        id_cat = self.id_var.get().strip()
        if not id_cat:
            messagebox.showwarning("Validación", "No hay ID para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la categoría con ID {id_cat}?"):
            return
        eliminado = False
        for i, categoria in enumerate(self.categorias):
            if categoria["id"] == id_cat:
                del self.categorias[i]
                eliminado = True
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente.")
                break
        if not eliminado:
            messagebox.showerror("Error", "No se encontró la categoría para eliminar.")
        self.limpiar_formulario()
        self.cargar_lista_categorias()
    
    def cargar_datos_categoria(self, id_cat):
        """Carga los datos de una categoría en el formulario."""
        for categoria in self.categorias:
            if categoria["id"] == id_cat:
                self.id_var.set(categoria["id"])
                self.nombre_var.set(categoria["nombre"])
                break
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.id_var.set("")
        self.nombre_var.set("")

# Para probar de forma independiente:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Categorías")
    root.state("zoomed")
    CategoriaApp(root)
    root.mainloop()
