import tkinter as tk
from tkinter import ttk, messagebox

class ProveedorApp:
    def __init__(self, container):
        """
        container: Frame donde se dibujará la interfaz (desde el menú principal).
        """
        self.container = container
        # Limpia el contenedor para cargar la nueva interfaz
        for widget in self.container.winfo_children():
            widget.destroy()
        self.container.configure(bg="white")
        
        # Simulación: registros de proveedores (sin conexión a BD)
        # Cada proveedor tiene: id, empresa, representante y teléfono.
        self.proveedores = [
            {"id": "P001", "empresa": "Empresa A", "representante": "Representante A", "telefono": "9991234567"},
            {"id": "P002", "empresa": "Empresa B", "representante": "Representante B", "telefono": "9987654321"}
        ]
        
        # -------------------------------------------
        # Título "PROVEEDORES"
        # -------------------------------------------
        title_frame = tk.Frame(self.container, bg="#ECECEC", height=40, padx=10, pady=5)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        lbl_title = tk.Label(title_frame, text="PROVEEDORES", font=("Helvetica", 14, "bold"), bg="#ECECEC")
        lbl_title.pack(side=tk.LEFT)
        
        # -------------------------------------------
        # Frame principal (dividido en dos secciones)
        # -------------------------------------------
        main_frame = tk.Frame(self.container, bg="white")
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Sección Izquierda (1/3): Búsqueda y lista de proveedores
        left_frame = tk.Frame(main_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 1) Barra de búsqueda (por ID de proveedor)
        search_frame = tk.Frame(left_frame, bg="white", padx=10, pady=10)
        search_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(search_frame, text="Buscar ID Proveedor:", font=("Helvetica", 10), bg="white")\
            .pack(side=tk.LEFT)
        self.buscar_var = tk.StringVar()
        entry_buscar = tk.Entry(search_frame, textvariable=self.buscar_var, width=15, font=("Helvetica", 10))
        entry_buscar.pack(side=tk.LEFT, padx=5)
        btn_buscar = tk.Button(search_frame, text="Buscar", font=("Helvetica", 9, "bold"), bg="#A9A9A9",
                               command=self.buscar_proveedor)
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        # 2) Treeview (muestra ID, Empresa y Representante)
        self.tree = ttk.Treeview(left_frame, columns=("id", "empresa", "representante"), show="headings", height=20)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.heading("id", text="ID Proveedor", anchor="center")
        self.tree.heading("empresa", text="Empresa", anchor="center")
        self.tree.heading("representante", text="Representante", anchor="center")
        self.tree.column("id", width=100, anchor="center")
        self.tree.column("empresa", width=200, anchor="center")
        self.tree.column("representante", width=200, anchor="center")
        scroll_y = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        scroll_y.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_proveedor_lista)
        
        # Sección Derecha (2/3): Botones y formulario de proveedores
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame para botones (Nuevo, Eliminar, Guardar)
        btn_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        btn_right_frame.pack(side=tk.TOP, fill=tk.X)
        btn_nuevo = tk.Button(btn_right_frame, text="Nuevo Proveedor", font=("Helvetica", 10, "bold"), bg="#87CEEB", fg="white",
                              width=15, command=self.nuevo_proveedor)
        btn_nuevo.pack(side=tk.LEFT, padx=5)
        btn_eliminar = tk.Button(btn_right_frame, text="Eliminar", font=("Helvetica", 10, "bold"), bg="red", fg="white",
                                 width=8, command=self.eliminar_proveedor)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        btn_guardar = tk.Button(btn_right_frame, text="Guardar", font=("Helvetica", 10, "bold"), bg="green", fg="white",
                                width=8, command=self.guardar_proveedor)
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        # Frame del formulario
        form_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        form_right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Variables del formulario
        self.telefono_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.empresa_var = tk.StringVar()
        self.representante_var = tk.StringVar()
        
        # Etiquetas y entradas (dispuestas en grid)
        tk.Label(form_right_frame, text="Teléfono (10 dígitos):", font=("Helvetica", 10), bg="white")\
            .grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.telefono_entry = tk.Entry(form_right_frame, textvariable=self.telefono_var, width=25, font=("Helvetica", 10))
        self.telefono_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_right_frame, text="ID Proveedor:", font=("Helvetica", 10), bg="white")\
            .grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.id_entry = tk.Entry(form_right_frame, textvariable=self.id_var, width=25, font=("Helvetica", 10))
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_right_frame, text="Empresa:", font=("Helvetica", 10), bg="white")\
            .grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.empresa_entry = tk.Entry(form_right_frame, textvariable=self.empresa_var, width=25, font=("Helvetica", 10))
        self.empresa_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_right_frame, text="Representante:", font=("Helvetica", 10), bg="white")\
            .grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        self.representante_entry = tk.Entry(form_right_frame, textvariable=self.representante_var, width=25, font=("Helvetica", 10))
        self.representante_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Carga la lista de proveedores en el Treeview de la sección izquierda
        self.cargar_lista_proveedores()
    
    # --------------------------------------------------
    # Funciones para la sección IZQUIERDA
    # --------------------------------------------------
    def cargar_lista_proveedores(self, filtro=""):
        """Carga en el Treeview (izquierdo) los proveedores existentes.
        Si 'filtro' no está vacío, filtra por el ID del proveedor."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for proveedor in self.proveedores:
            if filtro:
                if filtro not in proveedor["id"]:
                    continue
            # Se muestran en la tabla: id, empresa y representante
            self.tree.insert("", tk.END, values=(proveedor["id"],
                                                 proveedor["empresa"],
                                                 proveedor["representante"]))
    
    def buscar_proveedor(self):
        """Filtra los proveedores por el ID usando el valor del Entry de búsqueda."""
        filtro = self.buscar_var.get().strip()
        self.cargar_lista_proveedores(filtro)
    
    def seleccionar_proveedor_lista(self, event):
        """Cuando se selecciona un proveedor en el Treeview de la izquierda,
        carga sus datos en el formulario de la sección derecha."""
        item = self.tree.focus()
        if not item:
            return
        valores = self.tree.item(item, "values")  # (id, empresa, representante)
        if valores:
            id_prov, _, _ = valores
            self.cargar_datos_proveedor(id_prov)
    
    # --------------------------------------------------
    # Funciones para la sección DERECHA
    # --------------------------------------------------
    def nuevo_proveedor(self):
        """Limpia el formulario de la sección derecha para agregar un nuevo proveedor."""
        self.limpiar_formulario()
    
    def guardar_proveedor(self):
        """
        Inserta o actualiza el proveedor en el registro simulado.
        Se almacenan en la lista self.proveedores y se compara por ID.
        """
        telefono = self.telefono_var.get().strip()
        id_prov = self.id_var.get().strip()
        empresa = self.empresa_var.get().strip()
        representante = self.representante_var.get().strip()
        
        # Validaciones básicas
        if len(telefono) != 10 or not telefono.isdigit():
            messagebox.showwarning("Validación", "El teléfono debe tener 10 dígitos numéricos.")
            return
        if not id_prov:
            messagebox.showwarning("Validación", "El ID del proveedor es obligatorio.")
            return
        if not empresa:
            messagebox.showwarning("Validación", "El nombre de la empresa es obligatorio.")
            return
        if not representante:
            messagebox.showwarning("Validación", "El nombre del representante es obligatorio.")
            return
        
        existe = False
        for proveedor in self.proveedores:
            if proveedor["id"] == id_prov:
                # Actualizar
                proveedor["telefono"] = telefono
                proveedor["empresa"] = empresa
                proveedor["representante"] = representante
                existe = True
                messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
                break
        if not existe:
            # Insertar nuevo proveedor
            self.proveedores.append({
                "id": id_prov,
                "telefono": telefono,
                "empresa": empresa,
                "representante": representante
            })
            messagebox.showinfo("Éxito", "Proveedor insertado correctamente.")
        self.limpiar_formulario()
        self.cargar_lista_proveedores()
    
    def eliminar_proveedor(self):
        """Elimina el proveedor cuyo ID se muestra en el formulario de la sección derecha."""
        id_prov = self.id_var.get().strip()
        if not id_prov:
            messagebox.showwarning("Validación", "No hay ID para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar al proveedor con ID {id_prov}?"):
            return
        eliminado = False
        for i, proveedor in enumerate(self.proveedores):
            if proveedor["id"] == id_prov:
                del self.proveedores[i]
                eliminado = True
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
                break
        if not eliminado:
            messagebox.showerror("Error", "No se encontró el proveedor para eliminar.")
        self.limpiar_formulario()
        self.cargar_lista_proveedores()
    
    def cargar_datos_proveedor(self, id_prov):
        """Carga los datos completos de un proveedor en el formulario de la sección derecha."""
        for proveedor in self.proveedores:
            if proveedor["id"] == id_prov:
                self.telefono_var.set(proveedor["telefono"])
                self.id_var.set(proveedor["id"])
                self.empresa_var.set(proveedor["empresa"])
                self.representante_var.set(proveedor["representante"])
                break
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario de la sección derecha."""
        self.telefono_var.set("")
        self.id_var.set("")
        self.empresa_var.set("")
        self.representante_var.set("")

# Para probar de forma independiente:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Proveedores")
    root.state("zoomed")
    ProveedorApp(root)
    root.mainloop()
