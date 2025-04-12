import tkinter as tk
from tkinter import ttk, messagebox

class UnidadApp:
    def __init__(self, container):
        """
        container: Frame donde se dibujará la interfaz (desde el menú principal).
        """
        self.container = container
        # Limpiar el contenedor para cargar la nueva interfaz
        for widget in self.container.winfo_children():
            widget.destroy()
        self.container.configure(bg="white")
        
        # Simulación: registros de unidades (sin conexión a BD)
        # Cada unidad tendrá: id y nombre.
        self.unidades = [
            {"id": "M001", "nombre": "Kilogramo"},
            {"id": "M002", "nombre": "Litro"},
            {"id": "M003", "nombre": "Unidad"}
        ]
        
        # -------------------------------------------
        # Título "UNIDADES"
        # -------------------------------------------

        
        # -------------------------------------------
        # Frame principal (dividido en dos secciones)
        # -------------------------------------------
        main_frame = tk.Frame(self.container, bg="white")
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Sección Izquierda: Búsqueda y lista de unidades
        left_frame = tk.Frame(main_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 1) Barra de búsqueda (por ID Unidad)
        search_frame = tk.Frame(left_frame, bg="white", padx=10, pady=10)
        search_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(search_frame, text="Buscar ID Unidad:", font=("Helvetica", 10), bg="white")\
            .pack(side=tk.LEFT)
        self.buscar_var = tk.StringVar()
        entry_buscar = tk.Entry(search_frame, textvariable=self.buscar_var, width=15, font=("Helvetica", 10))
        entry_buscar.pack(side=tk.LEFT, padx=5)
        btn_buscar = tk.Button(search_frame, text="Buscar", font=("Helvetica", 9, "bold"), bg="#A9A9A9",
                               command=self.buscar_unidad)
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        # 2) Treeview (muestra ID y Nombre de la unidad)
        self.tree = ttk.Treeview(left_frame, columns=("id", "nombre"), show="headings", height=20)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.heading("id", text="ID Unidad", anchor="center")
        self.tree.heading("nombre", text="Nombre", anchor="center")
        self.tree.column("id", width=120, anchor="center")
        self.tree.column("nombre", width=200, anchor="center")
        scroll_y = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        scroll_y.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_unidad_lista)
        
        # Sección Derecha: Formulario y botones
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame para botones (Nuevo, Eliminar, Guardar)
        btn_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        btn_right_frame.pack(side=tk.TOP, fill=tk.X)
        btn_nuevo = tk.Button(btn_right_frame, text="Nueva Unidad", font=("Helvetica", 10, "bold"),
                              bg="#87CEEB", fg="white", width=15, command=self.nueva_unidad)
        btn_nuevo.pack(side=tk.LEFT, padx=5)
        btn_eliminar = tk.Button(btn_right_frame, text="Eliminar", font=("Helvetica", 10, "bold"),
                                 bg="red", fg="white", width=8, command=self.eliminar_unidad)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        btn_guardar = tk.Button(btn_right_frame, text="Guardar", font=("Helvetica", 10, "bold"),
                                bg="green", fg="white", width=8, command=self.guardar_unidad)
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        # Frame del formulario
        form_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        form_right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Variables del formulario
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        
        # Etiquetas y entradas (dispuestas en grid)
        tk.Label(form_right_frame, text="ID Unidad:", font=("Helvetica", 10), bg="white")\
            .grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.id_entry = tk.Entry(form_right_frame, textvariable=self.id_var, width=25, font=("Helvetica", 10))
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_right_frame, text="Nombre:", font=("Helvetica", 10), bg="white")\
            .grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.nombre_entry = tk.Entry(form_right_frame, textvariable=self.nombre_var, width=25, font=("Helvetica", 10))
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Cargar la lista de unidades en el Treeview
        self.cargar_lista_unidades()
    
    # --------------------------------------------------
    # Funciones para la sección IZQUIERDA
    # --------------------------------------------------
    def cargar_lista_unidades(self, filtro=""):
        """Carga en el Treeview las unidades existentes.
        Si 'filtro' no está vacío, filtra por el ID de la unidad."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for unidad in self.unidades:
            if filtro:
                if filtro not in unidad["id"]:
                    continue
            self.tree.insert("", tk.END, values=(unidad["id"], unidad["nombre"]))
    
    def buscar_unidad(self):
        """Filtra las unidades por el ID usando el valor del Entry de búsqueda."""
        filtro = self.buscar_var.get().strip()
        self.cargar_lista_unidades(filtro)
    
    def seleccionar_unidad_lista(self, event):
        """Carga los datos de la unidad seleccionada en el formulario."""
        item = self.tree.focus()
        if not item:
            return
        valores = self.tree.item(item, "values")
        if valores:
            id_uni, _ = valores
            self.cargar_datos_unidad(id_uni)
    
    # --------------------------------------------------
    # Funciones para la sección DERECHA
    # --------------------------------------------------
    def nueva_unidad(self):
        """Limpia el formulario para agregar una nueva unidad."""
        self.limpiar_formulario()
    
    def guardar_unidad(self):
        """
        Inserta o actualiza la unidad en el registro simulado.
        Se compara por ID.
        """
        id_uni = self.id_var.get().strip()
        nombre = self.nombre_var.get().strip()
        
        # Validaciones básicas
        if not id_uni:
            messagebox.showwarning("Validación", "El ID de la unidad es obligatorio.")
            return
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return
        
        existe = False
        for unidad in self.unidades:
            if unidad["id"] == id_uni:
                # Actualizar
                unidad["nombre"] = nombre
                existe = True
                messagebox.showinfo("Éxito", "Unidad actualizada correctamente.")
                break
        if not existe:
            # Insertar nueva unidad
            self.unidades.append({
                "id": id_uni,
                "nombre": nombre
            })
            messagebox.showinfo("Éxito", "Unidad insertada correctamente.")
        self.limpiar_formulario()
        self.cargar_lista_unidades()
    
    def eliminar_unidad(self):
        """Elimina la unidad cuyo ID se muestra en el formulario."""
        id_uni = self.id_var.get().strip()
        if not id_uni:
            messagebox.showwarning("Validación", "No hay ID para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la unidad con ID {id_uni}?"):
            return
        eliminado = False
        for i, unidad in enumerate(self.unidades):
            if unidad["id"] == id_uni:
                del self.unidades[i]
                eliminado = True
                messagebox.showinfo("Éxito", "Unidad eliminada correctamente.")
                break
        if not eliminado:
            messagebox.showerror("Error", "No se encontró la unidad para eliminar.")
        self.limpiar_formulario()
        self.cargar_lista_unidades()
    
    def cargar_datos_unidad(self, id_uni):
        """Carga los datos de una unidad en el formulario."""
        for unidad in self.unidades:
            if unidad["id"] == id_uni:
                self.id_var.set(unidad["id"])
                self.nombre_var.set(unidad["nombre"])
                break
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.id_var.set("")
        self.nombre_var.set("")

# Para probar de forma independiente:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Unidades")
    root.state("zoomed")
    UnidadApp(root)
    root.mainloop()

    