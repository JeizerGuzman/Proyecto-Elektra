import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
import conexion
from seleccionar_articulo import ArticuloSelector


class MetodoPagoApp:
    def __init__(self, container, venta_app, usuario=None):
        # Quien atiende
        self.usuario = usuario or "Vendedor General"
        self.venta_app = venta_app
        self.parent = container
        # Conectar BDD y preparar datos
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()
        self.items = venta_app.items
        self.total = sum(p*c for _, p, c, _ in self.items.values())
        self.folio = self._siguiente_folio()
        # Estilos
        self._config_styles()
        # Interfaz
        self._render_ui()

    def _siguiente_folio(self):
        self.cursor.execute("SELECT MAX(id_venta) FROM Venta")
        r = self.cursor.fetchone()[0]
        return (r or 999) + 1

    def _config_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        # Botones primarios
        style.configure('Primary.TButton', background='#28a745', foreground='white', font=('Helvetica',10,'bold'), padding=6)
        style.map('Primary.TButton', background=[('active','#218838')])
        # Botones secundarios
        style.configure('Secondary.TButton', background='#17a2b8', foreground='white', font=('Helvetica',10,'bold'), padding=6)
        style.map('Secondary.TButton', background=[('active','#117a8b')])
        # Botones cancel
        style.configure('Danger.TButton', background='#dc3545', foreground='white', font=('Helvetica',10,'bold'), padding=6)
        style.map('Danger.TButton', background=[('active','#c82333')])

    def _limpiar(self):
        for w in self.parent.winfo_children(): w.destroy()

    def _render_ui(self):
        self._limpiar()
        self.parent.configure(bg='white')
        # Header similar a VentaApp
        hdr = tk.Frame(self.parent, bg='#ECECEC', height=40)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text='COBRAR', font=('Helvetica',14,'bold'), bg='#ECECEC').pack(side=tk.LEFT, padx=10)
        tk.Label(hdr, text=f'Folio: {self.folio}', font=('Helvetica',12), bg='#ECECEC').pack(side=tk.RIGHT, padx=10)
        # Total
        totf = tk.Frame(self.parent, bg='white', pady=10)
        totf.pack(fill=tk.X)
        tk.Label(totf, text='Total a pagar:', font=('Helvetica',12), bg='white').pack(side=tk.LEFT, padx=10)
        tk.Label(totf, text=f'$ {self.total:.2f}', font=('Helvetica',18,'bold'), fg='#28a745', bg='white').pack(side=tk.LEFT)
        # Métodos (solo efectivo activo)
        pay = tk.Frame(self.parent, bg='white', pady=10)
        pay.pack(fill=tk.X)
        tk.Label(pay, text='Método de pago:', font=('Helvetica',12), bg='white').pack(side=tk.LEFT, padx=10)
        self.pay_var = tk.StringVar(value='Efectivo')
        rb1 = ttk.Radiobutton(pay, text='Efectivo', variable=self.pay_var, value='Efectivo')
        rb1.pack(side=tk.LEFT, padx=5)
        rb2 = ttk.Radiobutton(pay, text='Crédito', variable=self.pay_var, value='Crédito')
        rb2.state(['disabled'])
        rb2.pack(side=tk.LEFT, padx=5)
        tk.Label(pay, text='(Crédito no disponible)', font=('Helvetica',10), fg='gray', bg='white').pack(side=tk.LEFT)
        # Efectivo: recibido y cambio
        cash = tk.Frame(self.parent, bg='white', pady=10)
        cash.pack(fill=tk.X)
        tk.Label(cash, text='Recibido:', font=('Helvetica',12), bg='white').pack(side=tk.LEFT, padx=10)
        self.received_var = tk.StringVar()
        entry = ttk.Entry(cash, textvariable=self.received_var, width=10, font=('Helvetica',12))
        entry.pack(side=tk.LEFT)
        entry.focus()
        tk.Label(cash, text='Cambio:', font=('Helvetica',12), bg='white').pack(side=tk.LEFT, padx=10)
        self.lbl_change = tk.Label(cash, text='$0.00', font=('Helvetica',12,'bold'), bg='white', fg='#28a745')
        self.lbl_change.pack(side=tk.LEFT)
        self.received_var.trace_add('write', lambda *a: self._calc_change())
        # Botones
        btnf = tk.Frame(self.parent, bg='white', pady=20)
        btnf.pack(fill=tk.X)
        ttk.Button(btnf, text='Cobrar e Imprimir', style='Primary.TButton', command=lambda: self._process(True)).pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        ttk.Button(btnf, text='Cobrar sin imprimir', style='Secondary.TButton', command=lambda: self._process(False)).pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        ttk.Button(btnf, text='Cancelar', style='Danger.TButton', command=self._cancel).pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

    def _calc_change(self):
        try:
            r = float(self.received_var.get())
            c = r - self.total
            color = '#28a745' if c>=0 else '#dc3545'
            self.lbl_change.config(text=f'$ {max(c,0):.2f}', fg=color)
        except:
            self.lbl_change.config(text='$0.00', fg='#28a745')

    def _save(self):
        fecha = datetime.date.today()
        sel = self.venta_app.client_cb.get()
        cliente = None if sel=='Venta General' else sel.split(' ')[0]
        self.cursor.execute("INSERT INTO Venta (id_venta,fecha,importe,telefono,id_usuario) VALUES (%s,%s,%s,%s,%s)",
                            (self.folio, fecha, self.total, cliente, self.usuario))
        for code, info in self.items.items():
            _, price, qty, _ = info
            self.cursor.execute("INSERT INTO DetalleVenta (id_venta,codigo,cantidad,precio) VALUES (%s,%s,%s,%s)",
                                (self.folio, code, qty, price))
        self.db.commit()

    def _process(self, impr):
        # Validar efectivo
        try:
            rec = float(self.received_var.get())
            if rec < self.total:
                messagebox.showerror('Error','Monto insuficiente')
                return
        except:
            messagebox.showerror('Error','Monto inválido')
            return
        self._save()
        if impr:
            messagebox.showinfo('Info','Impresión no disponible por el momento')
        messagebox.showinfo('Éxito','Venta registrada correctamente')
        # volver a venta
        self.venta_app.items.clear()
        self.venta_app.show_sale_ui()

    def _cancel(self):
        self.venta_app.show_sale_ui()



