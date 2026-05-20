# ============================================================
#   interfaz.py — Interfaz gráfica con Tkinter
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox

from entrada import validar_nombre, validar_calificacion, nombre_duplicado
from reporte import generar_reporte, reporte_a_texto

# ── Paleta de colores ────────────────────────────────────────
COLOR_BG       = "#1e1e2e"
COLOR_PANEL    = "#2a2a3e"
COLOR_ACCENT   = "#7c6af7"
COLOR_ACCENT2  = "#56cfb2"
COLOR_DANGER   = "#f07178"
COLOR_TEXT     = "#cdd6f4"
COLOR_SUBTEXT  = "#a6adc8"
COLOR_INPUT_BG = "#313244"
COLOR_BORDER   = "#45475a"
COLOR_APROBADA = "#a6e3a1"
COLOR_REPROBADA= "#f38ba8"

FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_LABEL  = ("Segoe UI", 10)
FONT_BOLD   = ("Segoe UI", 10, "bold")
FONT_SMALL  = ("Segoe UI", 9)
FONT_MONO   = ("Consolas", 10)


def construir_interfaz(root):
    """
    Construye y configura todos los widgets de la ventana principal.
    """
    # Listas de datos
    nombres       = []
    calificaciones = []

    # ── Configuración de la ventana ──────────────────────────
    root.title("Calculadora de Promedios")
    root.configure(bg=COLOR_BG)
    root.resizable(False, False)

    # Centrar ventana
    ancho, alto = 860, 640
    x = (root.winfo_screenwidth()  - ancho) // 2
    y = (root.winfo_screenheight() - alto)  // 2
    root.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ── Encabezado ───────────────────────────────────────────
    frame_header = tk.Frame(root, bg=COLOR_ACCENT, pady=12)
    frame_header.pack(fill="x")

    tk.Label(
        frame_header,
        text="📚  Calculadora de Promedios",
        font=FONT_TITLE,
        bg=COLOR_ACCENT,
        fg="white",
    ).pack()

    tk.Label(
        frame_header,
        text="Ingresa tus materias y calificaciones para obtener tu reporte",
        font=FONT_SMALL,
        bg=COLOR_ACCENT,
        fg="#e0d9ff",
    ).pack()

    # ── Contenedor principal ─────────────────────────────────
    frame_main = tk.Frame(root, bg=COLOR_BG)
    frame_main.pack(fill="both", expand=True, padx=16, pady=12)

    # ── Panel izquierdo: formulario + lista ──────────────────
    frame_izq = tk.Frame(frame_main, bg=COLOR_BG, width=350)
    frame_izq.pack(side="left", fill="both", padx=(0, 8))
    frame_izq.pack_propagate(False)

    # Formulario de ingreso
    frame_form = tk.Frame(frame_izq, bg=COLOR_PANEL, padx=14, pady=14,
                          relief="flat", bd=0)
    frame_form.pack(fill="x")
    _borde(frame_form)

    tk.Label(frame_form, text="➕  Agregar Materia",
             font=FONT_BOLD, bg=COLOR_PANEL, fg=COLOR_ACCENT).pack(anchor="w")

    tk.Label(frame_form, text="Nombre de la materia:",
             font=FONT_LABEL, bg=COLOR_PANEL, fg=COLOR_SUBTEXT).pack(anchor="w", pady=(10, 2))
    entry_nombre = _entry(frame_form)
    entry_nombre.pack(fill="x")

    lbl_err_nombre = tk.Label(frame_form, text="", font=FONT_SMALL,
                              bg=COLOR_PANEL, fg=COLOR_DANGER)
    lbl_err_nombre.pack(anchor="w")

    tk.Label(frame_form, text="Calificación (0 – 10):",
             font=FONT_LABEL, bg=COLOR_PANEL, fg=COLOR_SUBTEXT).pack(anchor="w", pady=(6, 2))
    entry_cal = _entry(frame_form)
    entry_cal.pack(fill="x")

    lbl_err_cal = tk.Label(frame_form, text="", font=FONT_SMALL,
                           bg=COLOR_PANEL, fg=COLOR_DANGER)
    lbl_err_cal.pack(anchor="w")

    def agregar_materia():
        lbl_err_nombre.config(text="")
        lbl_err_cal.config(text="")

        ok_n, resultado_n = validar_nombre(entry_nombre.get())
        if not ok_n:
            lbl_err_nombre.config(text=f"⚠ {resultado_n}")
            entry_nombre.focus()
            return

        if nombre_duplicado(resultado_n, nombres):
            lbl_err_nombre.config(text="⚠ Esa materia ya fue ingresada.")
            entry_nombre.focus()
            return

        ok_c, resultado_c = validar_calificacion(entry_cal.get())
        if not ok_c:
            lbl_err_cal.config(text=f"⚠ {resultado_c}")
            entry_cal.focus()
            return

        nombres.append(resultado_n)
        calificaciones.append(resultado_c)

        entry_nombre.delete(0, tk.END)
        entry_cal.delete(0, tk.END)
        entry_nombre.focus()

        _actualizar_lista(tree_materias, nombres, calificaciones)
        lbl_contador.config(text=f"Total: {len(nombres)} materia(s)")

    btn_agregar = tk.Button(
        frame_form,
        text="  Agregar materia",
        font=FONT_BOLD,
        bg=COLOR_ACCENT,
        fg="white",
        activebackground="#6a58e0",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        pady=7,
        command=agregar_materia,
    )
    btn_agregar.pack(fill="x", pady=(10, 0))

    # Bind Enter en los campos
    entry_nombre.bind("<Return>", lambda e: entry_cal.focus())
    entry_cal.bind("<Return>",   lambda e: agregar_materia())

    # Lista de materias ingresadas
    frame_lista = tk.Frame(frame_izq, bg=COLOR_PANEL, padx=10, pady=10)
    frame_lista.pack(fill="both", expand=True, pady=(10, 0))
    _borde(frame_lista)

    tk.Label(frame_lista, text="📋  Materias ingresadas",
             font=FONT_BOLD, bg=COLOR_PANEL, fg=COLOR_ACCENT2).pack(anchor="w")

    lbl_contador = tk.Label(frame_lista, text="Total: 0 materia(s)",
                            font=FONT_SMALL, bg=COLOR_PANEL, fg=COLOR_SUBTEXT)
    lbl_contador.pack(anchor="w")

    # Treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background=COLOR_INPUT_BG,
                    foreground=COLOR_TEXT,
                    fieldbackground=COLOR_INPUT_BG,
                    rowheight=26,
                    font=FONT_SMALL)
    style.configure("Custom.Treeview.Heading",
                    background=COLOR_BORDER,
                    foreground=COLOR_TEXT,
                    font=FONT_BOLD)
    style.map("Custom.Treeview", background=[("selected", COLOR_ACCENT)])

    cols = ("materia", "nota", "estado")
    tree_materias = ttk.Treeview(frame_lista, columns=cols,
                                  show="headings", height=8,
                                  style="Custom.Treeview")
    tree_materias.heading("materia", text="Materia")
    tree_materias.heading("nota",    text="Nota")
    tree_materias.heading("estado",  text="Estado")
    tree_materias.column("materia", width=160, anchor="w")
    tree_materias.column("nota",    width=55,  anchor="center")
    tree_materias.column("estado",  width=90,  anchor="center")

    sb = ttk.Scrollbar(frame_lista, orient="vertical", command=tree_materias.yview)
    tree_materias.configure(yscrollcommand=sb.set)
    tree_materias.pack(side="left", fill="both", expand=True, pady=(6, 0))
    sb.pack(side="right", fill="y", pady=(6, 0))

    def eliminar_seleccionada():
        sel = tree_materias.selection()
        if not sel:
            messagebox.showinfo("Sin selección", "Selecciona una materia para eliminar.")
            return
        idx = tree_materias.index(sel[0])
        nombres.pop(idx)
        calificaciones.pop(idx)
        _actualizar_lista(tree_materias, nombres, calificaciones)
        lbl_contador.config(text=f"Total: {len(nombres)} materia(s)")

    tk.Button(
        frame_lista,
        text="🗑 Eliminar seleccionada",
        font=FONT_SMALL,
        bg=COLOR_DANGER,
        fg="white",
        activebackground="#c0515a",
        relief="flat",
        cursor="hand2",
        pady=4,
        command=eliminar_seleccionada,
    ).pack(fill="x", pady=(6, 0), side="bottom")

    # ── Panel derecho: reporte ───────────────────────────────
    frame_der = tk.Frame(frame_main, bg=COLOR_BG)
    frame_der.pack(side="right", fill="both", expand=True)

    frame_reporte = tk.Frame(frame_der, bg=COLOR_PANEL, padx=14, pady=12)
    frame_reporte.pack(fill="both", expand=True)
    _borde(frame_reporte)

    tk.Label(frame_reporte, text="📊  Reporte Final",
             font=FONT_BOLD, bg=COLOR_PANEL, fg=COLOR_ACCENT2).pack(anchor="w")

    txt_reporte = tk.Text(
        frame_reporte,
        font=FONT_MONO,
        bg=COLOR_INPUT_BG,
        fg=COLOR_TEXT,
        relief="flat",
        bd=0,
        state="disabled",
        wrap="none",
        padx=10,
        pady=8,
        insertbackground=COLOR_TEXT,
    )
    sb_txt = ttk.Scrollbar(frame_reporte, orient="vertical", command=txt_reporte.yview)
    txt_reporte.configure(yscrollcommand=sb_txt.set)
    txt_reporte.pack(side="left", fill="both", expand=True, pady=(8, 0))
    sb_txt.pack(side="right", fill="y", pady=(8, 0))

    def generar():
        if not nombres:
            messagebox.showwarning("Sin datos",
                                   "Agrega al menos una materia antes de generar el reporte.")
            return
        reporte = generar_reporte(nombres, calificaciones, umbral=5.0)
        texto   = reporte_a_texto(reporte)
        txt_reporte.config(state="normal")
        txt_reporte.delete("1.0", tk.END)
        txt_reporte.insert(tk.END, texto)
        txt_reporte.config(state="disabled")

    def limpiar_todo():
        if not nombres:
            return
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar todas las materias?"):
            nombres.clear()
            calificaciones.clear()
            _actualizar_lista(tree_materias, nombres, calificaciones)
            lbl_contador.config(text="Total: 0 materia(s)")
            txt_reporte.config(state="normal")
            txt_reporte.delete("1.0", tk.END)
            txt_reporte.config(state="disabled")

    # Botones inferiores
    frame_btns = tk.Frame(frame_der, bg=COLOR_BG, pady=8)
    frame_btns.pack(fill="x")

    tk.Button(
        frame_btns,
        text="📊  Generar Reporte",
        font=FONT_BOLD,
        bg=COLOR_ACCENT2,
        fg="#1e1e2e",
        activebackground="#3daf94",
        relief="flat",
        cursor="hand2",
        pady=8,
        command=generar,
    ).pack(side="left", fill="x", expand=True, padx=(0, 6))

    tk.Button(
        frame_btns,
        text="🗑  Limpiar Todo",
        font=FONT_BOLD,
        bg=COLOR_BORDER,
        fg=COLOR_TEXT,
        activebackground="#585b70",
        relief="flat",
        cursor="hand2",
        pady=8,
        command=limpiar_todo,
    ).pack(side="right", fill="x", expand=True)

    # Foco inicial
    entry_nombre.focus()


