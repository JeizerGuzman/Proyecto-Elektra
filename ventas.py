import tkinter as tk
from tkinter import ttk, messagebox,simpledialog 
import conexion  # Asegúrate de que conexion.py está en el mismo directorio
from seleccionar_articulo import ArticuloSelector
from metodo_pago import MetodoPagoApp
from botones import configurar_estilos


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
        configurar_estilos(self.container)
        
        
        
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

    
    def add_article(self, codigo, nombre, precio, existencia, cantidad=1):
        """Función auxiliar para agregar artículos al ticket"""
        
        if codigo in self.items:
            new_cantidad = self.items[codigo][2] + cantidad
            if new_cantidad > existencia:
                messagebox.showwarning("Sin stock", "No hay suficiente existencia.")
                return False
            self.items[codigo][2] = new_cantidad
        else:
            self.items[codigo] = [nombre, float(precio), cantidad, int(existencia)]
        self.refresh_ticket()
        return True

    def handle_barcode_entry(self, event):
        """Maneja la entrada de código de barras"""
        codigo = self.barcode_entry.get().strip()
        
        # Validar longitud del código
        if len(codigo) not in (12, 13):
            messagebox.showwarning("Código inválido", "El código debe tener 12 o 13 dígitos.")
            self.barcode_entry.delete(0, tk.END)
            return
            
        try:
            # Buscar artículo en la base de datos
            self.cursor.execute(
                "SELECT nombre, precio, existencia FROM Articulo WHERE codigo = %s",
                (codigo,)
            )
            row = self.cursor.fetchone()
            
            if not row:
                messagebox.showwarning("Artículo no registrado", "El código no existe en la base de datos.")
                self.barcode_entry.delete(0, tk.END)
                return
                
            nombre, precio, existencia = row
            
            # Pedir cantidad al usuario
            cantidad = simpledialog.askinteger(
                "Cantidad",
                "Ingrese la cantidad:",
                parent=self.container,
                minvalue=1,
                initialvalue=1
            )
            
            if cantidad and self.add_article(codigo, nombre, precio, existencia, cantidad):
                self.barcode_entry.delete(0, tk.END)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar artículo: {str(e)}")

    
    
    def show_sale_ui(self):
        self._limpiar_contenedor()
        self.container.configure(bg="white")

        # Título
        title = tk.Frame(self.container, bg="#8FC9DB", height=40, padx=10, pady=5)
        title.pack(side=tk.TOP, fill=tk.X)
        tk.Label(title, text="VENTAS", font=("Tahoma",14,"bold"),fg="white", bg="#8FC9DB").pack(side=tk.LEFT)

        # Botón Agregar Artículo
        sf = tk.Frame(self.container, bg="white", padx=10, pady=5)
        sf.pack(fill=tk.X)
        
        tk.Label(sf, text="Código de barras:", bg="white",font=("tahoma",10)).pack(side=tk.LEFT)
        self.barcode_entry = ttk.Entry(sf, width=20)
        self.barcode_entry.pack(side=tk.LEFT, padx=5)
        self.barcode_entry.bind("<Return>", self.handle_barcode_entry)
        
        
        ttk.Button(sf, text="Agregar Artículo", style="Azul.TButton", command=self.show_selector_ui).pack(side=tk.LEFT)

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

        # Configuración del estilo (hazlo una vez al inicio de tu aplicación)
        style = ttk.Style()
        style.theme_use('clam')  # Necesario para personalización

        # Estilo personalizado para el Combobox
        style.configure('Modern.TCombobox',
                        font=('Segoe UI', 10),
                        foreground='#2C3E50',  # Color texto
                        background='#FFFFFF',   # Color fondo
                        bordercolor='#BDC3C7', # Color borde
                        lightcolor='#BDC3C7',
                        darkcolor='#BDC3C7',
                        arrowsize=12,          # Tamaño flecha desplegable
                        padding=(8, 4),        # Padding interno
                        relief='flat')         # Estilo del borde

        style.map('Modern.TCombobox',
                fieldbackground=[('readonly', '#FFFFFF')],
                selectbackground=[('readonly', '#E8F4F8')],  # Color selección
                selectforeground=[('readonly', '#2C3E50')],
                bordercolor=[('focus', '#3498DB')],  # Color borde al enfocar
                arrowsize=[('pressed', 10), ('!pressed', 12)])

        # Área inferior mejorada
        bf = tk.Frame(self.container, bg="#F8F9FA", height=70, padx=15, pady=10)  # Fondo más claro
        bf.pack(side=tk.BOTTOM, fill=tk.X)

        # Etiqueta con mejor tipografía
        tk.Label(bf, 
                text="CLIENTE:", 
                bg="#F8F9FA",
                font=('Arial black', 12, 'bold'),
                fg="#000000").pack(side=tk.LEFT, padx=(0, 10))

        # Combobox mejorado
        self.client_cb = ttk.Combobox(
            bf, 
            state="readonly", 
            width=28,
            height=10,  # Altura del dropdown
            style='Modern.TCombobox',
            font=('Tahoma', 10)
        )
        self.load_clients()
        self.client_cb.pack(side=tk.LEFT, padx=5)

        # Añadir ícono opcional (requiere tener la imagen)
        try:
            client_icon = tk.PhotoImage(file='client_icon.png').subsample(20, 20)
            tk.Label(bf, image=client_icon, bg="#F8F9FA").pack(side=tk.LEFT, padx=(10, 0))
        except:
            pass  # Si no hay ícono, continuar sin él

        # Eliminar y vaciar
        ttk.Button(sf, text="Eliminar Articulo", style="Turquesa.TButton", command=self.del_producto).pack(side=tk.LEFT, padx=15)
        ttk.Button(bf, text="Vaciar Ticket", style="Peligro.TButton", command=self.clear_ticket).pack(side=tk.LEFT, padx=5)

        # Subtotal y Total
        totals_frame = tk.Frame(bf, bg="#FFFFFF")
        totals_frame.pack(side=tk.RIGHT)
        self.lbl_sub = tk.Label(totals_frame, text="Subtotal: $0.00",
                                font=("Tahoma",12,"bold"), bg="#FFFFFF")
        #self.lbl_sub.pack()
        self.lbl_tot = tk.Label(totals_frame, text="Total: $0.00",
                                font=("Tahoma",14,"bold"), bg="#FFFFFF")
        self.lbl_tot.pack()
        # Botón Cobrar
        ttk.Button(totals_frame, text="Cobrar",style="Exito.TButton", width=10,
                  command=self._open_metodo_pago).pack(pady=5)

        self.refresh_ticket()
        self.container.bind_all('<Alt_L>', lambda event: self.show_selector_ui())


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
        self.client_cb.set(default)
        

    def show_selector_ui(self):
        self._limpiar_contenedor()
        ArticuloSelector(
            self.container, 
            on_select_callback=self.on_select,
            on_cancel_callback=self.show_sale_ui  # Para volver al módulo de ventas
        )

    def on_select(self, data):
        if len(data) == 5:
            codigo, nombre, precio, existencia, cantidad = data
        else:
            codigo, nombre, precio, existencia = data
            cantidad = 1
        # Verifica si el Treeview existe antes de actualizarlo
        if hasattr(self, 'tree') and self.tree.winfo_exists():
            success = self.add_article(codigo, nombre, precio, existencia)
            if success:
                self.refresh_ticket()
            else:
                messagebox.showwarning("Error", "No se pudo agregar el artículo")
        else:
            # Si no existe la interfaz, recrea la vista de ventas
            self.show_sale_ui()
            self.add_article(codigo, nombre, precio, existencia, cantidad)

    def _open_metodo_pago(self):
        # Abrir Toplevel para método de pago
        top = tk.Toplevel(self.container)
        top.title('Método de Pago')
        # Prepara datos
# Asegura que el valor actual es el que está en pantalla, incluso si se redibujó
        try:
            cliente_disp = self.client_cb.get()
            cliente_tel = self.client_map.get(cliente_disp, '0000000000')  # valor por defecto si no está
            cliente_nombre = cliente_disp.split(' (')[0]
        except Exception:
            cliente_disp = "Venta General (0000000000)"
            cliente_tel = "0000000000"
            cliente_nombre = "Venta General"
            
        total = sum(info[1] * info[2] for info in self.items.values())
        productos = [ {'codigo':c, 'precio':info[1], 'cantidad':info[2]} for c,info in self.items.items() ]
        venta_data = {
            'usuario_id': self.usuario_id,
            'cliente_telefono': cliente_tel,
            'cliente_nombre': cliente_nombre,
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
        
        #importe
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
