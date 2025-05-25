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
        self.parent.configure(bg="#FFFFFF")

        # Header
        header = tk.Frame(self.parent,bg="#FFFFFF")
        header.pack(fill=tk.X)
        ttk.Label(header, text="MÉTODO DE PAGO", font=("Tahoma",18,'bold'), background="#004aad", foreground="white").pack(side=tk.LEFT, fill=tk.X, expand=True, pady=10)
        ttk.Label(header, text=f"Folio: {self.folio}", font=("Tahoma",18,'bold'), background="#004aad", foreground="white").pack(side=tk.RIGHT, padx=20)

        # Total
        ttk.Label(self.parent, text=f"Total a pagar: $ {self.total:.2f}", font=("Tahoma",24,'bold'), foreground="#004aad",background="#FFFFFF").pack(pady=20)


        # Configura el estilo primero (hazlo una vez al inicio de tu aplicación)
        style = ttk.Style()
        style.theme_use('clam')  # Necesario para personalización avanzada

        # Configuración específica para el LabelFrame y RadioButtons
        style.configure('Payment.TLabelframe', 
                    font=('Tahoma', 22, 'bold'),
                    borderwidth=2,
                    relief='groove',
                    foreground="#000000",  # Color texto
                    background="#FFFFFF")  # Color fondo

        style.configure('Payment.TRadiobutton',
                    font=('Tahoma', 10),
                    foreground="#000000",
                    padding=(5, 2),
                    background="#FFFFFF")

        style.map('Payment.TRadiobutton',
                foreground=[('disabled', '#95A5A6')])  # Color para opciones deshabilitadas

        # Creación del frame con el nuevo estilo
        met_frame = ttk.LabelFrame(
            self.parent, 
            text="MÉTODO DE PAGO",  # Texto en mayúsculas para mejor jerarquía
            style='Payment.TLabelframe',
            padding=(15, 10, 15, 10)  # Padding: (left, top, right, bottom)
        )
        met_frame.pack(fill=tk.X, padx=20, pady=10, ipady=5)  # ipady agrega padding interno vertical

        # RadioButtons con estilo mejorado
        ttk.Radiobutton(
            met_frame, 
            text="EFECTIVO", 
            variable=self.pay_method, 
            value="Efectivo",
            style='Payment.TRadiobutton'
        ).pack(anchor=tk.W, pady=3)  # Pequeño espacio entre opciones
        
        
        for m in ["Tarjeta", "Transferencia", "MercadoPago"]:
            ttk.Radiobutton(
                met_frame, 
                text=m.upper(),  # Texto en mayúsculas
                variable=self.pay_method, 
                value=m, 
                state=tk.DISABLED,
                style='Payment.TRadiobutton'
            ).pack(anchor=tk.W, pady=3)

        # Monto recibido y cambio
        amt_frame = tk.Frame(self.parent,bg="#FFFFFF")
        amt_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(amt_frame, text="Monto recibido:",background="#FFFFFF",font=("Tahoma",12,'bold')).pack(side=tk.LEFT)
        ttk.Entry(amt_frame, textvariable=self.received_var, width=10,font=("Tahoma",12)).pack(side=tk.LEFT, padx=5)
        ttk.Label(amt_frame, text="Cambio:",background="#FFFFFF").pack(side=tk.LEFT, padx=(20,5))
        ttk.Label(amt_frame, textvariable=self.change_var, font=("Tahoma",12,'bold'),background="#FFFFFF").pack(side=tk.LEFT)
        self.received_var.trace_add('write', lambda *args: self._calcular_cambio())

        # Botones de acción
        btn_frame = tk.Frame(self.parent,bg="#FFFFFF")
        btn_frame.pack(fill=tk.X, padx=20, pady=20)
        ttk.Button(btn_frame, text="Cobrar e Imprimir", command=lambda: self._procesar_pago(imprimir=True), 
                   style="Turquesa.TButton",width=25).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Cobrar sin imprimir", command=lambda: self._procesar_pago(imprimir=False), 
                   style="Naranja.TButton",width=25).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=self._cancelar, 
                   style="Peligro.TButton",width=10).pack(side=tk.RIGHT, padx=15)

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
        from PIL import ImageFont, ImageDraw, Image
        import os
        from datetime import date

        folder = 'FOLDER_TICKETS'
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"ticket_{self.folio}.png")

        width, height = 600, 800
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)

        try:
            font_title = ImageFont.truetype("arial.ttf", 32)
            font_subtitle = ImageFont.truetype("arial.ttf", 18)
            font_text = ImageFont.truetype("arial.ttf", 14)
            font_bold = ImageFont.truetype("arialbd.ttf", 16)
        except:
            font_title = font_subtitle = font_text = font_bold = ImageFont.load_default()

        telefono = self.venta_data.get('cliente_telefono', 'Venta General')

        y = 20
        draw.text((width//2 - 40, y), "Elektra", font=font_title, fill='black')
        y += 40
        draw.text((20, y), f"Folio: {self.folio}", font=font_text, fill='black')
        draw.text((400, y), f"Fecha: {date.today()}", font=font_text, fill='black')
        y += 25
        draw.text((20, y), f"Cliente: {telefono}", font=font_text, fill='black')
        y += 25
        draw.text((20, y), f"Atendido por: {self.usuario}", font=font_text, fill='black')
        y += 30

        draw.line([(20, y), (580, y)], fill='black', width=1)
        y += 10

        draw.text((20, y), "Código", font=font_bold, fill='black')
        draw.text((150, y), "Cantidad", font=font_bold, fill='black')
        draw.text((250, y), "Precio", font=font_bold, fill='black')
        draw.text((350, y), "Total", font=font_bold, fill='black')
        y += 25

        draw.line([(20, y), (580, y)], fill='black', width=1)
        y += 10

        for prod in self.venta_data.get('productos', []):
            total_prod = prod['precio'] * prod['cantidad']
            draw.text((20, y), prod['codigo'], font=font_text, fill='black')
            draw.text((150, y), str(prod['cantidad']), font=font_text, fill='black')
            draw.text((250, y), f"${prod['precio']:.2f}", font=font_text, fill='black')
            draw.text((350, y), f"${total_prod:.2f}", font=font_text, fill='black')
            y += 25

        y += 10
        draw.line([(20, y), (580, y)], fill='black', width=1)
        y += 10

        draw.text((250, y), "TOTAL:", font=font_bold, fill='black')
        draw.text((350, y), f"${self.total:.2f}", font=font_bold, fill='black')

        y += 40
        draw.text((width//2 - 100, y), "¡Gracias por su compra!", font=font_subtitle, fill='black')

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