# ── Helpers ──────────────────────────────────────────────────

def _entry(parent):
    """Crea un Entry con el estilo del tema oscuro."""
    e = tk.Entry(
        parent,
        font=("Segoe UI", 10),
        bg=COLOR_INPUT_BG,
        fg=COLOR_TEXT,
        insertbackground=COLOR_TEXT,
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground=COLOR_BORDER,
        highlightcolor=COLOR_ACCENT,
    )
    return e


def _borde(frame):
    """Agrega un borde sutil al frame (efecto tarjeta)."""
    frame.config(highlightbackground=COLOR_BORDER,
                 highlightthickness=1,
                 highlightcolor=COLOR_ACCENT)


def _actualizar_lista(tree, nombres, calificaciones):
    """Refresca el Treeview con los datos actuales."""
    for item in tree.get_children():
        tree.delete(item)
    for nombre, cal in zip(nombres, calificaciones):
        estado = "✔ Aprobada" if cal >= 5.0 else "✘ Reprobada"
        tag    = "aprobada" if cal >= 5.0 else "reprobada"
        tree.insert("", tk.END, values=(nombre, f"{cal:.1f}", estado), tags=(tag,))
    tree.tag_configure("aprobada",  foreground=COLOR_APROBADA)
    tree.tag_configure("reprobada", foreground=COLOR_REPROBADA)