class VentaApp:
    def __init__(self, container, usuario=None):
        self.usuario = usuario or "Vendedor General"
        self.container = container
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()
        self.items = {}
        self.show_sale_ui()

    def _limpiar_contenedor(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_sale_ui(self):
        self._limpiar_contenedor()
        self.container.configure(bg="white")
        title = tk.Frame(self.container, bg="#F0F0F0", height=40, padx=10, pady=5)
        title.pack(side=tk.TOP, fill=tk.X)
        tk.Label(title, text="VENTAS", font=("Helvetica", 16, "bold"), bg="#F0F0F0").pack(side=tk.LEFT)

        sf = tk.Frame(self.container, bg="white", padx=10, pady=5)
        sf.pack(fill=tk.X)
        tk.Button(sf, text="Agregar Artículo", bg="#87CEEB", fg="white",
                  font=("Helvetica", 10, "bold"), command=self.show_selector_ui).pack(side=tk.LEFT)

        cols = ("codigo", "descripcion", "precio", "cantidad", "importe", "existencia")
        tf = tk.Frame(self.container, bg="white")
        tf.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tree = ttk.Treeview(tf, columns=cols, show="headings")
        for c, w in zip(cols, [100, 200, 80, 80, 80, 80]):
            self.tree.heading(c, text=c.capitalize(), anchor="center")
            self.tree.column(c, width=w, anchor="center")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Scrollbar(tf, command=self.tree.yview).pack(side=tk.LEFT, fill=tk.Y)

        bf = tk.Frame(self.container, bg="#ECECEC", height=60, padx=10, pady=5)
        bf.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(bf, text="Cliente:", bg="#ECECEC").pack(side=tk.LEFT)
        self.client_cb = ttk.Combobox(bf, state="readonly", width=25)
        self.load_clients()
        self.client_cb.pack(side=tk.LEFT, padx=5)

        tk.Button(bf, text="Eliminar Producto", bg="#ff4d4d", fg="white",
                  font=("Helvetica", 10, "bold"), command=self.del_producto).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="Vaciar Ticket", bg="#ff4d4d", fg="white",
                  font=("Helvetica", 10, "bold"), command=self.clear_ticket).pack(side=tk.LEFT, padx=5)

        totals_frame = tk.Frame(bf, bg="#ECECEC")
        totals_frame.pack(side=tk.RIGHT)
        self.lbl_sub = tk.Label(totals_frame, text="Subtotal: $0.00",
                                font=("Helvetica", 12, "bold"), bg="#ECECEC")
        self.lbl_sub.pack()
        self.lbl_tot = tk.Label(totals_frame, text="Total: $0.00",
                                font=("Helvetica", 14, "bold"), bg="#ECECEC")
        self.lbl_tot.pack()
        tk.Button(totals_frame, text="Cobrar", bg="#28a745", fg="white",
                  font=("Helvetica", 10, "bold"), width=10,
                  command=self._open_metodo_pago).pack(pady=5)

        self.refresh_ticket()

    def load_clients(self):
        self.cursor.execute("SELECT telefono, nombre FROM Cliente")
        rows = self.cursor.fetchall()
        opts = ["Venta General"] + [f"{n} ({t})" for t, n in rows]
        self.client_cb['values'] = opts
        self.client_cb.current(0)

    def show_selector_ui(self):
        self._limpiar_contenedor()
        ArticuloSelector(self.container, self.on_select)

    def on_select(self, data):
        codigo, nombre, precio, existencia = data
        if codigo in self.items:
            prev = self.items[codigo]
            if prev[2] + 1 > int(existencia):
                return messagebox.showwarning("Sin stock", "No hay suficiente existencia.")
            prev[2] += 1
        else:
            self.items[codigo] = [nombre, float(precio), 1, int(existencia)]
        self.show_sale_ui()

    def _open_metodo_pago(self):
        MetodoPagoApp(self.container, self)

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


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Ventas')
    root.state('zoomed')
    VentaApp(root, usuario='Ana Pérez')
    root.mainloop()
