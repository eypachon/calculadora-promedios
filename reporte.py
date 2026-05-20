# ============================================================
#   reporte.py — Generación del resumen de resultados
# ============================================================

from calculos import calcular_promedio, determinar_estado, encontrar_extremos


def generar_reporte(nombres, calificaciones, umbral=5.0):
    """
    Genera un diccionario con toda la información procesada
    lista para ser mostrada por la interfaz.
    """
    if not nombres:
        return None

    promedio = calcular_promedio(calificaciones)
    aprobadas_idx, reprobadas_idx = determinar_estado(calificaciones, umbral)
    idx_max, idx_min = encontrar_extremos(calificaciones)

    reporte = {
        "total": len(nombres),
        "promedio": promedio,
        "aprobadas": [(nombres[i], calificaciones[i]) for i in aprobadas_idx],
        "reprobadas": [(nombres[i], calificaciones[i]) for i in reprobadas_idx],
        "mejor": (nombres[idx_max], calificaciones[idx_max]) if idx_max is not None else None,
        "peor": (nombres[idx_min], calificaciones[idx_min]) if idx_min is not None else None,
        "materias": list(zip(nombres, calificaciones)),
        "umbral": umbral,
    }

    return reporte


def reporte_a_texto(reporte):
    """
    Convierte el diccionario de reporte a un texto formateado para mostrar.
    """
    if not reporte:
        return "No hay datos para mostrar."

    lineas = []
    lineas.append("=" * 48)
    lineas.append("           RESUMEN DE CALIFICACIONES")
    lineas.append("=" * 48)
    lineas.append(f"\n{'Materia':<26} {'Nota':>6}  Estado")
    lineas.append("-" * 48)

    for nombre, cal in reporte["materias"]:
        estado = "✔ Aprobada" if cal >= reporte["umbral"] else "✘ Reprobada"
        lineas.append(f"{nombre:<26} {cal:>6.1f}  {estado}")

    lineas.append("-" * 48)
    lineas.append(f"\nTotal de materias : {reporte['total']}")
    lineas.append(f"Promedio general  : {reporte['promedio']:.2f} / 10.00")
    lineas.append(f"Aprobadas         : {len(reporte['aprobadas'])}")
    lineas.append(f"Reprobadas        : {len(reporte['reprobadas'])}")

    if reporte["mejor"]:
        lineas.append(f"\n🏆 Mejor nota : {reporte['mejor'][0]} ({reporte['mejor'][1]:.1f})")
    if reporte["peor"]:
        lineas.append(f"📉 Menor nota : {reporte['peor'][0]} ({reporte['peor'][1]:.1f})")

    lineas.append("\n" + "=" * 48)
    return "\n".join(lineas)
