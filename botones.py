"""
Módulo de estilos y paleta de colores extendida para Punto de Venta.
Mantiene el mismo diseño original pero con más opciones de colores.
"""
import tkinter as tk
from tkinter import ttk

# Paleta de colores extendida (conservando los originales y añadiendo nuevos)
PALETA_COLORES = {
    # Colores originales
    'AZUL':             '#007bff',
    'GRIS':             '#6c757d',
    'VERDE':            '#28a745',
    'ROJO':             '#dc3545',
    'AMARILLO':         '#ffc107',
    
    # Nuevos colores añadidos
    'CIAN':             '#17a2b8',
    'MORADO':           '#6f42c1',
    'ROSA':             '#e83e8c',
    'NARANJA':          '#fd7e14',
    'INDIGO':           '#6610f2',
    'TURQUESA':         '#20c997',
    'AZUL_OSCURO':      '#0056b3',
    'VERDE_OSCURO':     '#1e7e34',
    'AZUL_CIELO':       '#87CEFA',
    # Colores neutros (originales)
    'TEXTO_OSCURO':     '#212529',
    'FONDO_PRINCIPAL':  '#FFFFFF',
}

# Lista extendida de colores para botones (nombre en español, clave en la paleta)
COLORES_BOTONES = [
    # Originales
    ('Azul', 'AZUL'),
    ('Gris', 'GRIS'),
    ('Exito', 'VERDE'),
    ('Peligro', 'ROJO'),
    ('Advertencia', 'AMARILLO'),
    
    # Nuevos
    ('Cian', 'CIAN'),
    ('Morado', 'MORADO'),
    ('Rosa', 'ROSA'),
    ('Naranja', 'NARANJA'),
    ('Indigo', 'INDIGO'),
    ('Turquesa', 'TURQUESA'),
    ('Azul Oscuro', 'AZUL_OSCURO'),
    ('Verde Oscuro', 'VERDE_OSCURO'),
]

# Configuración global de estilos de botones outline (igual que original)
def configurar_estilos(raiz):
    estilo = ttk.Style(raiz)
    estilo.theme_use('clam')

    fuente_btn = ('Tahoma', 10,"bold")
    padding_btn = (10, 6)
    radio = 5

    for nombre, clave in COLORES_BOTONES:
        style_name = f"{nombre}.TButton"
        base_color = PALETA_COLORES[clave]
        # Outline: fondo blanco, texto y borde del color
        estilo.configure(
            style_name,
            font=fuente_btn,
            padding=padding_btn,
            background=PALETA_COLORES['FONDO_PRINCIPAL'],
            foreground=base_color,
            bordercolor=base_color,
            relief='solid',
            borderwidth=1,
            borderradius=radio,
            
        )
        # Hover: fondo en color y texto blanco
        estilo.map(
            style_name,
            background=[('active', base_color)],
            foreground=[('active', PALETA_COLORES['FONDO_PRINCIPAL'])],
            relief=[('pressed', 'flat')]
        )

# Función para crear botones fácilmente desde otros módulos
def crear_boton(padre, texto, color_nombre, comando=None):
    """
    Crea un botón con el estilo preconfigurado.
    
    Args:
        padre: Widget contenedor
        texto: Texto a mostrar en el botón
        color_nombre: Nombre del color (ej. 'Azul', 'Peligro')
        comando: Función a ejecutar al hacer click (opcional)
        
    Returns:
        ttk.Button: Botón configurado
    """
    # Buscar el nombre exacto en COLORES_BOTONES
    nombre_estilo = next((nombre for nombre, _ in COLORES_BOTONES if nombre.lower() == color_nombre.lower()), 'Azul')
    
    return ttk.Button(
        padre,
        text=texto,
        style=f"{nombre_estilo}.TButton",
        command=comando
    )


# Demo para visualizar todos los botones (mejorada para mostrar más botones)
def _demo_botones():
    raiz = tk.Tk()
    raiz.title('Demo de Botones POS - Colores Extendidos')
    raiz.configure(bg=PALETA_COLORES['FONDO_PRINCIPAL'])

    configurar_estilos(raiz)
    cont = ttk.Frame(raiz, padding=20)
    cont.pack(fill=tk.BOTH, expand=True)

    # Instrucciones
    ttk.Label(
        cont,
        text='Botones estilo POS extendidos - Pase el cursor para ver el estado hover',
        font=('Segoe UI', 10),
        foreground=PALETA_COLORES['TEXTO_OSCURO']
    ).pack(pady=(0,15))

    # Frame contenedor con scroll para muchos botones
    frame_contenedor = ttk.Frame(cont)
    frame_contenedor.pack(fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(frame_contenedor)
    scrollbar = ttk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Mostrar cada botón en dos columnas
    col1 = ttk.Frame(scrollable_frame)
    col2 = ttk.Frame(scrollable_frame)
    col1.pack(side="left", fill="both", expand=True, padx=10)
    col2.pack(side="left", fill="both", expand=True, padx=10)

    for i, (nombre, _) in enumerate(COLORES_BOTONES):
        col = col1 if i % 2 == 0 else col2
        btn = ttk.Button(col, text=nombre, style=f"{nombre}.TButton")
        btn.pack(fill=tk.X, pady=5)

    raiz.mainloop()

if __name__ == '__main__':
    _demo_botones()