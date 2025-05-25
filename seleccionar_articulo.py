import tkinter as tk
from tkinter import ttk, messagebox
import conexion  # Asegúrate de que conexion.py está en el mismo directorio
from botones import configurar_estilos



class ArticuloSelector:
    def __init__(self, container, on_select_callback):
        """
        container: Frame donde se cargará el selector de artículos.
        on_select_callback: función que recibirá los datos del artículo seleccionado.
        """
        self.container = container
        self.on_select = on_select_callback
        configurar_estilos(self.container)
        
        
        # Limpiar contenedor
        for w in self.container.winfo_children():
            w.destroy()
        self.container.configure(bg="white")

        # Conexión a BD
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()

        # Título
        header = tk.Frame(self.container, bg="#8FC9DB", height=40, padx=10, pady=5)
        header.pack(side=tk.TOP, fill=tk.X)
        tk.Label(header, text="SELECCIONAR ARTÍCULO", font=("Tahoma",16,"bold"),fg="white", bg="#8FC9DB").pack(side=tk.LEFT)

        # Búsqueda en tiempo real
        search_frame = tk.Frame(self.container, bg="white", padx=10, pady=5)
        search_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(search_frame, text="Buscar (código o descripción):", bg="white").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25,font=("tahoma",11),style='Modern.TEntry')
        entry.pack(side=tk.LEFT, padx=5)
        entry.bind('<KeyRelease>', lambda e: self.refresh_list())

        # Treeview de resultados
        cols = ("codigo","nombre","precio","existencia")
        list_frame = tk.Frame(self.container, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings")
        for c,w in zip(cols,[100,250,80,80]):
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=w, anchor='center')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, command=self.tree.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Botón de selección
        btn_frame = tk.Frame(self.container, bg="white", pady=10)
        btn_frame.pack(side=tk.BOTTOM)
        ttk.Button(btn_frame, text="Confirmar Selección",style="Azul.TButton",
                  command=self.confirm_selection).pack()

        # Carga inicial
        self.refresh_list()

    def refresh_list(self):
        """Refresca el Treeview según el texto de búsqueda."""
        query = self.search_var.get().strip()
        sql = "SELECT codigo, nombre, precio, existencia FROM Articulo"
        params = ()
        if query:
            sql += " WHERE codigo LIKE %s OR nombre LIKE %s"
            like = f"%{query}%"
            params = (like, like)
        self.cursor.execute(sql, params)
        rows = self.cursor.fetchall()

        # Limpiar y poblar
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        for r in rows:
            self.tree.insert('', tk.END, values=r)

    def confirm_selection(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un artículo antes de confirmar.")
            return
        data = self.tree.item(sel, 'values')  # (codigo, nombre, precio, existencia)
        self.on_select(data)

# Ejemplo de uso independiente
if __name__ == '__main__':
    def imprimir_seleccion(data):
        print("Artículo seleccionado:", data)

    root = tk.Tk()
    root.title('Selector de Artículos')
    root.state('zoomed')
    ArticuloSelector(root, imprimir_seleccion)
    root.mainloop()
