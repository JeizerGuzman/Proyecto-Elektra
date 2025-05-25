import tkinter as tk
from tkinter import ttk, messagebox
import conexion  # tu módulo de conexión

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

    def _clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def _render_ui(self):
        self._clear()
        self.container.configure(bg="white")

        # Encabezado
        header = tk.Frame(self.container, bg="#ECECEC", height=40, padx=10, pady=5)
        header.pack(fill=tk.X)
        tk.Label(header, text="HISTORIAL DE VENTAS", font=("Helvetica",14,"bold"), bg="#ECECEC").pack(side=tk.LEFT)

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

        # Botón para cancelar venta
        btn_cancel = tk.Button(left, text="Cancelar Venta", bg="#dc3545", fg="white",
                               font=("Helvetica",10,"bold"), command=self.cancelar_venta)
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

        # Cargar ventas
        self.load_ventas()

    def load_ventas(self):
        # Limpia y consulta con JOIN para mostrar nombre de usuario
        self.tree_v.delete(*self.tree_v.get_children())
        sql = ("SELECT v.id_venta, v.fecha, v.importe, v.telefono, u.nombre "
               "FROM Venta v "
               "LEFT JOIN Usuarios u ON v.id_usuario = u.id_usuario "
               "ORDER BY v.fecha DESC")
        try:
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():
                # row = (id_venta, fecha, importe, telefono, nombre_usuario)
                id_venta, fecha, importe, telefono, usuario = row
                self.tree_v.insert("", tk.END, values=(
                    id_venta, fecha, f"${importe:.2f}", telefono, usuario or "Desconocido"
                ))
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudo cargar ventas: {e}")

    def on_select_venta(self, event):
        sel = self.tree_v.selection()
        if not sel:
            return
        id_venta = self.tree_v.item(sel[0], 'values')[0]
        self.load_detalle(id_venta)

    def load_detalle(self, id_venta):
        self.tree_d.delete(*self.tree_d.get_children())
        sql = ("SELECT codigo, cantidad, precio "
               "FROM DetalleVenta WHERE id_venta = %s")
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
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la venta {id_venta}?"):
            return
        try:
            # Borrar detalle y venta
            self.cursor.execute("DELETE FROM DetalleVenta WHERE id_venta = %s", (id_venta,))
            self.cursor.execute("DELETE FROM Venta WHERE id_venta = %s", (id_venta,))
            self.db.commit()
            messagebox.showinfo("Éxito", f"Venta {id_venta} cancelada.")
            self.load_ventas()
            self.tree_d.delete(*self.tree_d.get_children())
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error BD", f"No se pudo cancelar venta: {e}")

# Ejemplo de uso desde tu módulo de reportes:
#
# from historial import HistorialApp
#
# class ReportesApp:
#     def on_historial(self):
#         self._clear()
#         HistorialApp(self.content)
#
# Y en la sección de navegación:
# tk.Button(nav, text="Historial", command=self.on_historial).pack(...)
