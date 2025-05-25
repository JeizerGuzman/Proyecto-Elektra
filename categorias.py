import tkinter as tk
from tkinter import ttk, messagebox
import conexion  # Asegúrate que 'conexion.py' está en el mismo directorio
from botones import configurar_estilos


class CategoriaApp:
    def __init__(self, container):
        self.container = container
        for widget in self.container.winfo_children():
            widget.destroy()
        self.container.configure(bg="white")
        configurar_estilos(self.container)
        
        # Conexión a la base de datos
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()

        # ---------------- INTERFAZ ------------------

        main_frame = tk.Frame(self.container, bg="white")
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        search_frame = tk.Frame(left_frame, bg="white", padx=10, pady=10)
        search_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(search_frame, text="Buscar ID Categoría:", font=("Helvetica", 10), bg="white")\
            .pack(side=tk.LEFT)
        self.buscar_var = tk.StringVar()
        entry_buscar = tk.Entry(search_frame, textvariable=self.buscar_var, width=15, font=("Helvetica", 10))
        entry_buscar.pack(side=tk.LEFT, padx=5)
        btn_buscar = ttk.Button(search_frame, text="Buscar", style="Gris.TButton",
                               command=self.buscar_categoria)
        btn_buscar.config(width=6)
        btn_buscar.pack(side=tk.LEFT, padx=5)

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

        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        btn_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        btn_right_frame.pack(side=tk.TOP, fill=tk.X)
        
        btn_nuevo = ttk.Button(
            btn_right_frame,
            text="Limpiar Datos",
            style="Azul.TButton",  # Estilo equivalente al azul claro
            command=self.nueva_categoria
        )
        btn_nuevo.pack(side=tk.LEFT, padx=5)
        
        # Botón Eliminar (equivalente a bg="red")
        btn_eliminar = ttk.Button(
            btn_right_frame,
            text="Eliminar Categoria",
            style="Peligro.TButton",  # Estilo rojo
            command=self.eliminar_categoria
        )
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        # Botón Guardar (equivalente a bg="green")
        btn_guardar = ttk.Button(
            btn_right_frame,
            text="Guardar Categoria",
            style="Exito.TButton",  # Estilo verde
            command=self.guardar_categoria
        )
        
        btn_guardar.pack(side=tk.LEFT, padx=5)
        btn_guardar.pack(side=tk.LEFT, padx=5)
        form_right_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        form_right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()

        tk.Label(form_right_frame, text="ID Categoría:", font=("Helvetica", 10), bg="white")\
            .grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.id_entry = tk.Entry(form_right_frame, textvariable=self.id_var, width=25, font=("Helvetica", 10))
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_right_frame, text="Nombre Categoría:", font=("Helvetica", 10), bg="white")\
            .grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.nombre_entry = tk.Entry(form_right_frame, textvariable=self.nombre_var, width=25, font=("Helvetica", 10))
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)

        self.cargar_lista_categorias()

    # ---------------- FUNCIONES ------------------

    def cargar_lista_categorias(self, filtro=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            if filtro:
                self.cursor.execute("SELECT id_categoria, nombre FROM Categoria WHERE id_categoria LIKE %s", (f"%{filtro}%",))
            else:
                self.cursor.execute("SELECT id_categoria, nombre FROM Categoria")
            filas = self.cursor.fetchall()
            for fila in filas:
                self.tree.insert("", tk.END, values=(fila[0], fila[1]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la lista: {e}")

    def buscar_categoria(self):
        filtro = self.buscar_var.get().strip()
        self.cargar_lista_categorias(filtro)

    def seleccionar_categoria_lista(self, event):
        item = self.tree.focus()
        if not item:
            return
        valores = self.tree.item(item, "values")
        if valores:
            id_cat, _ = valores
            self.cargar_datos_categoria(id_cat)

    def nueva_categoria(self):
        self.limpiar_formulario()

    def guardar_categoria(self):
        id_cat = self.id_var.get().strip()
        nombre = self.nombre_var.get().strip()
        if not id_cat or not nombre:
            messagebox.showwarning("Validación", "Debe ingresar ID y Nombre.")
            return
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Categoria WHERE id_categoria = %s", (id_cat,))
            existe = self.cursor.fetchone()[0] > 0
            if existe:
                self.cursor.execute("UPDATE Categoria SET nombre = %s WHERE id_categoria = %s", (nombre, id_cat))
                messagebox.showinfo("Actualizado", "Categoría actualizada.")
            else:
                self.cursor.execute("INSERT INTO Categoria (id_categoria, nombre) VALUES (%s, %s)", (id_cat, nombre))
                messagebox.showinfo("Insertado", "Categoría agregada.")
            self.db.commit()
            self.limpiar_formulario()
            self.cargar_lista_categorias()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def eliminar_categoria(self):
        id_cat = self.id_var.get().strip()
        if not id_cat:
            messagebox.showwarning("Validación", "No hay ID para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la categoría con ID {id_cat}?"):
            return
        try:
            self.cursor.execute("DELETE FROM Categoria WHERE id_categoria = %s", (id_cat,))
            self.db.commit()
            if self.cursor.rowcount:
                messagebox.showinfo("Eliminado", "Categoría eliminada.")
            else:
                messagebox.showwarning("Aviso", "Categoría no encontrada.")
            self.limpiar_formulario()
            self.cargar_lista_categorias()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def cargar_datos_categoria(self, id_cat):
        try:
            self.cursor.execute("SELECT id_categoria, nombre FROM Categoria WHERE id_categoria = %s", (id_cat,))
            fila = self.cursor.fetchone()
            if fila:
                self.id_var.set(fila[0])
                self.nombre_var.set(fila[1])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")

    def limpiar_formulario(self):
        self.id_var.set("")
        self.nombre_var.set("")

# Para probar de forma independiente:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Categorías")
    root.state("zoomed")
    CategoriaApp(root)
    root.mainloop()
