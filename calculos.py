# ============================================================
#   calculos.py — Funciones de procesamiento de calificaciones
# ============================================================


def calcular_promedio(calificaciones):
    """
    Recibe una lista de calificaciones y devuelve el promedio.
    Retorna 0.0 si la lista está vacía.
    """
    if not calificaciones:
        return 0.0
    return sum(calificaciones) / len(calificaciones)


def determinar_estado(calificaciones, umbral=5.0):
    """
    Clasifica materias en aprobadas y reprobadas según el umbral.
    Retorna dos listas con los índices correspondientes.
    """
    aprobadas = []
    reprobadas = []

    for i, calificacion in enumerate(calificaciones):
        if calificacion >= umbral:
            aprobadas.append(i)
        else:
            reprobadas.append(i)

    return aprobadas, reprobadas


def encontrar_extremos(calificaciones):
    """
    Encuentra el índice de la calificación más alta y más baja.
    Retorna (indice_max, indice_min). Si la lista está vacía retorna (None, None).
    """
    if not calificaciones:
        return None, None

    indice_max = 0
    indice_min = 0

    for i in range(1, len(calificaciones)):
        if calificaciones[i] > calificaciones[indice_max]:
            indice_max = i
        if calificaciones[i] < calificaciones[indice_min]:
            indice_min = i

    return indice_max, indice_min
