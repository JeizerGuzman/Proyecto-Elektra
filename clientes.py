import tkinter as tk
from tkinter import ttk, messagebox

class ClienteApp:
    def __init__(self, container):
        """
        container: Frame donde se dibujará la interfaz (desde el menú principal).
        """
        self.container = container
        # Limpia el contenedor para cargar la nueva interfaz
        for widget in self.container.winfo_children():
            widget.destroy()
        self.container.configure(bg="white")
        
        # En lugar de conectarse a una base de datos, usamos una lista para simular los registros.
        self.clientes = [
            {"telefono": "9991234567", "nombre": "Juan Pérez", "direccion": "Calle 1", "rfc": "RFC12345678901"},
            {"telefono": "9987654321", "nombre": "Ana Torres", "direccion": "Avenida X", "rfc": "RFCABCDEFGHIJKL"}
        ]
        
        # -------------------------------------------
        # Título "CLIENTES"
        # -------------------------------------------
        title_frame = tk.Frame(self.container, bg="#ECECEC", height=40, padx=10, pady=5)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        lbl_title = tk.Label(title_frame, text="CLIENTES", font=("Helvetica", 14, "bold"), bg="#ECECEC")
        lbl_title.pack(side=tk.LEFT)
        
        # -------------------------------------------
        # Frame principal (dividido en dos secciones)
        # -------------------------------------------
        main_frame = tk.Frame(self.container, bg="white")
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Sección Izquierda (1/3): Búsqueda y lista de clientes
        left_frame = tk.Frame(main_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 1) Barra de búsqueda (por teléfono)
        search_frame = tk.Frame(left_frame, bg="white", padx=10, pady=10)
        search_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(search_frame, text="Buscar Teléfono:", font=("Helvetica", 10), bg="white")\
            .pack(side=tk.LEFT)
        self.buscar_var = tk.StringVar()
        entry_buscar = tk.Entry(search_frame, textvariable=self.buscar_var, width=15, font=("Helvetica", 10))
        entry_buscar.pack(side=tk.LEFT, padx=5)
        btn_buscar = tk.Button(search_frame, text="Buscar", font=("Helvetica", 9, "bold"), bg="#A9A9A9",
                               command=self.buscar_cliente)
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        # 2) Treeview (muestra Teléfono y Nombre, con el Nombre centrado)
        self.tree = ttk.Treeview(left_frame, columns=("telefono", "nombre"), show="headings", height=20)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.heading("telefono", text="Teléfono", anchor="center")
        self.tree.heading("nombre", text="Nombre", anchor="center")
        self.tree.column("telefono", width=100, anchor="center")
        self.tree.column("nombre", width=200, anchor="center")
        scroll_y = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        scroll_y.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_cliente_lista)
        
        # Sección Derecha (2/3): Botones y formulario de clientes
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame para botones (Nuevo, Eliminar, Guardar)
        btn_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        btn_right_frame.pack(side=tk.TOP, fill=tk.X)
        btn_nuevo = tk.Button(btn_right_frame, text="Nuevo Cliente", font=("Helvetica", 10, "bold"), bg="#87CEEB", fg="white",
                              width=12, command=self.nuevo_cliente)
        btn_nuevo.pack(side=tk.LEFT, padx=5)
        btn_eliminar = tk.Button(btn_right_frame, text="Eliminar", font=("Helvetica", 10, "bold"), bg="red", fg="white",
                                 width=8, command=self.eliminar_cliente)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        btn_guardar = tk.Button(btn_right_frame, text="Guardar", font=("Helvetica", 10, "bold"), bg="green", fg="white",
                                width=8, command=self.guardar_cliente)
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        # Frame del formulario
        form_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        form_right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Variables del formulario
        self.telefono_var = tk.StringVar()
        self.nombre_var = tk.StringVar()   # Nombre(s)
        self.apellido_var = tk.StringVar()  # Apellido(s)
        self.direccion_var = tk.StringVar()
        self.rfc_var = tk.StringVar()
        
        # Etiquetas y entradas (dispuestas en grid)
        tk.Label(form_right_frame, text="Teléfono (10 dígitos):", font=("Helvetica", 10), bg="white")\
            .grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.telefono_entry = tk.Entry(form_right_frame, textvariable=self.telefono_var, width=25, font=("Helvetica", 10))
        self.telefono_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_right_frame, text="Nombre(s):", font=("Helvetica", 10), bg="white")\
            .grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.nombre_entry = tk.Entry(form_right_frame, textvariable=self.nombre_var, width=25, font=("Helvetica", 10))
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_right_frame, text="Apellido(s):", font=("Helvetica", 10), bg="white")\
            .grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.apellido_entry = tk.Entry(form_right_frame, textvariable=self.apellido_var, width=25, font=("Helvetica", 10))
        self.apellido_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_right_frame, text="Dirección:", font=("Helvetica", 10), bg="white")\
            .grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        self.direccion_entry = tk.Entry(form_right_frame, textvariable=self.direccion_var, width=25, font=("Helvetica", 10))
        self.direccion_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(form_right_frame, text="RFC:", font=("Helvetica", 10), bg="white")\
            .grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
        self.rfc_entry = tk.Entry(form_right_frame, textvariable=self.rfc_var, width=25, font=("Helvetica", 10))
        self.rfc_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Carga la lista de clientes en el Treeview de la sección izquierda
        self.cargar_lista_clientes()
    
    # --------------------------------------------------
    # Funciones para la sección IZQUIERDA
    # --------------------------------------------------
    def cargar_lista_clientes(self, filtro=""):
        """Carga en el Treeview (izquierdo) los clientes existentes. Si 'filtro' no está vacío, filtra por teléfono."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Simulación: Filtrar la lista interna
        for cliente in self.clientes:
            if filtro:
                if filtro not in cliente["telefono"]:
                    continue
            telefono = cliente["telefono"]
            nombreCompleto = cliente["nombre"]
            self.tree.insert("", tk.END, values=(telefono, nombreCompleto))
    
    def buscar_cliente(self):
        """Filtra los clientes por teléfono usando el valor del Entry de búsqueda."""
        filtro = self.buscar_var.get().strip()
        self.cargar_lista_clientes(filtro)
    
    def seleccionar_cliente_lista(self, event):
        """Cuando se selecciona un cliente en el Treeview de la izquierda, carga sus datos en el formulario de la derecha."""
        item = self.tree.focus()
        if not item:
            return
        valores = self.tree.item(item, "values")  # (telefono, nombreCompleto)
        if valores:
            telefono, _ = valores
            self.cargar_datos_cliente(telefono)
    
    # --------------------------------------------------
    # Funciones para la sección DERECHA
    # --------------------------------------------------
    def nuevo_cliente(self):
        """Limpia el formulario de la sección derecha para agregar un nuevo cliente."""
        self.limpiar_formulario()
    
    def guardar_cliente(self):
        """
        Inserta o actualiza el cliente según si existe o no el teléfono en el 'registro' simulado.
        Se unen nombre y apellido para guardarlo en la clave 'nombre'.
        """
        telefono = self.telefono_var.get().strip()
        nombre = self.nombre_var.get().strip()
        apellido = self.apellido_var.get().strip()
        direccion = self.direccion_var.get().strip()
        rfc = self.rfc_var.get().strip().upper()
        
        # Validaciones básicas
        if len(telefono) != 10 or not telefono.isdigit():
            messagebox.showwarning("Validación", "El teléfono debe tener 10 dígitos numéricos.")
            return
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return
        if len(rfc) != 13:
            messagebox.showwarning("Validación", "El RFC debe tener 13 caracteres.")
            return
        
        nombreCompleto = f"{nombre} {apellido}".strip()
        # Verificamos si el cliente ya existe (por teléfono)
        existe = False
        for cliente in self.clientes:
            if cliente["telefono"] == telefono:
                # Actualizar
                cliente["nombre"] = nombreCompleto
                cliente["direccion"] = direccion
                cliente["rfc"] = rfc
                existe = True
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
                break
        if not existe:
            # Insertar nuevo
            self.clientes.append({
                "telefono": telefono,
                "nombre": nombreCompleto,
                "direccion": direccion,
                "rfc": rfc
            })
            messagebox.showinfo("Éxito", "Cliente insertado correctamente.")
        self.limpiar_formulario()
        self.cargar_lista_clientes()
    
    def eliminar_cliente(self):
        """Elimina el cliente cuyo teléfono se muestra en el formulario de la sección derecha."""
        telefono = self.telefono_var.get().strip()
        if not telefono:
            messagebox.showwarning("Validación", "No hay teléfono para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar al cliente con teléfono {telefono}?"):
            return
        eliminado = False
        for i, cliente in enumerate(self.clientes):
            if cliente["telefono"] == telefono:
                del self.clientes[i]
                eliminado = True
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                break
        if not eliminado:
            messagebox.showerror("Error", "No se encontró el cliente para eliminar.")
        self.limpiar_formulario()
        self.cargar_lista_clientes()
    
    def cargar_datos_cliente(self, telefono):
        """Carga los datos completos de un cliente en el formulario de la sección derecha."""
        for cliente in self.clientes:
            if cliente["telefono"] == telefono:
                nombreCompleto = cliente["nombre"].strip()
                partes = nombreCompleto.split(" ", 1)
                if len(partes) == 2:
                    nombre, apellido = partes
                else:
                    nombre = partes[0]
                    apellido = ""
                self.telefono_var.set(cliente["telefono"])
                self.nombre_var.set(nombre)
                self.apellido_var.set(apellido)
                self.direccion_var.set(cliente["direccion"])
                self.rfc_var.set(cliente["rfc"].upper())
                break
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario de la sección derecha."""
        self.telefono_var.set("")
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.direccion_var.set("")
        self.rfc_var.set("")

# Para probar de forma independiente:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Clientes")
    root.state("zoomed")
    ClienteApp(root)
    root.mainloop()
