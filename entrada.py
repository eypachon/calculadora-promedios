# ============================================================
#   entrada.py — Validación de datos ingresados por el usuario
# ============================================================


def validar_nombre(nombre):
    """
    Valida que el nombre de la materia no esté vacío ni sea solo espacios.
    Retorna (True, nombre_limpio) o (False, mensaje_error).
    """
    nombre = nombre.strip()
    if not nombre:
        return False, "El nombre de la materia no puede estar vacío."
    if len(nombre) < 2:
        return False, "El nombre debe tener al menos 2 caracteres."
    return True, nombre


def validar_calificacion(texto):
    """
    Valida que la calificación sea un número entre 0 y 10.
    Retorna (True, valor_float) o (False, mensaje_error).
    """
    texto = texto.strip().replace(",", ".")
    if not texto:
        return False, "La calificación no puede estar vacía."
    try:
        valor = float(texto)
    except ValueError:
        return False, "Ingresa un número válido (ej. 7 o 8.5)."
    if valor < 0.0 or valor > 10.0:
        return False, "La calificación debe estar entre 0 y 10."
    return True, valor


def nombre_duplicado(nombre, lista_nombres):
    """
    Verifica si el nombre ya existe en la lista (sin distinción de mayúsculas).
    Retorna True si es duplicado.
    """
    nombre_lower = nombre.strip().lower()
    return any(n.lower() == nombre_lower for n in lista_nombres)
