#!/usr/bin/env python3
"""
Optimizador de empaquetado de items.

Dado un largo total, encuentra la mejor combinacion de items de tamano 50 y 30
que minimiza el espacio sin usar. El espacio sobrante se distribuye como huecos
iguales: uno antes del primer item, uno entre cada par, y uno despues del ultimo.

Esquema de distribucion:
  [gap/2] [item] [gap] [item] [gap] ... [item] [gap/2]

Donde:
  - gap      = remainder / total_items  (hueco entre items)
  - gap/2    = edge_gap                 (hueco en los extremos, mitad del interno)
  - remainder = longitud sobrante despues de colocar todos los items
"""


def find_best_packing(length: float, mode: str = "gap") -> tuple[int, int, float]:
    """
    Busca la combinacion optima de items de tamano 50 y 30 para cubrir 'length'.

    Estrategia de busqueda:
      Para cada posible cantidad de items de tamano 50 (desde 0 hasta el maximo
      que cabe), calcula cuantos items de tamano 30 caben en el espacio restante
      y cual es el sobrante (remainder). Luego elige la combinacion segun el modo.

    Modos de optimizacion:
      "gap"   -- minimiza gap_unit = remainder / total_items.
                 Ante empate, prefiere la combinacion con menos items totales.
                 Util cuando se quiere que los huecos entre items sean lo mas
                 pequenos posible.
      "items" -- minimiza total_items = n50 + n30.
                 Ante empate, prefiere la combinacion con menor gap_unit.
                 Util cuando se quiere usar la menor cantidad de piezas.

    Parametros:
      length -- longitud total disponible (puede ser decimal)
      mode   -- criterio de optimizacion: "gap" o "items"

    Retorna:
      (n50, n30, remainder)
        n50       -- cantidad de items de tamano 50
        n30       -- cantidad de items de tamano 30
        remainder -- espacio sobrante despues de colocar todos los items
    """

    def candidate(n50: int) -> tuple[int, int, float]:
        # Espacio que queda despues de colocar n50 items de tamano 50
        space = length - n50 * 50
        # Maximo de items de tamano 30 que caben en ese espacio (division entera)
        n30 = int(space // 30)
        # Espacio sobrante que no ocupa ningun item
        return n50, n30, space - n30 * 30

    # Funcion de ordenamiento segun el modo elegido.
    # Python's min() usa el primer elemento de la tupla como criterio principal
    # y los siguientes como desempate, en orden.
    if mode == "items":
        # Criterio principal: minimizar total de items (n50 + n30)
        # Desempate: minimizar gap_unit = remainder / total_items
        key = lambda c: (c[0] + c[1], c[2] / (c[0] + c[1]))
    else:
        # Criterio principal: minimizar gap_unit = remainder / total_items
        # Desempate: minimizar total de items
        key = lambda c: (c[2] / (c[0] + c[1]), c[0] + c[1])

    # Genera todos los candidatos posibles y elige el mejor segun la clave.
    # range(int(length // 50) + 1) produce 0, 1, 2, ... hasta el maximo de
    # items de tamano 50 que fisicamente caben en 'length'.
    return min(
        (candidate(n50) for n50 in range(int(length // 50) + 1)),
        key=key,
    )


def format_layout(items: list[int], gap_unit: float, edge_gap: float) -> str:
    """
    Genera una representacion visual del layout como cadena de texto.

    El layout tiene la forma:
      [edge_gap] [item1] [gap_unit] [item2] [gap_unit] ... [itemN] [edge_gap]

    Los huecos de los extremos (edge_gap) son la mitad del hueco interno
    (gap_unit), de modo que la suma de ambos extremos equivale a un hueco
    interno, manteniendo la distribucion uniforme.

    Parametros:
      items     -- lista de tamanos de los items en orden de colocacion
      gap_unit  -- tamano del hueco entre items consecutivos
      edge_gap  -- tamano del hueco en cada extremo (= gap_unit / 2)

    Retorna:
      Cadena con la representacion visual del layout.
    """
    eg = f"[{edge_gap:.4f}]"   # etiqueta para el hueco de extremo
    ig = f"[{gap_unit:.4f}]"   # etiqueta para el hueco interno
    parts = [eg]               # empieza con el hueco izquierdo
    last = len(items) - 1
    for i, size in enumerate(items):
        parts.append(f"[{size}]")
        # Despues del ultimo item va el hueco de extremo; entre items, el interno
        parts.append(eg if i == last else ig)
    return " ".join(parts)


def main() -> None:
    """
    Punto de entrada del programa. Lee parametros del usuario, ejecuta la
    optimizacion y muestra los resultados con detalle.

    Flujo:
      1. Pregunta al usuario que criterio de optimizacion desea usar.
      2. Lee el largo total de la seccion a rellenar.
      3. Valida que la entrada sea un numero positivo mayor o igual a 30
         (tamano del item mas pequeno).
      4. Llama a find_best_packing() para obtener la combinacion optima.
      5. Calcula los huecos a partir del sobrante.
      6. Muestra el resumen, el layout visual y la tabla de posiciones.
      7. Muestra una verificacion numerica de que la suma de todas las
         partes coincide con el largo total ingresado.
    """
    # Paso 1: elegir modo de optimizacion
    raw = input("Prioritize (G)ap size or (I)tem count? [G/I, default G]: ").strip().upper()
    mode = "items" if raw == "I" else "gap"
    mode_label = "Min items" if mode == "items" else "Min gap"

    print()

    # Paso 2: leer el largo total
    try:
        length = float(input("Enter the total length: "))
    except ValueError:
        print("Error: please enter a valid number.")
        return

    # Paso 3: validaciones de entrada
    if length <= 0:
        print("Error: length must be a positive number.")
        return

    if length < 30:
        # No cabe ni el item mas pequeno (tamano 30)
        print(f"Length {length:.4f} is smaller than the minimum item size (30).")
        print("No items can be placed.")
        return

    # Paso 4: encontrar la combinacion optima de items
    n50, n30, remainder = find_best_packing(length, mode)

    # Construir la lista de items: primero los de tamano 50, luego los de 30
    items = [50] * n50 + [30] * n30
    total_items = len(items)
    items_length = sum(items)   # suma de los tamanos de todos los items

    # Paso 5: calcular los huecos
    # El sobrante se divide en partes iguales: una por cada item.
    # Los huecos internos (entre items) usan una parte completa cada uno.
    # Los huecos de los extremos (inicio y fin) usan media parte cada uno,
    # de modo que los dos extremos juntos equivalen a un hueco interno.
    gap_unit = remainder / total_items   # hueco entre items consecutivos
    edge_gap = gap_unit / 2              # hueco en cada extremo

    # Paso 6a: mostrar resumen de la optimizacion
    print()
    print("=" * 50)
    print("  PACKING RESULT")
    print("=" * 50)
    print(f"  Optimization      : {mode_label}")
    print(f"  Total length      : {length}")
    print(f"  Items size 50     : {n50}  ({n50 * 50} units)")
    print(f"  Items size 30     : {n30}  ({n30 * 30} units)")
    print(f"  Total items       : {total_items}")
    print(f"  Items coverage    : {items_length} / {length}  ({items_length/length*100:.2f}%)")
    print(f"  Remainder         : {remainder:.6f}")
    print(f"  Internal gap      : {gap_unit:.6f}  ({total_items - 1} gaps between items)")
    print(f"  Edge gap (x2)     : {edge_gap:.6f}  (start + end = 1 internal gap)")
    print("=" * 50)
    print()

    # Paso 6b: mostrar el layout visual
    print("Layout  ( [gap] [item] [gap] ... ):")
    print()
    print("  " + format_layout(items, gap_unit, edge_gap))
    print()

    # Paso 6c: mostrar tabla de posiciones absolutas de cada item
    # 'cursor' rastrea la posicion actual a lo largo del largo total.
    # Comienza en edge_gap (el primer hueco de extremo).
    print(f"  {'#':<5} {'Size':<6} {'Start':>10} {'End':>10} {'Center':>10}")
    print(f"  {'-'*5} {'-'*6} {'-'*10} {'-'*10} {'-'*10}")
    cursor = edge_gap
    for i, size in enumerate(items, 1):
        start, end = cursor, cursor + size
        print(f"  {i:<5} {size:<6} {start:>10.4f} {end:>10.4f} {(start+end)/2:>10.4f}")
        # Avanza el cursor hasta el inicio del proximo item (item + hueco interno)
        cursor = end + gap_unit
    print()

    # Paso 7: verificacion numerica
    # La suma debe ser exactamente igual al largo total ingresado:
    #   items_length + gap_unit * (total_items - 1) + edge_gap * 2
    #   = items_length + remainder - gap_unit + gap_unit
    #   = items_length + remainder
    #   = length
    reconstructed = items_length + gap_unit * (total_items - 1) + edge_gap * 2
    print(f"  Verification: {items_length} + {gap_unit:.6f}x{total_items - 1} + {edge_gap:.6f}x2 = {reconstructed:.6f}  [OK]")
    print()


if __name__ == "__main__":
    main()
