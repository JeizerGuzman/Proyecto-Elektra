import tkinter as tk
from tkinter import ttk, messagebox
import conexion  # Tu módulo conexion.py
from botones import configurar_estilos

class UnidadApp:
    def __init__(self, container):
        self.container = container
        # Limpia contenedor
        for w in self.container.winfo_children():
            w.destroy()
        self.container.configure(bg="white")
        configurar_estilos(self.container)
        
        
        # Conexión
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()

        # Variables
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.buscar_var = tk.StringVar()

        # Construye UI y carga datos
        self._crear_interfaz()
        self.cargar_lista_unidades()

    def _crear_interfaz(self):
        main = tk.Frame(self.container, bg="white")
        main.pack(fill=tk.BOTH, expand=True)

        # IZQUIERDA: búsqueda + lista
        left = tk.Frame(main, bg="white")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sf = tk.Frame(left, bg="white", padx=10, pady=10)
        sf.pack(fill=tk.X)
        tk.Label(sf, text="Buscar ID Unidad:", bg="white").pack(side=tk.LEFT)
        tk.Entry(sf, textvariable=self.buscar_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(sf, text="Buscar",style="Gris.TButton",width=6, command=self.buscar_unidad).pack(side=tk.LEFT)

        self.tree = ttk.Treeview(left, columns=("id","nombre"), show="headings", height=15)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for col, txt, w in [("id","ID Unidad",100),("nombre","Nombre",200)]:
            self.tree.heading(col, text=txt)
            self.tree.column(col, width=w, anchor="center")
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_unidad_lista)

        # DERECHA: formulario + botones
        right = tk.Frame(main, bg="white")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        bf = tk.Frame(right, bg="white", pady=10)
        bf.pack(fill=tk.X)

        ttk.Button(bf, text="Limpiar Datos", style="Azul.TButton", command=self.nueva_unidad).pack(side=tk.LEFT, padx=5)
        ttk.Button(bf, text="Eliminar Unidad", style="Peligro.TButton", command=self.eliminar_unidad).pack(side=tk.LEFT, padx=5)
        ttk.Button(bf, text="Guardar Unidad", style="Exito.TButton", command=self.guardar_unidad).pack(side=tk.LEFT, padx=5)
        
        

        ff = tk.Frame(right, bg="white", padx=10, pady=10)
        ff.pack(fill=tk.BOTH, expand=True)
        tk.Label(ff, text="ID Unidad:", bg="white").grid(row=0, column=0, sticky=tk.E, pady=5, padx=5)
        tk.Entry(ff, textvariable=self.id_var, width=20).grid(row=0, column=1, pady=5, padx=5)
        tk.Label(ff, text="Nombre:", bg="white").grid(row=1, column=0, sticky=tk.E, pady=5, padx=5)
        tk.Entry(ff, textvariable=self.nombre_var, width=20).grid(row=1, column=1, pady=5, padx=5)

    def cargar_lista_unidades(self, filtro=""):
        self.tree.delete(*self.tree.get_children())
        try:
            if filtro:
                sql = "SELECT id_unidad, nombre FROM Unidad WHERE id_unidad LIKE %s"
                params = (f"%{filtro}%",)
            else:
                sql = "SELECT id_unidad, nombre FROM Unidad"
                params = ()
            self.cursor.execute(sql, params)
            for id_u, nom in self.cursor.fetchall():
                self.tree.insert("", tk.END, values=(id_u, nom))
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))

    def buscar_unidad(self):
        self.cargar_lista_unidades(self.buscar_var.get().strip())

    def seleccionar_unidad_lista(self, _):
        sel = self.tree.focus()
        if not sel:
            return
        id_u, nom = self.tree.item(sel, "values")
        self.id_var.set(id_u)
        self.nombre_var.set(nom)

    def nueva_unidad(self):
        self.id_var.set("")
        self.nombre_var.set("")

    def guardar_unidad(self):
        id_u = self.id_var.get().strip()
        nom = self.nombre_var.get().strip()

        # Validación: ID debe ser entero
        if not id_u.isdigit():
            messagebox.showerror("ID inválido", "El ID de unidad debe ser un número entero.")
            return
        if not nom:
            messagebox.showwarning("Nombre vacío", "El nombre de la unidad es obligatorio.")
            return

        try:
            # ¿Existe?
            self.cursor.execute("SELECT 1 FROM Unidad WHERE id_unidad = %s", (id_u,))
            if self.cursor.fetchone():
                # UPDATE
                self.cursor.execute(
                    "UPDATE Unidad SET nombre = %s WHERE id_unidad = %s",
                    (nom, id_u)
                )
                messagebox.showinfo("Actualizado", "Unidad actualizada correctamente.")
            else:
                # INSERT
                self.cursor.execute(
                    "INSERT INTO Unidad (id_unidad, nombre) VALUES (%s, %s)",
                    (id_u, nom)
                )
                messagebox.showinfo("Insertado", "Unidad agregada correctamente.")
            self.db.commit()
            self.cargar_lista_unidades()
            self.nueva_unidad()
        except Exception as e:
            # Muestra sólo el mensaje de error de MySQL (p. ej. violación de PK, etc.)
            messagebox.showerror("Error al guardar", e.msg if hasattr(e, 'msg') else str(e))

    def eliminar_unidad(self):
        id_u = self.id_var.get().strip()
        if not id_u:
            messagebox.showwarning("ID vacío", "No hay ID para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"Eliminar unidad {id_u}?"):
            return
        try:
            self.cursor.execute("DELETE FROM Unidad WHERE id_unidad = %s", (id_u,))
            self.db.commit()
            if self.cursor.rowcount:
                messagebox.showinfo("Eliminado", "Unidad eliminada correctamente.")
            else:
                messagebox.showwarning("No encontrado", "No existe esa unidad.")
            self.cargar_lista_unidades()
            self.nueva_unidad()
        except Exception as e:
            messagebox.showerror("Error al eliminar", e.msg if hasattr(e, 'msg') else str(e))

# Para prueba independiente
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Unidades")
    root.state("zoomed")
    UnidadApp(root)
    root.mainloop()
