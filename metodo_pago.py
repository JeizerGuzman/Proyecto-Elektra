import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import os
from PIL import Image, ImageDraw, ImageFont
from conexion import conectar
from botones import configurar_estilos

class MetodoPagoApp:
    """
    Módulo de método de pago en Tkinter, estilo punto de venta.
    Parámetros de inicio:
        container: Tk o Toplevel donde se mostrará la UI.
        venta_data: dict con claves usuario_id, cliente_telefono, total, productos.
        on_finish_callback: función a ejecutar al cerrar módulo.
    """
    def __init__(self, container, venta_data, on_finish_callback=None, usuario_nombre=None):
        self.parent = container
        self.venta_data = venta_data
        self.on_finish = on_finish_callback
        self.usuario = usuario_nombre or f"Usuario {venta_data.get('usuario_id', '')}"
        configurar_estilos(self.parent)
        
        
        # Conexión BD
        self.db = conectar()
        self.cursor = self.db.cursor()
        # Folio y total
        self.folio = self._siguiente_folio()
        self.total = venta_data.get('total', 0.00)

        # Valores dinámicos
        self.received_var = tk.StringVar()
        self.change_var = tk.StringVar(value="$0.00")
        self.pay_method = tk.StringVar(value="Efectivo")

        self._render_ui()

    def _siguiente_folio(self):
        self.cursor.execute("SELECT MAX(id_venta) FROM Venta")
        row = self.cursor.fetchone()
        ultimo = row[0] if row and row[0] is not None else 0
        return ultimo + 1

    def _render_ui(self):
        # Limpiar contenedor
        for w in self.parent.winfo_children(): w.destroy()

        # Maximizar ventana
        try: self.parent.state('zoomed')
        except: pass
        self.parent.configure(bg="#F0F0F0")

        # Estilos ttk
        style = ttk.Style(self.parent)
        style.configure("Success.TButton", font=(None,12), padding=10)
        style.map("Success.TButton", background=[('!disabled','#28a745'),('active','#218838')])
        style.configure("Danger.TButton", font=(None,12), padding=10)
        style.map("Danger.TButton", background=[('!disabled','#dc3545'),('active','#c82333')])

        # Header
        header = ttk.Frame(self.parent)
        header.pack(fill=tk.X)
        ttk.Label(header, text="MÉTODO DE PAGO", font=(None,18,'bold'), background="#004aad", foreground="white").pack(side=tk.LEFT, fill=tk.X, expand=True, pady=10)
        ttk.Label(header, text=f"Folio: {self.folio}", font=(None,12,'bold'), background="#004aad", foreground="white").pack(side=tk.RIGHT, padx=20)

        # Total
        ttk.Label(self.parent, text=f"Total a pagar: $ {self.total:.2f}", font=(None,24,'bold'), foreground="#004aad").pack(pady=20)

        # Método de pago (solo efectivo habilitado)
        met_frame = ttk.LabelFrame(self.parent, text="Método de Pago", padding=10)
        met_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Radiobutton(met_frame, text="Efectivo", variable=self.pay_method, value="Efectivo").pack(anchor=tk.W)
        for m in ["Tarjeta", "Transferencia", "MercadoPago"]:
            ttk.Radiobutton(met_frame, text=m, variable=self.pay_method, value=m, state=tk.DISABLED).pack(anchor=tk.W)

        # Monto recibido y cambio
        amt_frame = ttk.Frame(self.parent)
        amt_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(amt_frame, text="Monto recibido:").pack(side=tk.LEFT)
        ttk.Entry(amt_frame, textvariable=self.received_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(amt_frame, text="Cambio:").pack(side=tk.LEFT, padx=(20,5))
        ttk.Label(amt_frame, textvariable=self.change_var, font=(None,12,'bold')).pack(side=tk.LEFT)
        self.received_var.trace_add('write', lambda *args: self._calcular_cambio())

        # Botones de acción
        btn_frame = ttk.Frame(self.parent)
        btn_frame.pack(fill=tk.X, padx=20, pady=20)
        ttk.Button(btn_frame, text="Cobrar e Imprimir", command=lambda: self._procesar_pago(imprimir=True), style="Turquesa.TButton",width=25).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Cobrar sin imprimir", command=lambda: self._procesar_pago(imprimir=False), style="Naranja.TButton",width=25).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=self._cancelar, style="Peligro.TButton",width=10).pack(side=tk.RIGHT, padx=15)

    def _calcular_cambio(self):
        try:
            rec = float(self.received_var.get())
            cambio = rec - self.total
            self.change_var.set(f"$ {max(cambio,0):.2f}")
        except:
            self.change_var.set("$0.00")

    def _guardar_venta(self):
        # Inserta Venta y DetalleVenta
        self.cursor.execute(
            "INSERT INTO Venta (id_venta, fecha, importe, telefono, id_usuario) VALUES (%s,%s,%s,%s,%s)",
            (self.folio, date.today(), self.total, self.venta_data.get('cliente_telefono',''), self.venta_data.get('usuario_id',0))
        )
        for prod in self.venta_data.get('productos', []):
            self.cursor.execute(
                "INSERT INTO DetalleVenta (id_venta, codigo, cantidad, precio) VALUES (%s,%s,%s,%s)",
                (self.folio, prod['codigo'], prod['cantidad'], prod['precio'])
            )
        self.db.commit()

    def _generar_ticket_png(self):
        folder = 'FOLDER_TICKETS'
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"ticket_{self.folio}.png")
        img = Image.new('RGB', (600, 800), 'white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        y = 20
        draw.text((20,y), f"Ticket Folio: {self.folio}", font=font, fill='black')
        y += 30
        draw.text((20,y), f"Fecha: {date.today()}", font=font, fill='black')
        y += 20
        draw.text((20,y), f"Atendido por: {self.usuario}", font=font, fill='black')
        y += 20
        draw.text((20,y), f"Cliente: {self.venta_data.get('cliente_telefono','Venta General')}", font=font, fill='black')
        y += 30
        headers = [("Código",20), ("Cant",200), ("Precio",300)]
        for h, x in headers: draw.text((x,y), h, font=font, fill='black')
        y += 20
        for p in self.venta_data.get('productos',[]):
            draw.text((20,y), p['codigo'], font=font, fill='black')
            draw.text((200,y), str(p['cantidad']), font=font, fill='black')
            draw.text((300,y), f"{p['precio']:.2f}", font=font, fill='black')
            y += 20
        img.save(path)

    def _procesar_pago(self, imprimir=False):
        try:
            self._guardar_venta()
            if imprimir:
                self._generar_ticket_png()
            messagebox.showinfo("Éxito", "Venta registrada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar pago: {e}")
        finally:
            if callable(self.on_finish): self.on_finish()
            self.parent.destroy()

    def _cancelar(self):
        if callable(self.on_finish): self.on_finish()
        self.parent.destroy()

    def run(self):
        self.parent.mainloop()


# Ejemplo de uso:
# root = tk.Tk()
# venta_data = {
#     'usuario_id': 1,
#     'cliente_telefono': 'Venta General',
#     'total': 150.00,
#     'productos': [
#         {'codigo':'A123','precio':100.0,'cantidad':1},
#         {'codigo':'B456','precio':50.0,'cantidad':1}
#     ]
# }
# def refrescar(): pass
# app = MetodoPagoApp(root, venta_data, refrescar, usuario_nombre='Juan')
# app.run()
