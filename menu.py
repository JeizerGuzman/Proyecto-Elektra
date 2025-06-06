import tkinter as tk
from tkinter import ttk, messagebox
from ventas import VentaApp  # Importa la función de ventas
from clientes import ClienteApp  # Importa la clase de clientes
from PIL import Image, ImageTk
from contraseña import VentanaLogin
from proveedores import ProveedorApp
from configuracion import ConfiguracionesApp
from datetime import datetime
import locale
from inventario import InventarioApp
from historial import HistorialApp
from botones import configurar_estilos




class PuntoDeVenta:
    def __init__(self, root=None,usuario="Administrador"):
        self.usuario = usuario
        self.root = root if root else tk.Tk()
        self.root.title("Punto de Venta - Elektra")
        self.root.state("zoomed") 
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        configurar_estilos(root)
        
        
    def on_salir(self):
        self.root.destroy()

    def cambiar_usuario(self):
        self.root.destroy()  # Cierra la ventana actual del menú
        login = VentanaLogin()  # Crea una nueva instancia de login
        login.run()  # Inicia el mainloop de login


    def on_articulos(self):
        self._limpiar_contenedor()
        tk.Label(self.frame_contenedor, text="Aquí irá la configuración de los Articulos",
                 font=("Tahoma", 20), bg="white").pack(pady=50)

    def on_inventario(self):
        InventarioApp(self.frame_contenedor)

    def on_proveedores(self):
        self._limpiar_contenedor()
        ProveedorApp(self.frame_contenedor)


    def on_venta(self):
        self._limpiar_contenedor()
        VentaApp(self.frame_contenedor,self.usuario)

    def on_clientes(self):
        self._limpiar_contenedor()
        ClienteApp(self.frame_contenedor)

    def _limpiar_contenedor(self):
        for widget in self.frame_contenedor.winfo_children():
            widget.destroy()

    def on_configuracion(self):
        if not self.usuario == "Administrador":
            messagebox.showinfo("Acceso Denegado","Solo el Administrador puede Ingresar a configuraciones")
        else:
            self._limpiar_contenedor()
            ConfiguracionesApp(self.frame_contenedor)

    def on_reportes(self):
        self._limpiar_contenedor()
        HistorialApp(self.frame_contenedor)

    def actualizar_fecha_hora(self):
            # Configurar la localización a español}
            try:
                locale.setlocale(locale.LC_TIME, "Spanish_Spain.1252")  # Para Windows
            except:
                # Si falla, se utilizará la localización por defecto.
                pass
            
            # Se obtiene la fecha y hora actual
            ahora = datetime.now()
            # Formato para la fecha, por ejemplo "14/04/2025"
            fecha_str = ahora.strftime("%A %d de %B de %Y").lower()  
            # Formato para la hora en formato de 12 horas con AM/PM, por ejemplo "02:45:30 PM"
            ahora = datetime.now()
            hora = ahora.strftime("%I:%M:%S")
            indicador = "AM" if ahora.hour < 12 else "PM"
            hora_str = f"{hora} {indicador}"
            
            # Actualizar las etiquetas
            self.lbl_fecha.config(text=fecha_str)
            self.lbl_hora.config(text=hora_str)
            
            # Se programa la función para que se ejecute de nuevo en 1000 ms (1 segundo)
            self.root.after(1000, self.actualizar_fecha_hora)

    def main(self):
        # Cabecera
        cabecera = tk.Frame(self.root, bg="#394F66", height=30)
        cabecera.pack(side=tk.TOP, fill=tk.X)
        tk.Label(cabecera, text="Punto de Venta Elektra", font=("Tahoma", 10, "bold"), bg="#394F66",fg="#FFFFFF").pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(cabecera, text=f"Atiende: {self.usuario} ", font=("Tahoma", 10, "bold"), bg="#394F66",fg="#FFFFFF").pack(side=tk.RIGHT, padx=10, pady=5)

        # Menú
        menu = tk.Frame(self.root, bg="#FFFFFF", height=40)
        menu.pack(side=tk.TOP, fill=tk.X)

        # Definimos los botones con sus comandos
        botones = [
            ("Ventas", self.on_venta, "Indigo"),          # Azul para Ventas
            ("Clientes", self.on_clientes, "Indigo"),  # Verde oscuro para Clientes
            ("Inventario", self.on_inventario, "Indigo"), # Morado para Inventario
            ("Proveedores", self.on_proveedores, "Indigo"), # Naranja para Proveedores
            ("Historial", self.on_reportes, "Indigo"),      # Cian para Historial
            ("Configuración", self.on_configuracion, "Gris") # Gris para Configuración
        ]

        for texto, comando, color in botones:
            btn = ttk.Button(
                menu,
                text=texto,
                style=f"{color}.TButton",
                command=comando,
                width=12  # Mantenemos el ancho que tenías originalmente
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        # Botones lado derecho
        ttk.Button(menu, text="Salir", style="Peligro.TButton", width=10, command=self.on_salir).pack(side=tk.RIGHT, padx=5)
        ttk.Button(menu, text="Cambiar Usuario", style="Cian.TButton", width=15, command=self.cambiar_usuario).pack(side=tk.RIGHT, padx=5)
        

        # Frame contenedor
        self.frame_contenedor = tk.Frame(self.root, bg="white")
        self.frame_contenedor.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame_horario= tk.Frame(self.root,bg="black",height=70)
        self.frame_horario.pack(side=tk.TOP, fill=tk.BOTH)
        
                # Etiqueta para la fecha (alineada a la izquierda)
        self.lbl_fecha = tk.Label(self.frame_horario, bg="black", fg="white", font=("tahoma", 16))
        self.lbl_fecha.pack(side=tk.LEFT, padx=10)
        
        # Etiqueta para la hora (alineada a la derecha)
        self.lbl_hora = tk.Label(self.frame_horario, bg="black", fg="white", font=("tahoma", 16))
        self.lbl_hora.pack(side=tk.RIGHT, padx=10)
        
        # Iniciar actualización de fecha y hora
        self.actualizar_fecha_hora()
        
        # Vista por defecto
        self.on_venta()

        self.root.mainloop()

if __name__ == "__main__":
    app = PuntoDeVenta()
    app.main()