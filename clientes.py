import tkinter as tk
from tkinter import ttk, messagebox
import conexion  # tu módulo conexion.py

class ClienteApp:
    def __init__(self, container):
        """
        Interfaz de Clientes conectada a la tabla Cliente.
        Llave primaria: teléfono. Campo nombre almacena nombre completo.
        Dirección y RFC opcionales activados por checkbox.
        """
        self.container = container
        for w in self.container.winfo_children(): w.destroy()
        self.container.configure(bg="white")

        # Conexión
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()

        # Cabecera
        header = tk.Frame(self.container, bg="#ECECEC", height=40, padx=10, pady=5)
        header.pack(fill=tk.X)
        tk.Label(header, text="CLIENTES", font=("Helvetica",14,"bold"), bg="#ECECEC").pack(side=tk.LEFT)

        # Layout
        main = tk.Frame(self.container, bg="white")
        main.pack(fill=tk.BOTH, expand=True)

        # Izquierda: lista y búsqueda
        left = tk.Frame(main, bg="white")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sf = tk.Frame(left, bg="white", padx=10, pady=10); sf.pack(fill=tk.X)
        tk.Label(sf, text="Buscar Teléfono:", bg="white").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        tk.Entry(sf, textvariable=self.search_var, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(sf, text="Buscar", bg="#A9A9A9", fg="white", font=("Helvetica",9,"bold"),
                  command=self.load_clients).pack(side=tk.LEFT)

        cols = ("telefono","nombre")
        self.tree = ttk.Treeview(left, columns=cols, show="headings", height=20)
        self.tree.heading("telefono", text="Teléfono"); self.tree.column("telefono", width=100, anchor="center")
        self.tree.heading("nombre", text="Nombre"); self.tree.column("nombre", width=200, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.bind("<ButtonRelease-1>", self.on_select_client)

        # Derecha: formulario + botones
        right = tk.Frame(main, bg="white", padx=10, pady=10)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        bf = tk.Frame(right, bg="white", pady=10); bf.pack(fill=tk.X)
        actions = [("Nuevo Cliente", self.new_client, "#87CEEB"),
                   ("Guardar", self.save_client, "green"),
                   ("Eliminar", self.delete_client, "red")]
        for txt, cmd, col in actions:
            tk.Button(bf, text=txt, bg=col, fg="white", font=("Helvetica",10,"bold"), width=12,
                      command=cmd).pack(side=tk.LEFT, padx=5)

        form = tk.Frame(right, bg="white", padx=10, pady=10)
        form.pack(fill=tk.BOTH, expand=True)

        # Variables
        self.telefono_var = tk.StringVar()
        self.nombre_var   = tk.StringVar()
        self.direccion_var= tk.StringVar()
        self.rfc_var      = tk.StringVar()
        self.advanced_var = tk.BooleanVar(value=False)

        # Form fields
        tk.Label(form, text="Teléfono (10 dígitos):", bg="white").grid(row=0,column=0,sticky=tk.E,pady=5)
        tk.Entry(form, textvariable=self.telefono_var, width=25).grid(row=0,column=1,pady=5)
        tk.Label(form, text="Nombre:", bg="white").grid(row=1,column=0,sticky=tk.E,pady=5)
        tk.Entry(form, textvariable=self.nombre_var, width=25).grid(row=1,column=1,pady=5)

        # Checkbox para campos opcionales
        tk.Checkbutton(form, text="Datos adicionales", variable=self.advanced_var,
                       command=self.toggle_advanced, bg="white").grid(row=2,column=1, sticky=tk.W)

        # Campos opcionales (ocultos inicialmente)
        self.dir_label = tk.Label(form, text="Dirección:", bg="white")
        self.dir_entry = tk.Entry(form, textvariable=self.direccion_var, width=25)
        self.rfc_label = tk.Label(form, text="RFC:", bg="white")
        self.rfc_entry = tk.Entry(form, textvariable=self.rfc_var, width=25)

        # Cargar datos
        self.load_clients()

    def toggle_advanced(self):
        if self.advanced_var.get():
            # mostrar
            self.dir_label.grid(row=3,column=0,sticky=tk.E,pady=5)
            self.dir_entry.grid(row=3,column=1,pady=5)
            self.rfc_label.grid(row=4,column=0,sticky=tk.E,pady=5)
            self.rfc_entry.grid(row=4,column=1,pady=5)
        else:
            # ocultar
            self.dir_label.grid_remove()
            self.dir_entry.grid_remove()
            self.rfc_label.grid_remove()
            self.rfc_entry.grid_remove()

    def load_clients(self):
        self.tree.delete(*self.tree.get_children())
        sql = "SELECT telefono, nombre FROM Cliente"
        params = ()
        f = self.search_var.get().strip()
        if f:
            sql += " WHERE telefono LIKE %s"
            params = (f"%{f}%",)
        self.cursor.execute(sql, params)
        for tel, nm in self.cursor.fetchall():
            self.tree.insert("",tk.END,values=(tel,nm))

    def buscar_cliente(self):
        self.load_clients()

    def on_select_client(self, event):
        sel = self.tree.focus(); vals = self.tree.item(sel,'values')
        if not vals: return
        tel = vals[0]
        self.cursor.execute("SELECT nombre, direccion, rfc FROM Cliente WHERE telefono=%s",(tel,))
        rec = self.cursor.fetchone()
        if rec:
            nm, dirc, rfc = rec
            self.telefono_var.set(str(tel))
            self.nombre_var.set(nm)
            if dirc or rfc:
                self.advanced_var.set(True)
                self.toggle_advanced()
                self.direccion_var.set(dirc)
                self.rfc_var.set(rfc)
            else:
                self.advanced_var.set(False)
                self.toggle_advanced()

    def new_client(self):
        self.telefono_var.set("")
        self.nombre_var.set("")
        self.direccion_var.set("")
        self.rfc_var.set("")
        self.advanced_var.set(False)
        self.toggle_advanced()

    def save_client(self):
        tel = self.telefono_var.get().strip()
        nm  = self.nombre_var.get().strip()
        dirc= self.direccion_var.get().strip() if self.advanced_var.get() else ''
        rfc = self.rfc_var.get().strip().upper() if self.advanced_var.get() else ''
        # Validaciones
        if not tel.isdigit() or len(tel)!=10:
            messagebox.showwarning("Validación","Teléfono inválido."); return
        if not nm:
            messagebox.showwarning("Validación","Nombre obligatorio."); return
        if self.advanced_var.get() and len(rfc)!=13:
            messagebox.showwarning("Validación","RFC debe tener 13 caracteres."); return
        # Insert/update
        self.cursor.execute("SELECT 1 FROM Cliente WHERE telefono=%s",(tel,))
        if self.cursor.fetchone():
            sql = "UPDATE Cliente SET nombre=%s, direccion=%s, rfc=%s WHERE telefono=%s"
            params=(nm,dirc,rfc,tel); msg="Cliente actualizado correctamente."
        else:
            sql = "INSERT INTO Cliente (telefono,nombre,direccion,rfc) VALUES (%s,%s,%s,%s)"
            params=(tel,nm,dirc,rfc); msg="Cliente insertado correctamente."
        try:
            self.cursor.execute(sql,params)
            self.db.commit()
            messagebox.showinfo("Éxito",msg)
            self.new_client()
            self.load_clients()
        except Exception as e:
            messagebox.showerror("Error al guardar",str(e))

    def delete_client(self):
        tel = self.telefono_var.get().strip()
        if not tel:
            messagebox.showwarning("Validación","Teléfono requerido."); return
        if not messagebox.askyesno("Confirmar",f"Eliminar cliente {tel}? "): return
        try:
            self.cursor.execute("DELETE FROM Cliente WHERE telefono=%s",(tel,))
            self.db.commit()
            messagebox.showinfo("Éxito","Cliente eliminado correctamente.")
            self.new_client()
            self.load_clients()
        except Exception as e:
            messagebox.showerror("Error al eliminar",str(e))

# Prueba independiente
if __name__ == "__main__":
    root=tk.Tk(); root.title("Clientes"); root.state("zoomed")
    ClienteApp(root); root.mainloop()
