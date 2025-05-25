import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import conexion  # tu módulo conexion.py
from botones import configurar_estilos



class VentanaLogin:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Iniciar sesión - Login")
        self.ventana.state("zoomed")
        self.ventana.config(bg="white")
        self.ventana.resizable(False, False)
        configurar_estilos(self.ventana)
        
        
        
        # Conexión y cursor
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()

        # Fondo y logo
        self._cargar_fondo()
        self.widget = tk.LabelFrame(self.ventana, width=400, height=500, bg="white")
        self.widget.pack(side=tk.TOP, pady=100)
        self.widget.pack_propagate(False)
        self._cargar_logo()

        # Usuario (por nombre)
        tk.Label(self.widget, text="Usuario", font=("tahoma",12,"bold"), bg="white").pack()
        self.nombre_var = tk.StringVar()
        # Configuración del estilo (hazlo una vez al inicio de tu aplicación)
        style = ttk.Style()
        style.theme_use('clam')  # Necesario para personalización

        # Estilo que replica el Combobox original pero mejorado
        style.configure('Enhanced.TCombobox',
                        font=('Tahoma', 12),
                        foreground='#000000',
                        background='#FFFFFF',
                        bordercolor='#707070',
                        arrowsize=14,
                        padding=(6, 4),
                        relief='solid',
                        borderwidth=1)

        style.map('Enhanced.TCombobox',
                fieldbackground=[('readonly', '#FFFFFF')],
                selectbackground=[('readonly', '#E1E1E1')],
                selectforeground=[('readonly', '#000000')],
                bordercolor=[('focus', '#0078D7')],
                arrowsize=[('pressed', 12), ('!pressed', 14)])

        # Versión mejorada que mantiene toda la funcionalidad original
        self.cursor.execute("SELECT nombre FROM Usuarios")
        nombres = [r[0] for r in self.cursor.fetchall()]

        self.cmb_usuario = ttk.Combobox(
            self.widget, 
            values=nombres,
            textvariable=self.nombre_var,
            font=('Tahoma', 12),
            width=23,
            style='Enhanced.TCombobox',
            state="readonly"  # Asegura que sea solo de selección
        )

        # Mantenemos todos los binds y funciones originales
        self.cmb_usuario.bind("<<ComboboxSelected>>", self._mostrar_cargo)
        self.cmb_usuario.pack(pady=5)  # Pequeño espacio adicional para mejor legibilidad

        # Opcional: Placeholder para mejor UX
        if not nombres:  # Si no hay usuarios
            self.cmb_usuario.set("-- Seleccione usuario --")
            self.cmb_usuario['state'] = 'disabled'
        else:
            self.cmb_usuario.current(0)  # Selecciona el primer item por defecto
        # Cargo mostrado
        self.cargo_label = tk.Label(self.widget, text="Cargo: ", font=("tahoma",12), bg="white")
        self.cargo_label.pack(pady=5)

        # Contraseña
        tk.Label(self.widget, text="Contraseña", font=("tahoma",12,"bold"), bg="white").pack()
        # Configuración del estilo para el Entry que coincida con el Combobox
        style = ttk.Style()
        style.theme_use('clam')

        # Estilo para Entry que coincide con el Combobox mejorado
        style.configure('Modern.TEntry',
                    font=('Tahoma', 12),
                    foreground='#000000',
                    background='#FFFFFF',
                    bordercolor='#707070',
                    padding=(6, 4),
                    relief='solid',
                    borderwidth=1)

        style.map('Modern.TEntry',
                bordercolor=[('focus', '#0078D7')],  # Borde azul al enfocar
                fieldbackground=[('!disabled', '#FFFFFF')])

        # Entry con el mismo estilo que el Combobox
        self.entry_pwd = ttk.Entry(
            self.widget, 
            show="*", 
            style='Modern.TEntry',
            width=25,
            font=('Tahoma', 12)
        )
        self.entry_pwd.pack(pady=5)
        self.var_show = tk.BooleanVar()
        tk.Checkbutton(self.widget, text="Ver contraseña", variable=self.var_show,
                       command=self._ver_contraseña, font=("tahoma",12), bg="white").pack(pady=10)

        # Botón Iniciar
        ttk.Button(self.widget, text="Iniciar Sesión", command=self._iniciar_sesion,
                  style="Exito.TButton", width=15).pack(pady=20)

    def _cargar_fondo(self):
        dir_act = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(dir_act, "imagen", "image.png")
        try:
            img = Image.open(ruta)
            w, h = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(img)
            tk.Label(self.ventana, image=self.bg_img).place(x=0, y=0, relwidth=1, relheight=1)
        except:
            pass

    def _cargar_logo(self):
        dir_act = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(dir_act, "imagen", "logoElektra.png")
        try:
            logo = Image.open(ruta).resize((200,150), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo)
            frame = tk.Frame(self.widget, bg="white", width=300, height=200)
            frame.pack(); frame.pack_propagate(False)
            tk.Label(frame, image=self.logo_img, bg="white").pack(pady=20)
        except:
            pass

    def _mostrar_cargo(self, event):
        nombre = self.nombre_var.get()
        self.cursor.execute("SELECT departamento FROM Usuarios WHERE nombre=%s", (nombre,))
        row = self.cursor.fetchone()
        cargo = row[0] if row else ''
        self.cargo_label.config(text=f"Cargo: {cargo}")

    def _ver_contraseña(self):
        self.entry_pwd.config(show='' if self.var_show.get() else '*')

    def _iniciar_sesion(self):
        nombre = self.nombre_var.get().strip()
        pwd = self.entry_pwd.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Selecciona un usuario")
            return
        if not pwd:
            messagebox.showerror("Error", "La contraseña no puede estar vacía")
            return
        self.cursor.execute("SELECT contraseña FROM Usuarios WHERE nombre=%s", (nombre,))
        row = self.cursor.fetchone()
        if not row:
            messagebox.showerror("Error", "Usuario no encontrado")
            return
        if pwd != row[0]:
            messagebox.showerror("Error", "Contraseña incorrecta")
            return
        # Login exitoso
        from menu import PuntoDeVenta
        self.widget.destroy()
        PuntoDeVenta(self.ventana, usuario=nombre).main()

    def run(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = VentanaLogin()
    app.run()



