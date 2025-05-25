import tkinter as tk
from tkinter import ttk, messagebox
import conexion  # Asegúrate de que conexion.py está en el mismo directorio
from botones import configurar_estilos



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
        configurar_estilos(self.container)
        
        
        # Conexión a la base de datos
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()
        
        # -------------------------------------------
        # Título "PROVEEDORES"
        # -------------------------------------------
        title_frame = tk.Frame(self.container, bg="#ECECEC", height=40, padx=10, pady=5)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(title_frame, text="PROVEEDORES", font=("Helvetica", 14, "bold"), bg="#ECECEC")\
            .pack(side=tk.LEFT)
        
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
        tk.Entry(search_frame, textvariable=self.buscar_var, width=15, font=("Helvetica", 10))\
            .pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Buscar",style="Gris.TButton",width=6,
                  command=self.buscar_proveedor).pack(side=tk.LEFT, padx=5)
        
        # 2) Treeview (muestra ID, Empresa y Representante)
        self.tree = ttk.Treeview(left_frame, columns=("id", "empresa", "representante"), show="headings", height=20)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        for col, txt, w in [("id","ID Proveedor",100),("empresa","Empresa",200),("representante","Representante",200)]:
            self.tree.heading(col, text=txt, anchor="center")
            self.tree.column(col, width=w, anchor="center")
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
        ttk.Button(btn_right_frame, text="Limpiar Datos",style="Azul.TButton", width=15, command=self.nuevo_proveedor)\
            .pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_right_frame, text="Eliminar Proveedor",style="Peligro.TButton", command=self.eliminar_proveedor)\
            .pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_right_frame, text="Guardar Proveedor",style="Exito.TButton", command=self.guardar_proveedor)\
            .pack(side=tk.LEFT, padx=5)
        
        # Frame del formulario
        form_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        form_right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Variables del formulario
        self.id_var = tk.StringVar()
        self.empresa_var = tk.StringVar()
        self.representante_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        
        # Etiquetas y entradas (dispuestas en grid)
        labels = [
            ("ID Proveedor:", self.id_var, 0),
            ("Teléfono (10 dígitos):", self.telefono_var, 1),
            ("Empresa:", self.empresa_var, 2),
            ("Representante:", self.representante_var, 3),
        ]
        for text, var, row in labels:
            tk.Label(form_right_frame, text=text, font=("Helvetica", 10), bg="white")\
                .grid(row=row, column=0, sticky=tk.E, padx=5, pady=5)
            tk.Entry(form_right_frame, textvariable=var, width=25, font=("Helvetica", 10))\
                .grid(row=row, column=1, padx=5, pady=5)
        
        # Carga inicial de proveedores
        self.cargar_lista_proveedores()
    
    # --------------------------------------------------
    # Funciones para la sección IZQUIERDA
    # --------------------------------------------------
    def cargar_lista_proveedores(self, filtro=""):
        """Carga en el Treeview los proveedores desde la BD."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        sql = "SELECT id_proveedor, nombre, representante FROM Proveedor"
        params = ()
        if filtro:
            sql += " WHERE id_proveedor LIKE %s"
            params = (f"%{filtro}%",)
        self.cursor.execute(sql, params)
        for idp, empresa, rep in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=(idp, empresa, rep))
    
    def buscar_proveedor(self):
        filtro = self.buscar_var.get().strip()
        self.cargar_lista_proveedores(filtro)
    
    def seleccionar_proveedor_lista(self, event):
        sel = self.tree.focus()
        if not sel:
            return
        idp, empresa, rep = self.tree.item(sel, "values")
        self.id_var.set(idp)
        self.empresa_var.set(empresa)
        self.representante_var.set(rep)
        # Carga teléfono aparte
        self.cursor.execute("SELECT telefono FROM Proveedor WHERE id_proveedor = %s", (idp,))
        row = self.cursor.fetchone()
        self.telefono_var.set(row[0] if row else "")
    
    # --------------------------------------------------
    # Funciones para la sección DERECHA
    # --------------------------------------------------
    def nuevo_proveedor(self):
        """Limpia el formulario para un nuevo registro."""
        self.id_var.set("")
        self.empresa_var.set("")
        self.representante_var.set("")
        self.telefono_var.set("")
    
    def guardar_proveedor(self):
        idp = self.id_var.get().strip()
        empresa = self.empresa_var.get().strip()
        rep = self.representante_var.get().strip()
        tel = self.telefono_var.get().strip()
        
        # Validaciones
        if not idp:
            messagebox.showwarning("Validación", "El ID del proveedor es obligatorio.")
            return
        if not empresa or not rep:
            messagebox.showwarning("Validación", "Empresa y representante son obligatorios.")
            return
        if len(tel) != 10 or not tel.isdigit():
            messagebox.showwarning("Validación", "El teléfono debe tener 10 dígitos numéricos.")
            return
        
        # Insert o Update
        self.cursor.execute("SELECT 1 FROM Proveedor WHERE id_proveedor = %s", (idp,))
        if self.cursor.fetchone():
            sql = """
                UPDATE Proveedor
                   SET nombre=%s, representante=%s, telefono=%s
                 WHERE id_proveedor=%s
            """
            params = (empresa, rep, tel, idp)
            message = "Proveedor actualizado correctamente."
        else:
            sql = """
                INSERT INTO Proveedor (id_proveedor, nombre, representante, telefono)
                VALUES (%s, %s, %s, %s)
            """
            params = (idp, empresa, rep, tel)
            message = "Proveedor insertado correctamente."
        try:
            self.cursor.execute(sql, params)
            self.db.commit()
            messagebox.showinfo("Éxito", message)
            self.nuevo_proveedor()
            self.cargar_lista_proveedores()
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))
    
    def eliminar_proveedor(self):
        idp = self.id_var.get().strip()
        if not idp:
            messagebox.showwarning("Validación", "No hay ID para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar proveedor {idp}?"):
            return
        try:
            self.cursor.execute("DELETE FROM Proveedor WHERE id_proveedor = %s", (idp,))
            self.db.commit()
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
            self.nuevo_proveedor()
            self.cargar_lista_proveedores()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))

# Para probar de forma independiente:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Proveedores")
    root.state("zoomed")
    ProveedorApp(root)
    root.mainloop()
