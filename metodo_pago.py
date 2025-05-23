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
        self.usuario = usuario or "Vendedor General"
        self.venta_app = venta_app
        self.parent = container
        if venta_app:
            self.db = conexion.conectar()
            self.cursor = self.db.cursor()
            self.items = venta_app.items
            self.folio = self._siguiente_folio()
            self.total = sum(info[1] * info[2] for info in self.items.values())
        else:
            self.items = {'0001': ['Producto X', 50.0, 2, 100]}
            self.folio = 1000
            self.total = 100.0
        self._render_ui()

    def _limpiar_contenedor(self):
        for w in self.parent.winfo_children():
            w.destroy()

    def _siguiente_folio(self):
        self.cursor.execute("SELECT MAX(id_venta) FROM Venta")
        row = self.cursor.fetchone()
        ultimo = row[0] if row and row[0] is not None else 999
        return ultimo + 1

    def _render_ui(self):
        self._limpiar_contenedor()
        self.parent.configure(bg="#F0F0F0")

        # Frame principal para mejor organización
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header con estilo similar a VentaApp
        header = ttk.Frame(main_frame, style="Header.TFrame")
        header.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header, text="MÉTODO DE PAGO", font=("Helvetica", 18, "bold"), 
                 style="Header.TLabel").pack(side=tk.LEFT, padx=10)
        
        folio_frame = ttk.Frame(header)
        folio_frame.pack(side=tk.RIGHT, padx=10)
        ttk.Label(folio_frame, text="Folio:", font=("Helvetica", 12)).pack(side=tk.LEFT)
        ttk.Label(folio_frame, text=f"{self.folio}", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)

        # Sección de total con mejor diseño
        total_frame = ttk.Frame(main_frame, style="Total.TFrame")
        total_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(total_frame, text="TOTAL A PAGAR:", font=("Helvetica", 14)).pack(side=tk.LEFT, padx=10)
        ttk.Label(total_frame, text=f"$ {self.total:.2f}", font=("Helvetica", 24, "bold"), 
                 foreground="#004aad").pack(side=tk.RIGHT, padx=10)

        # Frame para los métodos de pago con mejor distribución
        pay_frame = ttk.LabelFrame(main_frame, text="Seleccione Método de Pago", 
                                 padding=(20, 10), style="Pago.TLabelframe")
        pay_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.pay_var = tk.StringVar(value="Efectivo")
        
        # Usando grid para mejor alineación
        ttk.Radiobutton(pay_frame, text="Efectivo", variable=self.pay_var, 
                        value="Efectivo", style="Pago.TRadiobutton").grid(
                            row=0, column=0, padx=20, pady=5, sticky=tk.W)
        
        ttk.Radiobutton(pay_frame, text="Crédito", variable=self.pay_var, 
                        value="Crédito", style="Pago.TRadiobutton",
                        command=lambda: messagebox.showinfo(
                            "No disponible", "Crédito no está disponible.")).grid(
                                row=0, column=1, padx=20, pady=5, sticky=tk.W)
        
        ttk.Radiobutton(pay_frame, text="Tarjeta", variable=self.pay_var, 
                        value="Tarjeta", style="Pago.TRadiobutton",
                        command=lambda: messagebox.showinfo(
                            "No disponible", "Pago con tarjeta no está disponible.")).grid(
                                row=0, column=2, padx=20, pady=5, sticky=tk.W)

        # Sección de efectivo con mejor diseño
        cash_frame = ttk.Frame(main_frame, style="Cash.TFrame")
        cash_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Usando grid para mejor organización
        ttk.Label(cash_frame, text="Monto recibido:", font=("Helvetica", 12)).grid(
            row=0, column=0, padx=(20, 5), pady=10, sticky=tk.E)
        
        self.received_var = tk.StringVar()
        entry = ttk.Entry(cash_frame, textvariable=self.received_var, 
                         font=("Helvetica", 12), width=15)
        entry.grid(row=0, column=1, padx=5, pady=10, sticky=tk.W)
        entry.focus()
        
        ttk.Label(cash_frame, text="Cambio:", font=("Helvetica", 12)).grid(
            row=0, column=2, padx=(40, 5), pady=10, sticky=tk.E)
        
        self.lbl_change = ttk.Label(cash_frame, text="$0.00", 
                                  font=("Helvetica", 14, "bold"),
                                  foreground="#28a745")
        self.lbl_change.grid(row=0, column=3, padx=(5, 20), pady=10, sticky=tk.W)
        
        self.received_var.trace_add('write', lambda *args: self._calcular_cambio())

        # Botones con mejor distribución y estilo
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Configurar estilos para los botones
        style = ttk.Style()
        style.configure("Primary.TButton", font=("Helvetica", 12, "bold"), 
                       foreground="white", background="#28a745", padding=10)
        style.configure("Secondary.TButton", font=("Helvetica", 12), 
                       padding=10)
        style.configure("Danger.TButton", font=("Helvetica", 12), 
                       foreground="white", background="#dc3545", padding=10)
        
        # Botones principales
        ttk.Button(btn_frame, text="Cobrar e Imprimir", 
                  command=lambda: self._procesar_pago(imprimir=True),
                  style="Primary.TButton").pack(
                      side=tk.LEFT, padx=10, ipadx=20, fill=tk.X, expand=True)
        
        ttk.Button(btn_frame, text="Cobrar sin imprimir", 
                  command=lambda: self._procesar_pago(imprimir=False),
                  style="Secondary.TButton").pack(
                      side=tk.LEFT, padx=10, ipadx=20, fill=tk.X, expand=True)
        
        ttk.Button(btn_frame, text="Cancelar", 
                  command=self._cancelar,
                  style="Danger.TButton").pack(
                      side=tk.LEFT, padx=10, ipadx=20, fill=tk.X, expand=True)

        # Configurar estilos adicionales
        self._configure_styles()

    def _configure_styles(self):
        style = ttk.Style()
        
        # Estilo para el header
        style.configure("Header.TFrame", background="#004aad")
        style.configure("Header.TLabel", background="#004aad", foreground="white")
        
        # Estilo para el frame de total
        style.configure("Total.TFrame", background="#e9ecef", 
                        borderwidth=2, relief="groove")
        
        # Estilo para el frame de métodos de pago
        style.configure("Pago.TLabelframe", font=("Helvetica", 12, "bold"))
        style.configure("Pago.TLabelframe.Label", font=("Helvetica", 12, "bold"))
        style.configure("Pago.TRadiobutton", font=("Helvetica", 12))
        
        # Estilo para el frame de efectivo
        style.configure("Cash.TFrame", background="#f8f9fa", 
                       borderwidth=1, relief="solid")

    def _calcular_cambio(self):
        try:
            received = float(self.received_var.get())
            change = received - self.total
            color = "#28a745" if change >= 0 else "#dc3545"
            self.lbl_change.config(text=f"$ {change:.2f}", foreground=color)
        except ValueError:
            self.lbl_change.config(text="$0.00", foreground="#28a745")

    def _guardar_venta(self):
        if not self.venta_app:
            return
        fecha = datetime.date.today()
        sel = self.venta_app.client_cb.get()
        cliente = None if sel == "Venta General" else sel.split(' ')[-1].strip('()')
        sql_v = "INSERT INTO Venta (id_venta, fecha, importe, telefono, id_usuario) VALUES (%s,%s,%s,%s,%s)"
        self.cursor.execute(sql_v, (self.folio, fecha, self.total, cliente, self.usuario))
        for codigo, info in self.items.items():
            _, precio, cantidad, _ = info
            sql_d = "INSERT INTO DetalleVenta (id_venta,codigo,cantidad,precio) VALUES (%s,%s,%s,%s)"
            self.cursor.execute(sql_d, (self.folio, codigo, cantidad, precio))
        self.db.commit()

    def _generar_ticket_pdf(self):
        try:
            folder = os.path.abspath('FOLDER_TICKETS')
            os.makedirs(folder, exist_ok=True)
            pdf_path = os.path.join(folder, f"ticket_{self.folio}.pdf")
            c = pdf_canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter
            y = height - 40
            c.setFont("Helvetica-Bold", 14)
            c.drawString(40, y, f"Ticket - Folio {self.folio}")
            y -= 20
            c.setFont("Helvetica", 10)
            c.drawString(40, y, f"Fecha: {datetime.date.today()}")
            y -= 15
            c.drawString(40, y, f"Atendido por: {self.usuario}")
            y -= 15
            client_label = self.venta_app.client_cb.get() if self.venta_app else 'General'
            c.drawString(40, y, f"Cliente: {client_label}")
            y -= 25
            c.setFont("Helvetica-Bold", 10)
            for text, x in [("Código", 40), ("Descripción", 120), ("Cant", 300), ("Precio", 350)]:
                c.drawString(x, y, text)
            y -= 15
            c.setFont("Helvetica", 10)
            for codigo, info in self.items.items():
                nombre, precio, cantidad, _ = info
                c.drawString(40, y, codigo)
                c.drawString(120, y, nombre[:25])
                c.drawString(300, y, str(cantidad))
                c.drawString(350, y, f"{precio:.2f}")
                y -= 15
                if y < 40:
                    c.showPage()
                    y = height - 40
            c.save()
            return pdf_path
        except Exception as e:
            messagebox.showerror("Error al generar PDF", str(e))
            return None

    def _procesar_pago(self, imprimir=False):
        if self.pay_var.get() == "Efectivo":
            try:
                received = float(self.received_var.get())
                if received < self.total:
                    messagebox.showerror("Error", "El monto recibido es menor al total.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido.")
                return
        
        self._guardar_venta()
        pdf_path = self._generar_ticket_pdf() if imprimir else None
        if imprimir and pdf_path:
            messagebox.showinfo("Éxito", f"Compra realizada correctamente.\nPDF guardado en:\n{pdf_path}")
        else:
            messagebox.showinfo("Éxito", "Compra realizada correctamente.")
        if self.venta_app:
            self.venta_app.items.clear()
            self.venta_app.show_sale_ui()
        else:
            self._render_ui()

    def _cancelar(self):
        if self.venta_app:
            self.venta_app.show_sale_ui()
        else:
            self.parent.destroy()

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
