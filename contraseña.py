import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os


class VentanaLogin:
    def __init__(self):
        self.ventana_contraseña = tk.Tk()
        self.ventana_contraseña.title("Inicar sesion - Login")
        self.ventana_contraseña.state("zoomed")
        self.ventana_contraseña.config(bg="white")
        self.ventana_contraseña.resizable(False, False)

        self.ventana_contraseña.update()
        self.ancho_ventana = self.ventana_contraseña.winfo_width()
        self.alto_ventana = self.ventana_contraseña.winfo_height()
        
        
        # Obtiene el directorio donde se encuentra el script actual
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta relativa a la imagen
        ruta_imagen = os.path.join(directorio_actual, "imagen", "image.png")
        
        try:
            self.imagen_original = Image.open(ruta_imagen)
        except IOError:
            messagebox.showerror("Error", "No se pudo cargar la imagen. Verifica la ruta o los recursos.")
            # Aquí puedes definir una acción alternativa, como cargar una imagen por defecto
        
        self.imagen_fondo_redimensionada = self.imagen_original.resize(
            (self.ancho_ventana, self.alto_ventana), resample=Image.Resampling.LANCZOS
        )
        self.bg_image = ImageTk.PhotoImage(self.imagen_fondo_redimensionada)

        self.bg_label = tk.Label(self.ventana_contraseña, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        self.widget_central = tk.LabelFrame(self.ventana_contraseña, text="")
        self.widget_central.config(width=400, height=500)
        self.widget_central.pack(side=tk.TOP, pady=100)
        self.widget_central.pack_propagate(False)

        self.relleno2 = tk.Frame(self.widget_central, width=300, height=200)
        self.relleno2.pack()
        self.relleno2.pack_propagate(False)

        # Obtiene el directorio donde se encuentra el script actual
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta relativa a la imagen
        ruta_imagen = os.path.join(directorio_actual, "imagen", "logoElektra.png")

        self.imagen_logo = Image.open(ruta_imagen)
        self.imagen_logo_redimensionada = self.imagen_logo.resize(
            (200, 150), resample=Image.Resampling.LANCZOS
        )
        self.imagen_relleno = ImageTk.PhotoImage(self.imagen_logo_redimensionada)

        self.lbl_imagen_relleno = tk.Label(self.relleno2, image=self.imagen_relleno)
        self.lbl_imagen_relleno.pack(expand=True, pady=20)

        self.lbl_nombre_usuario = tk.Label(self.widget_central, text="Usuario")
        self.lbl_nombre_usuario.config(font=("tahoma", 12, "bold"), height=2)
        self.lbl_nombre_usuario.pack()

        self.variable_usuarios = tk.StringVar()
        self.usuarios = ["Administrador", "Gerente"]
        self.seleccionar_usuario = ttk.Combobox(
            self.widget_central,
            values=self.usuarios,
            textvariable=self.variable_usuarios
        )
        self.seleccionar_usuario.config(font=("tahoma", 12), width=23)
        self.seleccionar_usuario.pack()

        self.lbl_contraseña = tk.Label(self.widget_central, text="Contraseña")
        self.lbl_contraseña.config(font=("tahoma", 12, "bold"), height=2)
        self.lbl_contraseña.pack()

        self.entry_contraseña = tk.Entry(self.widget_central, show="*")
        self.entry_contraseña.config(font=("tahoma", 12), width=25)
        self.entry_contraseña.pack()

        self.variable_contraseña = tk.BooleanVar()
        self.ver_contraseña = tk.Checkbutton(
            self.widget_central,
            text="Ver contraseña",
            variable=self.variable_contraseña,
            command=self.ver_contraseña_func
        )
        self.ver_contraseña.config(font=("tahoma", 12), width=25)
        self.ver_contraseña.pack(pady=10)

        self.btn_iniciar_sesion = tk.Button(
            self.widget_central,
            text="Iniciar Sesion",
            command=self.iniciar_sesion
        )
        self.btn_iniciar_sesion.config(fg="white", bg="green", font=("tahoma", 12), width=15)
        self.btn_iniciar_sesion.pack(pady=20)

    def limpiar_ventana(self):
        for widget in self.ventana_contraseña.winfo_children():
            widget.destroy()

    def ver_contraseña_func(self):
        if self.variable_contraseña.get():
            self.entry_contraseña.config(show="")
        else:
            self.entry_contraseña.config(show="*")

    def iniciar_sesion(self):
        from menu import PuntoDeVenta
        usuario_encontrado = 0
        contraseña = "7"
        for usuario in self.usuarios:
            if usuario == self.variable_usuarios.get():
                usuario_encontrado = 1

        self.usuario_seleccionado = self.variable_usuarios.get()
        if usuario_encontrado == 0:
            messagebox.showerror("Error", "El usuario no existe")
        elif len(self.entry_contraseña.get()) == 0:
            messagebox.showerror("Error", "La contraseña no tiene que tener campos vacíos")
        elif not self.entry_contraseña.get() == contraseña:
            messagebox.showerror("Error", "Contraseña Incorrecta")
        else:
            self.limpiar_ventana()
            PuntoDeVenta(self.ventana_contraseña,usuario=self.usuario_seleccionado).main()

    def run(self):
        self.ventana_contraseña.mainloop()


if __name__ == "__main__":
    app = VentanaLogin()
    app.run()



