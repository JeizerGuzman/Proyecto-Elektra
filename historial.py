import tkinter as tk
from tkinter import ttk, messagebox
import conexion  # tu módulo de conexión
from botones import configurar_estilos

class HistorialApp:
    """
    Muestra un historial de ventas y sus detalles.
    container: Frame donde se renderiza.
    """
    def __init__(self, container):
        self.container = container
        self.db = conexion.conectar()
        self.cursor = self.db.cursor()
        self._render_ui()
        configurar_estilos(self.container)

    def _clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def _render_ui(self):
        self._clear()
        self.container.configure(bg="white")

        # Encabezado
        header = tk.Frame(self.container, bg="#8FC9DB", height=40, padx=10, pady=5)
        header.pack(fill=tk.X)
        tk.Label(header, text="HISTORIAL DE VENTAS", font=("Tahoma",14,"bold"),fg="white", bg="#8FC9DB").pack(side=tk.LEFT)

        # Panel búsqueda
        search_frame = tk.Frame(self.container, bg="white")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(search_frame, text="Buscar por ID Venta:", bg="white",font=("tahoma",10)).pack(side=tk.LEFT)
        self.entry_buscar = ttk.Entry(search_frame, width=20)
        self.entry_buscar.pack(side=tk.LEFT, padx=5)
        self.entry_buscar.bind("<KeyRelease>", self.buscar_ventas)

        # Split: Ventas (izq) y Detalles (der)
        main = tk.Frame(self.container, bg="white")
        main.pack(fill=tk.BOTH, expand=True)

        # Panel de Ventas
        left = tk.Frame(main, bg="white")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        cols_v = ("id_venta", "fecha", "importe", "telefono_cliente", "usuario")
        self.tree_v = ttk.Treeview(left, columns=cols_v, show="headings")
        for col, txt, w in [
            ("id_venta","ID",80),
            ("fecha","Fecha",100),
            ("importe","Importe",100),
            ("telefono_cliente","Teléfono Cliente",140),
            ("usuario","Usuario",120)
        ]:
            self.tree_v.heading(col, text=txt)
            self.tree_v.column(col, width=w, anchor="center")
        self.tree_v.pack(fill=tk.BOTH, expand=True)
        sb_v = ttk.Scrollbar(left, orient="vertical", command=self.tree_v.yview)
        sb_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_v.configure(yscrollcommand=sb_v.set)
        self.tree_v.bind("<<TreeviewSelect>>", self.on_select_venta)

        btn_cancel = ttk.Button(left, text="Cancelar Venta", style="Peligro.TButton", command=self.cancelar_venta)
        btn_cancel.pack(pady=5)

        # Panel de DetalleVenta
        right = tk.Frame(main, bg="white")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        cols_d = ("codigo", "cantidad", "precio")
        self.tree_d = ttk.Treeview(right, columns=cols_d, show="headings")
        for col, txt, w in [
            ("codigo","Código",120),
            ("cantidad","Cantidad",80),
            ("precio","Precio",100)
        ]:
            self.tree_d.heading(col, text=txt)
            self.tree_d.column(col, width=w, anchor="center")
        self.tree_d.pack(fill=tk.BOTH, expand=True)
        sb_d = ttk.Scrollbar(right, orient="vertical", command=self.tree_d.yview)
        sb_d.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_d.configure(yscrollcommand=sb_d.set)

        self.load_ventas()

    def load_ventas(self, filtro=None):
        self.tree_v.delete(*self.tree_v.get_children())
        sql = (
            "SELECT v.id_venta, v.fecha, v.importe, v.telefono, u.nombre "
            "FROM Venta v "
            "LEFT JOIN Usuarios u ON v.id_usuario = u.id_usuario "
        )
        params = []
        if filtro:
            sql += "WHERE CAST(v.id_venta AS CHAR) LIKE %s "
            params = [f"%{filtro}%"]
        sql += "ORDER BY v.id_venta DESC"  # Ordena por más reciente primero
        try:
            self.cursor.execute(sql, params)
            for row in self.cursor.fetchall():
                id_venta, fecha, importe, telefono, usuario = row
                self.tree_v.insert("", tk.END, values=(
                    id_venta, fecha, f"${importe:.2f}", telefono, usuario or "Desconocido"
                ))
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudo cargar ventas: {e}")

    def buscar_ventas(self, event):
        texto = self.entry_buscar.get().strip()
        self.load_ventas(filtro=texto if texto else None)

    def on_select_venta(self, event):
        sel = self.tree_v.selection()
        if not sel:
            return
        id_venta = self.tree_v.item(sel[0], 'values')[0]
        self.load_detalle(id_venta)

    def load_detalle(self, id_venta):
        self.tree_d.delete(*self.tree_d.get_children())
        sql = (
            "SELECT codigo, cantidad, precio "
            "FROM DetalleVenta WHERE id_venta = %s"
        )
        try:
            self.cursor.execute(sql, (id_venta,))
            for codigo, cantidad, precio in self.cursor.fetchall():
                self.tree_d.insert("", tk.END, values=(codigo, cantidad, f"${precio:.2f}"))
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudo cargar detalle: {e}")

    def cancelar_venta(self):
        sel = self.tree_v.selection()
        if not sel:
            messagebox.showwarning("Validación", "Seleccione una venta para cancelar.")
            return
        id_venta = self.tree_v.item(sel[0], 'values')[0]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la venta {id_venta}?" ):
            return
        try:
            self.cursor.execute("DELETE FROM DetalleVenta WHERE id_venta = %s", (id_venta,))
            self.cursor.execute("DELETE FROM Venta WHERE id_venta = %s", (id_venta,))
            self.db.commit()
            messagebox.showinfo("Éxito", f"Venta {id_venta} cancelada.")
            self.load_ventas()
            self.tree_d.delete(*self.tree_d.get_children())
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error BD", f"No se pudo cancelar venta: {e}")
