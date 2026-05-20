# ============================================================
#   calculadora_promedios.py
#   Calculadora de promedios escolares — Programación Estructurada
# ============================================================

from calculos import calcular_promedio, determinar_estado, encontrar_extremos


# ── Función 1 ────────────────────────────────────────────────
def ingresar_calificaciones():
    """
    Permite al usuario ingresar nombres de materias y calificaciones.
    Valida que cada calificación sea un número entre 0 y 10.
    Retorna dos listas: nombres y calificaciones.
    """
    nombres        = []
    calificaciones = []

    print("\n" + "=" * 50)
    print("     INGRESO DE MATERIAS Y CALIFICACIONES")
    print("=" * 50)

    while True:
        # Ingresar nombre de la materia
        while True:
            nombre = input("\nNombre de la materia: ").strip()
            if len(nombre) >= 2:
                break
            print("  ⚠ El nombre debe tener al menos 2 caracteres.")

        # Validar que no sea duplicado
        if any(n.lower() == nombre.lower() for n in nombres):
            print(f"  ⚠ '{nombre}' ya fue ingresada. Elige otro nombre.")
            continue

        # Ingresar y validar calificación
        while True:
            entrada = input(f"Calificación de '{nombre}' (0 - 10): ").strip().replace(",", ".")
            try:
                calificacion = float(entrada)
                if 0.0 <= calificacion <= 10.0:
                    break
                else:
                    print("  ⚠ La calificación debe estar entre 0 y 10.")
            except ValueError:
                print("  ⚠ Ingresa un número válido (ej. 7 o 8.5).")

        nombres.append(nombre)
        calificaciones.append(calificacion)
        print(f"  ✔ '{nombre}' con calificación {calificacion:.1f} registrada.")

        # Preguntar si continuar
        while True:
            continuar = input("\n¿Deseas agregar otra materia? (s/n): ").strip().lower()
            if continuar in ("s", "n"):
                break
            print("  ⚠ Responde con 's' para sí o 'n' para no.")

        if continuar == "n":
            break

    return nombres, calificaciones


# ── Función 2 ────────────────────────────────────────────────
def mostrar_resumen(nombres, calificaciones, umbral=5.0):
    """
    Muestra el resumen final con todas las materias, promedio,
    aprobadas, reprobadas y los extremos de calificación.
    """
    promedio              = calcular_promedio(calificaciones)
    aprobadas_idx, reprobadas_idx = determinar_estado(calificaciones, umbral)
    idx_max, idx_min      = encontrar_extremos(calificaciones)

    print("\n" + "=" * 50)
    print("              RESUMEN FINAL")
    print("=" * 50)

    # Tabla de materias
    print(f"\n{'N°':<4} {'Materia':<25} {'Nota':>6}  Estado")
    print("-" * 50)
    for i in range(len(nombres)):
        estado = "✔ Aprobada" if calificaciones[i] >= umbral else "✘ Reprobada"
        print(f"{i + 1:<4} {nombres[i]:<25} {calificaciones[i]:>6.1f}  {estado}")
    print("-" * 50)

    # Promedio general
    print(f"\nPromedio general   : {promedio:.2f} / 10.00")
    print(f"Umbral de aprobado : {umbral:.1f}")

    # Aprobadas
    print(f"\n✔  Materias APROBADAS ({len(aprobadas_idx)}):")
    if aprobadas_idx:
        for i in aprobadas_idx:
            print(f"    - {nombres[i]} ({calificaciones[i]:.1f})")
    else:
        print("    Ninguna materia aprobada.")

    # Reprobadas
    print(f"\n✘  Materias REPROBADAS ({len(reprobadas_idx)}):")
    if reprobadas_idx:
        for i in reprobadas_idx:
            print(f"    - {nombres[i]} ({calificaciones[i]:.1f})")
    else:
        print("    Ninguna materia reprobada. ¡Excelente!")

    # Extremos
    print(f"\n🏆 Mejor calificación : {nombres[idx_max]} — {calificaciones[idx_max]:.1f}")
    print(f"📉 Menor calificación : {nombres[idx_min]} — {calificaciones[idx_min]:.1f}")

    print("\n" + "=" * 50)


# ── Función 3 ────────────────────────────────────────────────
def verificar_datos(nombres, calificaciones):
    """
    Verifica que las listas no estén vacías antes de procesar.
    Retorna True si hay datos, False si no hay nada que procesar.
    """
    if not nombres or not calificaciones:
        print("\n⚠ No se ingresaron materias. No hay datos para procesar.")
        return False
    if len(nombres) != len(calificaciones):
        print("\n⚠ Error interno: listas desincronizadas.")
        return False
    return True


# ── Función principal ────────────────────────────────────────
def main():
    print("\n" + "=" * 50)
    print("   BIENVENIDO A LA CALCULADORA DE PROMEDIOS")
    print("=" * 50)

    # 1. Ingresar calificaciones
    nombres, calificaciones = ingresar_calificaciones()

    # 2. Verificar que haya datos
    if not verificar_datos(nombres, calificaciones):
        print("\n¡Hasta luego! 👋\n")
        return

    # 3. Mostrar resumen completo
    mostrar_resumen(nombres, calificaciones, umbral=5.0)

    print("\n¡Gracias por usar la Calculadora de Promedios! 👋\n")


if __name__ == "__main__":
    main()
