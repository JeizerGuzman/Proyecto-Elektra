import tkinter as tk
from tkinter import ttk, messagebox
import conexion  # tu módulo de conexión
from categorias import CategoriaApp
from unidades import UnidadApp

class ConfiguracionesApp:
    def __init__(self, container):
        self.container = container
        for w in self.container.winfo_children(): w.destroy()
        self.container.configure(bg="white")

        # Cabecera
        header = tk.Frame(self.container, bg="#ECECEC", height=40, padx=10, pady=5)
        header.pack(fill=tk.X)
        tk.Label(header, text="CONFIGURACIONES", font=("Helvetica",14,"bold"), bg="#ECECEC")\
            .pack(side=tk.LEFT)

        # Navegación
        main = tk.Frame(self.container, bg="white")
        main.pack(fill=tk.BOTH, expand=True)
        nav = tk.Frame(main, bg="#F0F0F0", height=40)
        nav.pack(fill=tk.X)
        tk.Button(nav, text="Usuarios",   font=("Helvetica",10,"bold"), width=15,
                  command=self.on_usuarios).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(nav, text="Categorías", font=("Helvetica",10,"bold"), width=15,
                  command=self.on_categorias).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(nav, text="Unidades",    font=("Helvetica",10,"bold"), width=18,
                  command=self.on_unidades).pack(side=tk.LEFT, padx=5, pady=5)

        # Contenedor de vista
        self.content = tk.Frame(main, bg="white")
        self.content.pack(fill=tk.BOTH, expand=True)
        self.on_usuarios()

    def _clear(self):
        for w in self.content.winfo_children(): w.destroy()

    def on_usuarios(self):
        self._clear()
        UsuarioApp(self.content)

    def on_categorias(self):
        self._clear()
        CategoriaApp(self.content)

    def on_unidades(self):
        self._clear()
        UnidadApp(self.content)


