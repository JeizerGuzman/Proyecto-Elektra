import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import conexion  # tu módulo conexion.py

class VentanaLogin:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Iniciar sesión - Login")
        self.ventana.state("zoomed")
        self.ventana.config(bg="white")
        self.ventana.resizable(False, False)

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
        # Carga nombres desde BD
        self.cursor.execute("SELECT nombre FROM Usuarios")
        nombres = [r[0] for r in self.cursor.fetchall()]
        self.cmb_usuario = ttk.Combobox(self.widget, values=nombres, textvariable=self.nombre_var)
        self.cmb_usuario.config(font=("tahoma",12), width=23)
        self.cmb_usuario.bind("<<ComboboxSelected>>", self._mostrar_cargo)
        self.cmb_usuario.pack()

        # Cargo mostrado
        self.cargo_label = tk.Label(self.widget, text="Cargo: ", font=("tahoma",12), bg="white")
        self.cargo_label.pack(pady=5)

        # Contraseña
        tk.Label(self.widget, text="Contraseña", font=("tahoma",12,"bold"), bg="white").pack()
        self.entry_pwd = tk.Entry(self.widget, show="*", font=("tahoma",12), width=25)
        self.entry_pwd.pack()
        self.var_show = tk.BooleanVar()
        tk.Checkbutton(self.widget, text="Ver contraseña", variable=self.var_show,
                       command=self._ver_contraseña, font=("tahoma",12), bg="white").pack(pady=10)

        # Botón Iniciar
        tk.Button(self.widget, text="Iniciar Sesión", command=self._iniciar_sesion,
                  fg="white", bg="green", font=("tahoma",12), width=15).pack(pady=20)

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



