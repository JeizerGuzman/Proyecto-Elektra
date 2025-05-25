import tkinter as tk
from tkinter import ttk, messagebox
import conexion  # Asegúrate de que conexion.py está en el mismo directorio
from seleccionar_articulo import ArticuloSelector
from metodo_pago import MetodoPagoApp

class VentaApp:
    def __init__(self, container, usuario_nombre=None):
        """
        container: Tk o Frame donde se incrusta el módulo de ventas.
        usuario_nombre: nombre del vendedor, usado para buscar su ID en BD.
        """
        self.container = container
        self.usuario_nombre = usuario_nombre or "Vendedor General"
        # Conexión a BD
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()
        # Obtener ID de usuario desde nombre
        self.usuario_id = self._get_usuario_id(self.usuario_nombre)
        # Datos del ticket
        self.items = {}  # {codigo: [nombre, precio, cantidad, existencia]}
        # Mostrar interfaz de ventas
        self.show_sale_ui()

    def _get_usuario_id(self, nombre):
        try:
            self.cursor.execute("SELECT id_usuario FROM Usuarios WHERE nombre = %s", (nombre,))
            row = self.cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudo obtener ID de usuario: {e}")
            return None

    def _limpiar_contenedor(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_sale_ui(self):
        self._limpiar_contenedor()
        self.container.configure(bg="white")

        # Título
        title = tk.Frame(self.container, bg="#F0F0F0", height=40, padx=10, pady=5)
        title.pack(side=tk.TOP, fill=tk.X)
        tk.Label(title, text="VENTAS", font=("Helvetica",16,"bold"), bg="#F0F0F0").pack(side=tk.LEFT)

        # Botón Agregar Artículo
        sf = tk.Frame(self.container, bg="white", padx=10, pady=5)
        sf.pack(fill=tk.X)
        tk.Button(sf, text="Agregar Artículo", bg="#87CEEB", fg="white",
                  font=("Helvetica",10,"bold"), command=self.show_selector_ui).pack(side=tk.LEFT)

        # Tabla ticket
        cols = ("codigo","descripcion","precio","cantidad","importe","existencia")
        tf = tk.Frame(self.container, bg="white")
        tf.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tree = ttk.Treeview(tf, columns=cols, show="headings")
        for c,w in zip(cols,[100,200,80,80,80,80]):
            self.tree.heading(c, text=c.capitalize(), anchor="center")
            self.tree.column(c, width=w, anchor="center")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Scrollbar(tf, command=self.tree.yview).pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=lambda f,s: None)

        # Área inferior: cliente, botones y totales
        bf = tk.Frame(self.container, bg="#ECECEC", height=60, padx=10, pady=5)
        bf.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(bf, text="Cliente:", bg="#ECECEC").pack(side=tk.LEFT)
        self.client_cb = ttk.Combobox(bf, state="readonly", width=25)
        self.load_clients()
        self.client_cb.pack(side=tk.LEFT, padx=5)

        # Eliminar y vaciar
        tk.Button(bf, text="Eliminar Producto", bg="#ff4d4d", fg="white",
                  font=("Helvetica",10,"bold"), command=self.del_producto).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="Vaciar Ticket", bg="#ff4d4d", fg="white",
                  font=("Helvetica",10,"bold"), command=self.clear_ticket).pack(side=tk.LEFT, padx=5)

        # Subtotal y Total
        totals_frame = tk.Frame(bf, bg="#ECECEC")
        totals_frame.pack(side=tk.RIGHT)
        self.lbl_sub = tk.Label(totals_frame, text="Subtotal: $0.00",
                                font=("Helvetica",12,"bold"), bg="#ECECEC")
        self.lbl_sub.pack()
        self.lbl_tot = tk.Label(totals_frame, text="Total: $0.00",
                                font=("Helvetica",14,"bold"), bg="#ECECEC")
        self.lbl_tot.pack()
        # Botón Cobrar
        tk.Button(totals_frame, text="Cobrar", bg="#28a745", fg="white",
                  font=("Helvetica",10,"bold"), width=10,
                  command=self._open_metodo_pago).pack(pady=5)

        self.refresh_ticket()

    def load_clients(self):
        # Carga lista de clientes con su teléfono como clave directamente de la BD
        self.cursor.execute("SELECT telefono, nombre FROM Cliente")
        rows = self.cursor.fetchall()
        # display -> telefono mapping
        self.client_map = {f"{n} ({t})": t for t,n in rows}
        # Opciones: sólo las de BD
        opts = list(self.client_map.keys())
        self.client_cb['values'] = opts
        # Seleccionar por defecto el cliente 'Venta General (0000000000)'
        default = next((opt for opt in opts if opt.startswith('Venta General')), opts[0])
        self.client_cb.current(opts.index(default))

    def show_selector_ui(self):
        self._limpiar_contenedor()
        ArticuloSelector(self.container, self.on_select)

    def on_select(self, data):
        codigo, nombre, precio, existencia = data
        if codigo in self.items:
            if self.items[codigo][2] + 1 > int(existencia):
                return messagebox.showwarning("Sin stock", "No hay suficiente existencia.")
            self.items[codigo][2] += 1
        else:
            self.items[codigo] = [nombre, float(precio), 1, int(existencia)]
        self.show_sale_ui()

    def _open_metodo_pago(self):
        # Abrir Toplevel para método de pago
        top = tk.Toplevel(self.container)
        top.title('Método de Pago')
        # Prepara datos
        cliente_disp = self.client_cb.get()
        cliente_tel = self.client_map.get(cliente_disp)
        total = sum(info[1] * info[2] for info in self.items.values())
        productos = [ {'codigo':c, 'precio':info[1], 'cantidad':info[2]} for c,info in self.items.items() ]
        venta_data = {
            'usuario_id': self.usuario_id,
            'cliente_telefono': cliente_tel,
            'total': total,
            'productos': productos
        }
        # Lanza el módulo de pago en ventana propia
        pago = MetodoPagoApp(
            top,
            venta_data,
            on_finish_callback=self.show_sale_ui,
            usuario_nombre=self.usuario_nombre
        )
        pago.run()

    def refresh_ticket(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        sub = 0.0
        for codigo, info in self.items.items():
            nombre, precio, cantidad, existencia = info
            imp = precio * cantidad
            sub += imp
            self.tree.insert('', tk.END, values=(
                codigo, nombre, f"{precio:.2f}", cantidad, f"{imp:.2f}", existencia))
        self.lbl_sub.config(text=f"Subtotal: ${sub:.2f}")
        self.lbl_tot.config(text=f"Total: ${sub:.2f}")

    def del_producto(self):
        for iid in self.tree.selection():
            codigo = self.tree.item(iid, 'values')[0]
            if codigo in self.items:
                del self.items[codigo]
        self.refresh_ticket()

    def clear_ticket(self):
        self.items.clear()
        self.refresh_ticket()

# Para probar independientemente
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Ventas')
    root.state('zoomed')
    VentaApp(root, usuario_nombre='Ana Pérez')
    root.mainloop()
