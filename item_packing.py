#!/usr/bin/env python3
"""
Item packing optimizer.

Given a total length, finds the best combination of size-50 and size-30 items
that minimizes unused space. The remaining space is then distributed as equal
gaps: one before the first item, one between each pair, and one after the last.
"""


def find_best_packing(length: float) -> tuple[int, int, float]:
    """
    Return (n50, n30, remainder) minimizing remainder.
    Tie-break: prefer the combination with fewer total items.
    """
    def candidate(n50: int) -> tuple[int, int, float]:
        space = length - n50 * 50
        n30 = int(space // 30)
        return n50, n30, space - n30 * 30

    return min(
        (candidate(n50) for n50 in range(int(length // 50) + 1)),
        key=lambda c: (c[2], c[0] + c[1]),
    )


def format_layout(items: list[int], gap_unit: float, edge_gap: float) -> str:
    eg = f"[{edge_gap:.4f}]"
    ig = f"[{gap_unit:.4f}]"
    parts = [eg]
    last = len(items) - 1
    for i, size in enumerate(items):
        parts.append(f"[{size}]")
        parts.append(eg if i == last else ig)
    return " ".join(parts)


def main() -> None:
    try:
        length = float(input("Enter the total length: "))
    except ValueError:
        print("Error: please enter a valid number.")
        return

    if length <= 0:
        print("Error: length must be a positive number.")
        return

    if length < 30:
        print(f"Length {length:.4f} is smaller than the minimum item size (30).")
        print("No items can be placed.")
        return

    n50, n30, remainder = find_best_packing(length)
    items = [50] * n50 + [30] * n30
    total_items = len(items)
    items_length = sum(items)
    gap_unit = remainder / total_items
    edge_gap = gap_unit / 2

    print()
    print("=" * 50)
    print("  PACKING RESULT")
    print("=" * 50)
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
    print("Layout  ( [gap] [item] [gap] ... ):")
    print()
    print("  " + format_layout(items, gap_unit, edge_gap))
    print()

    print(f"  {'#':<5} {'Size':<6} {'Start':>10} {'End':>10} {'Center':>10}")
    print(f"  {'-'*5} {'-'*6} {'-'*10} {'-'*10} {'-'*10}")
    cursor = edge_gap
    for i, size in enumerate(items, 1):
        start, end = cursor, cursor + size
        print(f"  {i:<5} {size:<6} {start:>10.4f} {end:>10.4f} {(start+end)/2:>10.4f}")
        cursor = end + gap_unit
    print()

    reconstructed = items_length + gap_unit * (total_items - 1) + edge_gap * 2
    print(f"  Verification: {items_length} + {gap_unit:.6f}x{total_items - 1} + {edge_gap:.6f}x2 = {reconstructed:.6f}  [OK]")
    print()


if __name__ == "__main__":
    main()
