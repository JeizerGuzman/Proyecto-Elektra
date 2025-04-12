import tkinter as tk
from tkinter import ttk, messagebox
from categorias import CategoriaApp
from unidades import UnidadApp

class ConfiguracionesApp:
    def __init__(self, container):
        """
        container: Frame/ventana donde se dibujará la ventana de Configuraciones (desde tu menú principal).
        """
        self.container = container
        # Limpiamos cualquier contenido anterior
        for widget in self.container.winfo_children():
            widget.destroy()
        self.container.configure(bg="white")

        # -------------------------------
        # Cabecera "CONFIGURACIONES"
        # -------------------------------
        title_frame = tk.Frame(self.container, bg="#ECECEC", height=40, padx=10, pady=5)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        lbl_title = tk.Label(title_frame, text="CONFIGURACIONES", font=("Helvetica", 14, "bold"), bg="#ECECEC")
        lbl_title.pack(side=tk.LEFT)

        # -------------------------------
        # División principal:
        #   - Parte superior: Barra de navegación horizontal
        #   - Parte inferior: Frame contenedor de la vista
        # -------------------------------
        main_frame = tk.Frame(self.container, bg="white")
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Barra de navegación horizontal
        navbar = tk.Frame(main_frame, bg="#F0F0F0", height=40)
        navbar.pack(side=tk.TOP, fill=tk.X)
        btn_usuarios = tk.Button(navbar, text="Usuarios", font=("Helvetica", 10, "bold"), width=15,
                                 command=self.on_usuarios)
        btn_usuarios.pack(side=tk.LEFT, padx=5, pady=5)
        btn_categorias = tk.Button(navbar, text="Categorías", font=("Helvetica", 10, "bold"), width=15,
                                   command=self.on_categorias)
        btn_categorias.pack(side=tk.LEFT, padx=5, pady=5)
        btn_unidades = tk.Button(navbar, text="Unidades de Medida", font=("Helvetica", 10, "bold"), width=18,
                                 command=self.on_unidades)
        btn_unidades.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame contenedor donde se cargarán las vistas
        self.frame_contenedor = tk.Frame(main_frame, bg="white")
        self.frame_contenedor.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Por defecto, carga la vista de "Usuarios"
        self.on_usuarios()

    def _limpiar_contenedor(self):
        """Elimina todos los widgets dentro del frame_contenedor."""
        for widget in self.frame_contenedor.winfo_children():
            widget.destroy()

    def on_usuarios(self):
        self._limpiar_contenedor()
        UsuarioApp(self.frame_contenedor)

    def on_categorias(self):
        self._limpiar_contenedor()
        CategoriaApp(self.frame_contenedor)

    def on_unidades(self):
        self._limpiar_contenedor()
        UnidadApp(self.frame_contenedor)


