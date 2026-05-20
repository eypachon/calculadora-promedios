# ============================================================
#   main.py — Punto de entrada de la aplicación
# ============================================================

import tkinter as tk
from interfaz import construir_interfaz


def main():
    root = tk.Tk()
    construir_interfaz(root)
    root.mainloop()


if __name__ == "__main__":
    main()
