import tkinter as tk
from tkinter import ttk, messagebox
import conexion  # Asegúrate de que conexion.py está en el mismo directorio
from botones import configurar_estilos


class ArticuloSelector:
    def __init__(self, container, on_select_callback, on_cancel_callback=None):
        """
        container: Frame donde se cargará el selector de artículos.
        on_select_callback: función que recibirá los datos del artículo seleccionado y cantidad.
        """
        self.on_cancel = on_cancel_callback
        self.container = container
        self.on_select = on_select_callback
        self.cantidad_window = None
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
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25,font=("tahoma",11),style='Modern.TEntry')
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.refresh_list())

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

        # Eventos del treeview
        self.tree.bind('<Return>', self.on_enter_pressed)
        self.tree.bind('<Double-1>', self.on_enter_pressed)

        # Botón de regresar
        btn_frame = tk.Frame(self.container, bg="white", pady=10)
        btn_frame.pack(side=tk.BOTTOM)
        ttk.Button(self.container, text="Regresar",style="Peligro.TButton",
                  cursor="hand2", command=self.regresar).pack(side=tk.BOTTOM,pady=5)

        # Carga inicial
        self.refresh_list()
        
        # Configurar foco inicial
        self.container.after(100, self.set_initial_focus)

    def set_initial_focus(self):
        """Establece el foco inicial en el primer elemento de la tabla."""
        if self.tree.get_children():
            first_item = self.tree.get_children()[0]
            self.tree.selection_set(first_item)
            self.tree.focus(first_item)
            self.tree.focus_set()

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
        
        # Mantener selección en el primer elemento después de la búsqueda
        if self.tree.get_children():
            first_item = self.tree.get_children()[0]
            self.tree.selection_set(first_item)
            self.tree.focus(first_item)

    def on_enter_pressed(self, event=None):
        """Maneja la selección cuando se presiona Enter."""
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un artículo antes de confirmar.")
            return
        
        data = self.tree.item(sel, 'values')  # (codigo, nombre, precio, existencia)
        self.mostrar_ventana_cantidad(data)

    def mostrar_ventana_cantidad(self, articulo_data):
        """Muestra ventana para ingresar la cantidad del artículo."""
        if self.cantidad_window and self.cantidad_window.winfo_exists():
            self.cantidad_window.destroy()
        
        self.cantidad_window = tk.Toplevel(self.container)
        self.cantidad_window.title("Cantidad del Artículo")
        self.cantidad_window.geometry("400x200")
        self.cantidad_window.transient(self.container)
        self.cantidad_window.grab_set()
        self.cantidad_window.configure(bg="white")
        
        # Centrar la ventana
        self.cantidad_window.update_idletasks()
        x = (self.cantidad_window.winfo_screenwidth() // 2) - (self.cantidad_window.winfo_width() // 2)
        y = (self.cantidad_window.winfo_screenheight() // 2) - (self.cantidad_window.winfo_height() // 2)
        self.cantidad_window.geometry(f"+{x}+{y}")

        # Frame principal
        main_frame = tk.Frame(self.cantidad_window, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Información del artículo
        info_frame = tk.Frame(main_frame, bg="white")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(info_frame, text="Artículo seleccionado:", font=("Tahoma", 10, "bold"), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"Código: {articulo_data[0]}", font=("Tahoma", 10), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"Nombre: {articulo_data[1]}", font=("Tahoma", 10), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"Precio: ${articulo_data[2]}", font=("Tahoma", 10), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"Existencia: {articulo_data[3]}", font=("Tahoma", 10), bg="white").pack(anchor="w")

        # Frame para cantidad
        cantidad_frame = tk.Frame(main_frame, bg="white",height=100)
        cantidad_frame.pack(fill=tk.X, pady=0)

        
        tk.Label(cantidad_frame, text="Cantidad:", font=("Tahoma", 10, "bold"), bg="white").pack(side=tk.LEFT)
        
        self.cantidad_var = tk.StringVar(value="1")
        self.entry_cantidad = ttk.Entry(cantidad_frame, textvariable=self.cantidad_var, 
                                 font=("Tahoma", 12), width=10, style='Modern.TEntry')
        self.entry_cantidad .pack(side=tk.LEFT, padx=(10, 0))
        
        # Eventos para la entrada de cantidad
        self.entry_cantidad .bind('<Return>', lambda e: self.confirmar_cantidad(articulo_data))
        self.entry_cantidad .bind('<Escape>', lambda e: self.cantidad_window.destroy())
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(btn_frame, text="Confirmar (Enter)", style="Azul.TButton",
                  command=lambda: self.confirmar_cantidad(articulo_data)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Cancelar (Esc)", style="Azul.TButton",
                  command=self.cantidad_window.destroy).pack(side=tk.LEFT)

        # Establecer foco en la entrada de cantidad y seleccionar todo el texto
        self.entry_cantidad .focus_set()
        self.entry_cantidad .select_range(0, tk.END)

    def confirmar_cantidad(self, articulo_data):
        cantidad_str = self.entry_cantidad.get().strip()

        try:
            cantidad = int(cantidad_str)

            # Desempaquetar los datos del artículo
            codigo, nombre, precio, existencia = articulo_data

            # Convertir existencia a entero si viene como string
            existencia = int(existencia)

            if cantidad > existencia:
                messagebox.showwarning("Sin stock", "No hay suficiente existencia.")
                return

            # Llamar al callback con la cantidad válida
            self.on_select((codigo, nombre, precio, existencia, cantidad))

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido.")

            

    def regresar(self):
        """Llama a la función de cancelación o vuelve atrás."""
        if callable(self.on_cancel):
            self.on_cancel()

# Ejemplo de uso independiente
if __name__ == '__main__':
    def imprimir_seleccion(data):
        if data:
            print("Artículo seleccionado:", data)
            print(f"Código: {data[0]}, Nombre: {data[1]}, Precio: {data[2]}, Existencia: {data[3]}, Cantidad: {data[4]}")
        else:
            print("Selección cancelada")

    root = tk.Tk()
    root.title('Selector de Artículos')
    root.state('zoomed')
    ArticuloSelector(root, imprimir_seleccion)
    root.mainloop()