class UsuarioApp:
    """
    Diseño similar a ProveedorApp, pero para 'Usuarios'.
    La tabla muestra: (id, departamento, nombre)
    El formulario maneja: id usuario, nombre, departamento, teléfono, contraseña, hora entrada y hora salida (con combobox AM/PM).
    """
    def __init__(self, container):
        self.container = container
        # Datos simulados de usuarios
        self.usuarios = [
            {"id": "U001", "nombre": "Jeizer Guzman", "departamento": "Administrador", "telefono": "9161579322",
             "contraseña": "7", "hora_entrada": "08:00 AM", "hora_salida": "04:00 PM"},
            {"id": "U002", "nombre": "Alejandro Gutierrez", "departamento": "Gerencia", "telefono": "9987654321",
             "contraseña": "4", "hora_entrada": "09:00 AM", "hora_salida": "05:00 PM"}
        ]

        # Limpiar contenedor e iniciar interfaz
        for widget in self.container.winfo_children():
            widget.destroy()

        # Frame principal (dos secciones)
        main_frame = tk.Frame(self.container, bg="white")
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Sección Izquierda: Búsqueda + tabla
        left_frame = tk.Frame(main_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de búsqueda (por ID)
        search_frame = tk.Frame(left_frame, bg="white", padx=10, pady=10)
        search_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(search_frame, text="Buscar ID Usuario:", font=("Helvetica", 10), bg="white")\
            .pack(side=tk.LEFT)
        self.buscar_var = tk.StringVar()
        entry_buscar = tk.Entry(search_frame, textvariable=self.buscar_var, width=15, font=("Helvetica", 10))
        entry_buscar.pack(side=tk.LEFT, padx=5)
        btn_buscar = tk.Button(search_frame, text="Buscar", font=("Helvetica", 9, "bold"), bg="#A9A9A9",
                               command=self.buscar_usuario)
        btn_buscar.pack(side=tk.LEFT, padx=5)

        # Treeview (muestra ID, Departamento, Nombre)
        self.tree = ttk.Treeview(left_frame, columns=("id", "departamento", "nombre"), show="headings", height=20)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.heading("id", text="ID Usuario", anchor="center")
        self.tree.heading("departamento", text="Departamento", anchor="center")
        self.tree.heading("nombre", text="Nombre", anchor="center")
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("departamento", width=120, anchor="center")
        self.tree.column("nombre", width=180, anchor="center")
        scroll_y = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        scroll_y.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_usuario_lista)

        # Sección Derecha: Botones + formulario
        right_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame de botones (Nuevo, Eliminar, Guardar)
        btn_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        btn_right_frame.pack(side=tk.TOP, fill=tk.X)
        btn_nuevo = tk.Button(btn_right_frame, text="Nuevo Usuario", font=("Helvetica", 10, "bold"),
                              bg="#87CEEB", fg="white", width=12, command=self.nuevo_usuario)
        btn_nuevo.pack(side=tk.LEFT, padx=5)
        btn_eliminar = tk.Button(btn_right_frame, text="Eliminar", font=("Helvetica", 10, "bold"),
                                 bg="red", fg="white", width=8, command=self.eliminar_usuario)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        btn_guardar = tk.Button(btn_right_frame, text="Guardar", font=("Helvetica", 10, "bold"),
                                bg="green", fg="white", width=8, command=self.guardar_usuario)
        btn_guardar.pack(side=tk.LEFT, padx=5)

        # Formulario (ID, Nombre, Departamento, Teléfono, Contraseña, Hora Entrada, Hora Salida)
        form_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        form_right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.departamento_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.contraseña_var = tk.StringVar()
        self.hora_entrada_var = tk.StringVar()
        self.hora_salida_var = tk.StringVar()

        
        
        # Fila 0: ID
        tk.Label(form_right_frame, text="ID Usuario:", font=("Helvetica", 10), bg="white")\
            .grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Entry(form_right_frame, textvariable=self.id_var, width=25, font=("Helvetica", 10))\
            .grid(row=0, column=1, padx=5, pady=5)
        # Fila 1: Nombre
        tk.Label(form_right_frame, text="Nombre:", font=("Helvetica", 10), bg="white")\
            .grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Entry(form_right_frame, textvariable=self.nombre_var, width=25, font=("Helvetica", 10))\
            .grid(row=1, column=1, padx=5, pady=5)
        # Fila 2: Departamento (combobox)
        tk.Label(form_right_frame, text="Departamento:", font=("Helvetica", 10), bg="white")\
            .grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        departamentos_elektra = ["Administrador", "Gerencia", "Ventas", "Cajas", "Servicio al Cliente",
                                 "Bodega"]
        combo_dept = ttk.Combobox(form_right_frame, textvariable=self.departamento_var,
                                  values=departamentos_elektra, width=22)
        combo_dept.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        # Fila 3: Teléfono
        tk.Label(form_right_frame, text="Teléfono (10 dígitos):", font=("Helvetica", 10), bg="white")\
            .grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Entry(form_right_frame, textvariable=self.telefono_var, width=25, font=("Helvetica", 10))\
            .grid(row=3, column=1, padx=5, pady=5)
        # Fila 4: Contraseña
        tk.Label(form_right_frame, text="Contraseña:", font=("Helvetica", 10), bg="white")\
            .grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
        # Guardamos el Entry en self.entry_contraseña para poder modificarlo
        self.entry_contraseña = tk.Entry(form_right_frame, textvariable=self.contraseña_var, 
                                        width=25, font=("Helvetica", 10), show="*")
        self.entry_contraseña.grid(row=4, column=1, padx=5, pady=5)
        # Fila 5: Hora Entrada con combobox AM/PM
        tk.Label(form_right_frame, text="Hora Entrada:", font=("Helvetica", 10), bg="white")\
            .grid(row=5, column=0, sticky=tk.E, padx=5, pady=5)
        hora_entrada_frame = tk.Frame(form_right_frame, bg="white")
        hora_entrada_frame.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Entry(hora_entrada_frame, textvariable=self.hora_entrada_var, width=10, font=("Helvetica", 10))\
            .pack(side=tk.LEFT)
        self.entrada_meridiano = tk.StringVar(value="AM")
        combo_entrada = ttk.Combobox(hora_entrada_frame, textvariable=self.entrada_meridiano,
                                      values=["AM", "PM"], width=4)
        combo_entrada.pack(side=tk.LEFT, padx=5)
        # Fila 6: Hora Salida con combobox AM/PM
        tk.Label(form_right_frame, text="Hora Salida:", font=("Helvetica", 10), bg="white")\
            .grid(row=6, column=0, sticky=tk.E, padx=5, pady=5)
        hora_salida_frame = tk.Frame(form_right_frame, bg="white")
        hora_salida_frame.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Entry(hora_salida_frame, textvariable=self.hora_salida_var, width=10, font=("Helvetica", 10))\
            .pack(side=tk.LEFT)
        self.salida_meridiano = tk.StringVar(value="PM")
        combo_salida = ttk.Combobox(hora_salida_frame, textvariable=self.salida_meridiano,
                                     values=["AM", "PM"], width=4)
        combo_salida.pack(side=tk.LEFT, padx=5)
 
        # Creamos una variable de control para el Checkbutton
        self.mostrar_contraseña = tk.IntVar(value=0)
        # Creamos el Checkbutton y lo ubicamos (por ejemplo, justo debajo o al lado del Entry)
        check_btn = tk.Checkbutton(form_right_frame, text="Mostrar", variable=self.mostrar_contraseña, 
                                bg="white", command=self.ver_contraseña)
        check_btn.grid(row=4, column=2, padx=5, pady=5)

        # Cargar la lista inicial en el Treeview
        self.cargar_lista_usuarios()



    def ver_contraseña(self):
        if self.mostrar_contraseña.get():
            # Si el check está marcado, se muestra la contraseña (sin enmascarar)
            self.entry_contraseña.config(show="")
        else:
            # Si está desmarcado, se enmascara la contraseña
            self.entry_contraseña.config(show="*")
    # --------------------------------------------------
    # Sección Izquierda (tabla y búsqueda)
    # --------------------------------------------------
    def cargar_lista_usuarios(self, filtro=""):
        """Carga en el Treeview los usuarios existentes. Filtra por ID si 'filtro' no está vacío."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for usuario in self.usuarios:
            if filtro:
                if filtro not in usuario["id"]:
                    continue
            self.tree.insert("", tk.END, values=(usuario["id"], usuario["departamento"], usuario["nombre"]))

    def buscar_usuario(self):
        filtro = self.buscar_var.get().strip()
        self.cargar_lista_usuarios(filtro)

    def seleccionar_usuario_lista(self, event):
        item = self.tree.focus()
        if not item:
            return
        valores = self.tree.item(item, "values")  # (id, departamento, nombre)
        if valores:
            id_user, _, _ = valores
            self.cargar_datos_usuario(id_user)

    # --------------------------------------------------
    # Sección Derecha (formulario y botones)
    # --------------------------------------------------
    def nuevo_usuario(self):
        """Limpia el formulario para agregar un nuevo usuario."""
        self.limpiar_formulario()

    def guardar_usuario(self):
        """
        Inserta o actualiza el usuario según si existe o no el 'id' en self.usuarios.
        """
        id_user = self.id_var.get().strip()
        nombre = self.nombre_var.get().strip()
        depto = self.departamento_var.get().strip()
        tel = self.telefono_var.get().strip()
        contraseña = self.contraseña_var.get().strip()
        # Concatenamos la hora con el meridiano seleccionado
        h_entrada = self.hora_entrada_var.get().strip() + " " + self.entrada_meridiano.get()
        h_salida = self.hora_salida_var.get().strip() + " " + self.salida_meridiano.get()

        # Validaciones
        if not id_user:
            messagebox.showwarning("Validación", "El ID del usuario es obligatorio.")
            return
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return
        if len(tel) != 10 or not tel.isdigit():
            messagebox.showwarning("Validación", "El teléfono debe tener 10 dígitos numéricos.")
            return
        if not depto:
            messagebox.showwarning("Validación", "El departamento es obligatorio.")
            return
        if not contraseña:
            messagebox.showwarning("Validación", "La contraseña es obligatoria.")
            return
        if not self.hora_entrada_var.get().strip():
            messagebox.showwarning("Validación", "La hora de entrada es obligatoria (Ej: 08:00).")
            return
        if not self.hora_salida_var.get().strip():
            messagebox.showwarning("Validación", "La hora de salida es obligatoria (Ej: 04:00).")
            return

        # Verificar si ya existe
        existe = False
        for u in self.usuarios:
            if u["id"] == id_user:
                # Actualizar
                u["nombre"] = nombre
                u["departamento"] = depto
                u["telefono"] = tel
                u["contraseña"] = contraseña
                u["hora_entrada"] = h_entrada
                u["hora_salida"] = h_salida
                existe = True
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
                break

        if not existe:
            # Insertar nuevo
            self.usuarios.append({
                "id": id_user,
                "nombre": nombre,
                "departamento": depto,
                "telefono": tel,
                "contraseña": contraseña,
                "hora_entrada": h_entrada,
                "hora_salida": h_salida
            })
            messagebox.showinfo("Éxito", "Usuario insertado correctamente.")

        self.limpiar_formulario()
        self.cargar_lista_usuarios()

    def eliminar_usuario(self):
        """Elimina al usuario cuyo ID se muestra en el formulario."""
        id_user = self.id_var.get().strip()
        if not id_user:
            messagebox.showwarning("Validación", "No hay ID para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar al usuario con ID {id_user}?"):
            return

        eliminado = False
        for i, usuario in enumerate(self.usuarios):
            if usuario["id"] == id_user:
                del self.usuarios[i]
                eliminado = True
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
                break
        if not eliminado:
            messagebox.showerror("Error", "No se encontró el usuario para eliminar.")
        self.limpiar_formulario()
        self.cargar_lista_usuarios()

    def cargar_datos_usuario(self, id_user):
        """Carga los datos completos de un usuario en el formulario."""
        for usuario in self.usuarios:
            if usuario["id"] == id_user:
                self.id_var.set(usuario["id"])
                self.nombre_var.set(usuario["nombre"])
                self.departamento_var.set(usuario["departamento"])
                self.telefono_var.set(usuario["telefono"])
                self.contraseña_var.set(usuario.get("contraseña", ""))
                # Separar hora y meridiano si están concatenados
                if " " in usuario["hora_entrada"]:
                    hora, mer = usuario["hora_entrada"].split(" ")
                    self.hora_entrada_var.set(hora)
                    self.entrada_meridiano.set(mer)
                else:
                    self.hora_entrada_var.set(usuario["hora_entrada"])
                if " " in usuario["hora_salida"]:
                    hora, mer = usuario["hora_salida"].split(" ")
                    self.hora_salida_var.set(hora)
                    self.salida_meridiano.set(mer)
                else:
                    self.hora_salida_var.set(usuario["hora_salida"])
                break

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.id_var.set("")
        self.nombre_var.set("")
        self.departamento_var.set("")
        self.telefono_var.set("")
        self.contraseña_var.set("")
        self.hora_entrada_var.set("")
        self.hora_salida_var.set("")
        self.entrada_meridiano.set("AM")
        self.salida_meridiano.set("PM")


# Para probar individualmente:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Configuraciones - Prueba")
    root.state("zoomed")
    # Se invoca ConfiguracionesApp para probar la vista de configuraciones
    ConfiguracionesApp(root)
    root.mainloop()