class UsuarioApp:
    """Gestión de Usuarios (sin hora_entrada/hora_salida)."""
    def __init__(self, container):
        self.container = container
        for w in self.container.winfo_children(): w.destroy()
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()

        # Variables
        self.id_var    = tk.StringVar()
        self.nom_var   = tk.StringVar()
        self.dept_var  = tk.StringVar()
        self.sal_var   = tk.StringVar()
        self.tel_var   = tk.StringVar()
        self.pwd_var   = tk.StringVar()
        self.search_var= tk.StringVar()

        # Layout principal
        main = tk.Frame(self.container, bg="white")
        main.pack(fill=tk.BOTH, expand=True)

        # Izquierda: búsqueda + tabla
        left = tk.Frame(main, bg="white")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sf = tk.Frame(left, bg="white", padx=10, pady=10); sf.pack(fill=tk.X)
        tk.Label(sf, text="Buscar ID Usuario:", bg="white").pack(side=tk.LEFT)
        tk.Entry(sf, textvariable=self.search_var, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(sf, text="Buscar", bg="#A9A9A9", fg="white", font=("Helvetica",9,"bold"),
                  command=self.load_users).pack(side=tk.LEFT)

        cols = ("id","dep","nom")
        self.tree = ttk.Treeview(left, columns=cols, show="headings", height=20)
        for col, txt, w in [("id","ID Usuario",80),("dep","Departamento",120),("nom","Nombre",180)]:
            self.tree.heading(col, text=txt)
            self.tree.column(col, width=w, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        sb = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        sb.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.bind("<ButtonRelease-1>", self.select_user)

        # Derecha: formulario + botones
        right = tk.Frame(main, bg="white", padx=10, pady=10)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        bf = tk.Frame(right, bg="white", pady=10); bf.pack(fill=tk.X)
        actions = [
            ("Nuevo Usuario", self.new_user, "#87CEEB"),
            ("Guardar Usuario", self.save_user, "green"),
            ("Eliminar Usuario", self.delete_user, "red")
        ]
        for txt, cmd, col in actions:
            tk.Button(bf, text=txt, bg=col, fg="white", font=("Helvetica",10,"bold"), width=15,
                      command=cmd).pack(side=tk.LEFT, padx=5)

        form = tk.Frame(right, bg="white", padx=10, pady=10)
        form.pack(fill=tk.BOTH, expand=True)
        labels = ["ID Usuario:", "Nombre:", "Departamento:", "Salario:", "Teléfono:", "Contraseña:"]
        for i, lbl in enumerate(labels):
            tk.Label(form, text=lbl, bg="white").grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Entry(form, textvariable=self.id_var, width=25).grid(row=0, column=1)
        tk.Entry(form, textvariable=self.nom_var, width=25).grid(row=1, column=1)
        ttk.Combobox(form, textvariable=self.dept_var,
                     values=["Administrador","Gerencia","Ventas","Cajas","Servicio al Cliente","Bodega"],
                     width=22).grid(row=2, column=1)
        tk.Entry(form, textvariable=self.sal_var, width=25).grid(row=3, column=1)
        tk.Entry(form, textvariable=self.tel_var, width=25).grid(row=4, column=1)
        self.pwd_entry = tk.Entry(form, textvariable=self.pwd_var, show="*", width=25)
        self.pwd_entry.grid(row=5, column=1)
        tk.Checkbutton(form, text="Mostrar", variable=tk.IntVar(),
                       command=self.toggle_pwd, bg="white").grid(row=5, column=2)

        # Carga inicial
        self.load_users()

    def toggle_pwd(self):
        s = self.pwd_entry.cget('show')
        self.pwd_entry.config(show='' if s=='*' else '*')

    def load_users(self):
        self.tree.delete(*self.tree.get_children())
        sql = "SELECT id_usuario, departamento, nombre FROM Usuarios"
        params = ()
        f = self.search_var.get().strip()
        if f:
            sql += " WHERE id_usuario LIKE %s"
            params = (f"%{f}%",)
        self.cursor.execute(sql, params)
        for idu, dep, nm in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=(idu, dep, nm))

    def select_user(self, _):
        sel = self.tree.focus()
        if not sel: return
        idu = self.tree.item(sel, 'values')[0]
        self.cursor.execute(
            "SELECT id_usuario, nombre, departamento, salario, telefono, contraseña FROM Usuarios WHERE id_usuario=%s",
            (idu,)
        )
        rec = self.cursor.fetchone()
        if rec:
            uid, nm, dp, sal, tel, pw = rec
            self.id_var.set(uid)
            self.nom_var.set(nm)
            self.dept_var.set(dp)
            self.sal_var.set(str(sal))
            self.tel_var.set(tel)
            self.pwd_var.set(pw)

    def new_user(self):
        for var in (self.id_var, self.nom_var, self.dept_var,
                    self.sal_var, self.tel_var, self.pwd_var):
            var.set("")

    def save_user(self):
        uid, nm, dp = self.id_var.get().strip(), self.nom_var.get().strip(), self.dept_var.get().strip()
        sal, tel, pw = self.sal_var.get().strip(), self.tel_var.get().strip(), self.pwd_var.get().strip()
        # Validaciones
        if not all([uid, nm, dp, sal, tel, pw]):
            messagebox.showwarning("Validación", "Todos los campos son obligatorios."); return
        if not tel.isdigit() or len(tel)!=10:
            messagebox.showwarning("Validación", "Teléfono inválido."); return
        if not sal.isdigit():
            messagebox.showwarning("Validación", "Salario debe ser numérico."); return
        sal_i = int(sal)
        # Insert / Update
        self.cursor.execute("SELECT 1 FROM Usuarios WHERE id_usuario=%s", (uid,))
        if self.cursor.fetchone():
            sql = ("UPDATE Usuarios SET nombre=%s, departamento=%s, salario=%s, telefono=%s, contraseña=%s "
                   "WHERE id_usuario=%s")
            params = (nm, dp, sal_i, tel, pw, uid)
            msg = "Usuario actualizado correctamente."
        else:
            sql = ("INSERT INTO Usuarios (id_usuario, nombre, departamento, salario, telefono, contraseña) "
                   "VALUES (%s,%s,%s,%s,%s,%s)")
            params = (uid, nm, dp, sal_i, tel, pw)
            msg = "Usuario creado correctamente."
        try:
            self.cursor.execute(sql, params)
            self.db.commit()
            messagebox.showinfo("Éxito", msg)
            self.load_users()
            self.new_user()
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    def delete_user(self):
        uid = self.id_var.get().strip()
        if not uid:
            messagebox.showwarning("Validación", "ID requerido."); return
        if not messagebox.askyesno("Confirmar", "¿Eliminar usuario? "): return
        try:
            self.cursor.execute("DELETE FROM Usuarios WHERE id_usuario=%s", (uid,))
            self.db.commit()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
            self.load_users()
            self.new_user()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Configuraciones")
    root.state("zoomed")
    ConfiguracionesApp(root)
    root.mainloop()
