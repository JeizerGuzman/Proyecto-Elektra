import tkinter as tk
from tkinter import ttk


def ventana_venta(container):
    """
    Carga la interfaz de Ventas en el contenedor (frame) que se le pase.
    Este módulo muestra:
      - Un título "VENTAS".
      - Una barra de búsqueda para el código de producto y un botón "Agregar producto".
      - Una tabla (Treeview) que simula el ticket con columnas:
        Código de Barra, Descripción, Precio Venta, Cantidad, Importe y Existencia.
      - En la parte inferior, botones para "Eliminar Ticket" y "Asignar Usuario", 
        y a la derecha, un botón "Cobrar" junto a la visualización del Total.
    """
    # Limpia el contenedor
    for widget in container.winfo_children():
        widget.destroy()

    # Frame principal
    main_frame = tk.Frame(container, bg="white")
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Título del contenido (por defecto: "Ventas")
    content_title_frame = tk.Frame(main_frame, bg="#F0F0F0", height=40, padx=10, pady=5)
    content_title_frame.pack(side=tk.TOP, fill=tk.X)
    lbl_content_title = tk.Label(content_title_frame, text="VENTAS", font=("Helvetica", 16, "bold"), bg="#F0F0F0")
    lbl_content_title.pack(side=tk.LEFT)

    # Barra de búsqueda (código de producto + botón "Agregar producto")
    search_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10)
    search_frame.pack(side=tk.TOP, fill=tk.X)
    tk.Label(search_frame, text="Código de producto:", font=("Helvetica", 10), bg="white")\
        .pack(side=tk.LEFT, padx=5)
    entry_codigo = tk.Entry(search_frame, width=20, font=("Helvetica", 10))
    entry_codigo.pack(side=tk.LEFT, padx=5)
    btn_agregar_prod = tk.Button(search_frame, text="Agregar producto", font=("Helvetica", 10, "bold"), 
                                 bg="#A9A9A9", width=15)
    btn_agregar_prod.pack(side=tk.LEFT, padx=10)

    # Tabla del ticket
    table_frame = tk.Frame(main_frame, bg="white")
    table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
    columns = ("cod_barras", "descripcion", "precio_venta", "cantidad", "importe", "existencia")
    tree_ticket = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
    tree_ticket.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Encabezados
    tree_ticket.heading("cod_barras", text="Código del Producto", anchor="center")
    tree_ticket.heading("descripcion", text="Descripción", anchor="center")
    tree_ticket.heading("precio_venta", text="Precio Venta", anchor="center")
    tree_ticket.heading("cantidad", text="Cantidad", anchor="center")
    tree_ticket.heading("importe", text="Importe", anchor="center")
    tree_ticket.heading("existencia", text="Existencia", anchor="center")
    
    # Ajuste de columnas
    tree_ticket.column("cod_barras", width=120, anchor="center")
    tree_ticket.column("descripcion", width=200, anchor="w")
    tree_ticket.column("precio_venta", width=80, anchor="e")
    tree_ticket.column("cantidad", width=80, anchor="center")
    tree_ticket.column("importe", width=80, anchor="e")
    tree_ticket.column("existencia", width=80, anchor="center")
    
    # Scrollbar vertical
    scroll_ticket_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree_ticket.yview)
    scroll_ticket_y.pack(side=tk.LEFT, fill=tk.Y)
    tree_ticket.configure(yscrollcommand=scroll_ticket_y.set)

    # Frame inferior: botones + total
    bottom_frame = tk.Frame(main_frame, bg="#ECECEC", height=50, padx=10, pady=10)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Botones lado izquierdo
    btn_eliminar_ticket = tk.Button(bottom_frame, text="Eliminar Ticket", font=("Helvetica", 10, "bold"),
                                    bg="#A9A9A9", fg="black")
    btn_eliminar_ticket.pack(side=tk.LEFT, padx=5)
    
    btn_asignar_usuario = tk.Button(bottom_frame, text="Asignar Usuario", font=("Helvetica", 10, "bold"),
                                    bg="#A9A9A9", fg="black")
    btn_asignar_usuario.pack(side=tk.LEFT, padx=5)
    
    # Botón de Cobrar (lado derecho)
    btn_cobrar = tk.Button(bottom_frame, text="Cobrar", font=("Helvetica", 10, "bold"),
                           bg="green", fg="white", width=10)
    btn_cobrar.pack(side=tk.RIGHT, padx=5)
    
    # Total en la esquina inferior derecha
    lbl_total_compra = tk.Label(bottom_frame, text="Total: $0.00", font=("Helvetica", 14, "bold"), bg="#ECECEC")
    lbl_total_compra.pack(side=tk.RIGHT, padx=20)
    
    # (Opcional) Puedes agregar un label para el Subtotal si lo deseas.
    
# Si se ejecuta este archivo de forma independiente para pruebas:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Prueba de Ventas")
    root.state("zoomed")
    ventana_venta(root)
    root.mainloop()
