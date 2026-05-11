"""
csv_to_sw_sketch.py  [v4]
--------------------------
Lee un CSV con columnas: #, Size, Start, End, Center
Crea un ensamblaje nuevo de SolidWorks (.SLDASM) con un Sketch 3D
que contiene un punto por cada fila, ubicado a la distancia "Center"
desde el origen sobre el eje X.

Formato del CSV:
    #,Size,Start,End,Center
    1,50,0.2533,50.2533,25.2533
    2,30,50.7600,80.7600,65.7600
    ...

Requisitos:
    - SolidWorks instalado (no necesita estar abierto)
    - pip install pywin32
    - Python 64-bit si SolidWorks es 64-bit (lo normal desde SW2016+)

Uso rapido (sin SolidWorks):
    python csv_to_sw_sketch_1.py --dry-run
"""

import sys
import os
import csv
import argparse
import glob
import pythoncom

# ─────────────────────────────────────────────────────────────
#  CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────

DEFAULT_CSV    = "packing-386.08.csv"
DEFAULT_OUTPUT = "ensamblaje_puntos.SLDASM"

# Unidades del CSV → SolidWorks trabaja en metros internamente
# Factor ×10: valor CSV 25.2533 → 0.252533 m → SolidWorks muestra 252.533 mm
MM_TO_M = 0.01

# Plantilla de ensamblaje. Si dejas "", el script la busca automáticamente.
SW_ASSEMBLY_TEMPLATE = ""

# swUserPreferenceStringValue_e.swDefaultTemplateAssembly = 7
# (8 = swDefaultTemplateDrawing — DO NOT use 8)
_SW_PREF_TEMPLATE_ASM = 7

# swDocumentTypes_e
_SW_DOC_ASSEMBLY = 2


# ─────────────────────────────────────────────────────────────
#  LEER CSV
# ─────────────────────────────────────────────────────────────

def leer_csv(ruta: str):
    """
    Lee el CSV con columnas: #, Size, Start, End, Center.
    Devuelve lista de dicts. Ignora filas vacías o con datos inválidos.
    """
    segmentos = []
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            sys.exit("[ERROR] El CSV no tiene encabezados.")
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        for i, fila in enumerate(reader, start=2):
            fila = {k: v.strip() for k, v in fila.items() if k}

            if not any(fila.values()):
                continue

            try:
                numero = int(fila["#"])
                size   = float(fila["Size"])
                start  = float(fila["Start"])
                end    = float(fila["End"])
                center = float(fila["Center"])
            except (KeyError, ValueError):
                print(f"  [ADVERTENCIA] Fila {i} omitida (datos invalidos): {fila}")
                continue

            segmentos.append({
                "numero": numero,
                "size":   size,
                "start":  start,
                "end":    end,
                "center": center,   # mm desde el origen
            })

    if not segmentos:
        sys.exit("[ERROR] El CSV no contiene segmentos validos.")
    return segmentos


# ─────────────────────────────────────────────────────────────
#  DRY RUN (sin SolidWorks)
# ─────────────────────────────────────────────────────────────

def dry_run(segmentos, ruta_salida):
    """Muestra lo que se haria sin conectar a SolidWorks."""
    print("[DRY RUN] No se conectara a SolidWorks.")
    print(f"  Archivo de salida seria: {os.path.abspath(ruta_salida)}")
    print()
    print(f"  {'#':>3}  {'Size':>6}  {'Start':>10}  {'End':>10}  {'Center':>10}  {'X (m)':>10}")
    print("  " + "-" * 58)
    for seg in segmentos:
        x_m = seg["center"] * MM_TO_M
        print(
            f"  {seg['numero']:>3}  {seg['size']:>6.4f}  "
            f"{seg['start']:>10.4f}  {seg['end']:>10.4f}  "
            f"{seg['center']:>10.4f}  {x_m:>10.6f}"
        )
    print()
    print(f"  Total puntos a insertar: {len(segmentos)}")


# ─────────────────────────────────────────────────────────────
#  SOLIDWORKS — CONEXIÓN
# ─────────────────────────────────────────────────────────────

def iniciar_solidworks():
    """Conecta a SW si ya corre; si no, lo lanza."""
    try:
        import win32com.client
    except ImportError:
        sys.exit("[ERROR] pywin32 no encontrado. Ejecuta: pip install pywin32")

    print("[1/4] Conectando a SolidWorks...")
    try:
        sw = win32com.client.GetActiveObject("SldWorks.Application")
        print("      -> Instancia existente encontrada.")
    except Exception:
        print("      -> SolidWorks no estaba abierto, iniciando...")
        try:
            sw = win32com.client.Dispatch("SldWorks.Application")
        except Exception as e:
            sys.exit(
                f"[ERROR] No se pudo iniciar SolidWorks: {e}\n"
                f"        Verifica que SolidWorks este instalado."
            )
    sw.Visible     = True
    sw.UserControl = True
    return sw


# ─────────────────────────────────────────────────────────────
#  BUSCAR PLANTILLA
# ─────────────────────────────────────────────────────────────

def _buscar_plantilla_asm(sw):
    """Localiza un .asmdot en las rutas habituales de SolidWorks."""
    try:
        tpl = sw.GetUserPreferenceStringValue(_SW_PREF_TEMPLATE_ASM)
        if tpl and os.path.exists(tpl) and tpl.lower().endswith(".asmdot"):
            return tpl
    except Exception:
        pass

    try:
        exe    = sw.GetExecutablePath()
        sw_dir = os.path.dirname(exe)
    except Exception:
        sw_dir = r"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS"

    for patron in [
        os.path.join(sw_dir, "**", "*.asmdot"),
        r"C:\ProgramData\SolidWorks\**\*.asmdot",
        r"C:\Program Files\SOLIDWORKS Corp\**\*.asmdot",
    ]:
        resultados = glob.glob(patron, recursive=True)
        if resultados:
            return resultados[0]
    return ""


# ─────────────────────────────────────────────────────────────
#  CREAR ENSAMBLAJE NUEVO
# ─────────────────────────────────────────────────────────────

def crear_ensamblaje(sw, ruta_salida: str, plantilla: str):
    """Crea un .SLDASM vacío y lo guarda en ruta_salida."""
    print("[2/4] Creando ensamblaje nuevo...")

    if not plantilla:
        plantilla = _buscar_plantilla_asm(sw)

    if not plantilla or not os.path.exists(plantilla):
        sys.exit(
            "[ERROR] No se encontro la plantilla de ensamblaje (.asmdot).\n"
            "        Usa --plantilla \"C:\\ruta\\Assembly.asmdot\""
        )

    print(f"      -> Plantilla : {plantilla}")

    doc = sw.NewDocument(plantilla, 0, 0, 0)
    if doc is None:
        sys.exit("[ERROR] NewDocument() retorno None. SolidWorks no pudo crear el ensamblaje.")

    doc_type = doc.GetType
    if doc_type != _SW_DOC_ASSEMBLY:
        tipo_nombre = {1: "PART", 3: "DRAWING"}.get(doc_type, f"desconocido({doc_type})")
        sys.exit(
            f"[ERROR] NewDocument creo un {tipo_nombre} en lugar de ASSEMBLY.\n"
            f"        Verifica que la plantilla sea un .asmdot: {plantilla}"
        )

    ruta_abs = os.path.abspath(ruta_salida)
    os.makedirs(os.path.dirname(ruta_abs) or ".", exist_ok=True)

    # SaveAs3(path, version, options) — returns swFileSaveError_e; 0 = no error
    longstatus = doc.SaveAs3(ruta_abs, 0, 0)
    if longstatus != 0:
        print(f"  [ADVERTENCIA] SaveAs3 retorno codigo de error {longstatus} al guardar '{ruta_abs}'.")
    else:
        print(f"      -> Archivo  : {ruta_abs}")

    # Re-fetch active doc after SaveAs3 — the reference can go stale after the rename.
    doc = sw.ActiveDoc
    if doc is None:
        sys.exit("[ERROR] ActiveDoc es None despues de SaveAs3. No se pudo activar el ensamblaje.")

    return doc


# ─────────────────────────────────────────────────────────────
#  CREAR SKETCH 2D (TOP PLANE) CON PUNTOS
# ─────────────────────────────────────────────────────────────

def crear_puntos_sketch(doc, segmentos):
    """
    Selecciona el Top Plane, abre un Sketch 2D e inserta un punto por segmento.
    Sigue el mismo patron que la macro grabada en SolidWorks:
      SelectByID2("Top Plane") -> InsertSketch -> CreatePoint -> EditRebuild3
    Cada punto queda en (Center * MM_TO_M, 0, 0) sobre el eje X.
    """
    n = len(segmentos)
    print(f"[3/5] Insertando {n} punto(s) en Sketch 2D sobre Top Plane (eje X = Center)...")

    try:
        doc.EditAssembly()
    except Exception as e:
        print(f"  [ADVERTENCIA] EditAssembly() fallo: {e}")

    sm = doc.SketchManager
    if sm is None:
        sys.exit("[ERROR] SketchManager no disponible.")

    import win32com.client
    nothing = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)
    ok = doc.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, nothing, 0)
    if not ok:
        print("  [ADVERTENCIA] No se pudo seleccionar el Top Plane.")

    sm.InsertSketch(True)   # abre el sketch 2D sobre el plano seleccionado

    print()
    print(f"  {'#':>3}  {'Size':>6}  {'Start':>10}  {'End':>10}  {'Center':>10}  (mm)")
    print("  " + "-" * 50)

    for seg in segmentos:
        x_m = seg["center"] * MM_TO_M
        sm.CreatePoint(x_m, 0.0, 0.0)
        print(
            f"  {seg['numero']:>3}  {seg['size']:>6.4f}  "
            f"{seg['start']:>10.4f}  {seg['end']:>10.4f}  {seg['center']:>10.4f}"
        )

    sm.InsertSketch(True)   # cierra el sketch 2D (toggle)

    doc.EditRebuild3
    doc.ClearSelection2(True)

    print()
    print("      -> Sketch 2D cerrado correctamente.")


# ─────────────────────────────────────────────────────────────
#  GUARDAR Y CERRAR
# ─────────────────────────────────────────────────────────────

def guardar_doc(doc, ruta_salida: str):
    """Guarda con SaveAs3 (sin parametros ByRef) — mismo metodo que la macro grabada."""
    print("[4/5] Guardando cambios finales...")
    ruta_abs = os.path.abspath(ruta_salida)
    longstatus = doc.SaveAs3(ruta_abs, 0, 0)
    if longstatus != 0:
        print(f"  [ADVERTENCIA] SaveAs3 retorno codigo {longstatus}.")
    else:
        print(f"      -> Guardado OK: {ruta_abs}")


def cerrar_doc(sw, ruta_salida: str):
    """Cierra el documento en SolidWorks por nombre de archivo (sin ruta)."""
    print("[5/5] Cerrando documento...")
    nombre = os.path.basename(ruta_salida)
    try:
        sw.CloseDoc(nombre)
        print(f"      -> '{nombre}' cerrado correctamente.")
    except Exception as e:
        print(f"  [ADVERTENCIA] CloseDoc fallo: {e}")


# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Lee un CSV (#, Size, Start, End, Center) y crea un ensamblaje "
            "de SolidWorks con un punto por cada fila en la distancia 'Center' "
            "desde el origen sobre el eje X."
        )
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        default=DEFAULT_CSV,
        help=f"Ruta al CSV (default: {DEFAULT_CSV})",
    )
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_OUTPUT,
        help=f"Ruta de salida .SLDASM (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--plantilla",
        default=SW_ASSEMBLY_TEMPLATE,
        help="Ruta a la plantilla .asmdot de SolidWorks (opcional).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Leer y mostrar el CSV sin conectar a SolidWorks (para pruebas).",
    )
    args = parser.parse_args()

    print()
    print("=" * 62)
    print("  CSV (#,Size,Start,End,Center)  ->  SolidWorks Assembly")
    print("=" * 62)
    print(f"  CSV entrada  : {args.csv_file}")
    if not args.dry_run:
        print(f"  ASM salida   : {os.path.abspath(args.output)}")
    print("-" * 62)
    print()

    segmentos = leer_csv(args.csv_file)
    print(f"  OK  {len(segmentos)} segmento(s) leidos del CSV.\n")

    if args.dry_run:
        dry_run(segmentos, args.output)
        print("=" * 62)
        print("  Dry run completo - CSV valido, listo para usar con SolidWorks.")
        print("=" * 62)
        print()
        return

    sw  = iniciar_solidworks()
    print(f"  OK  SolidWorks revision {sw.RevisionNumber}\n")

    doc = crear_ensamblaje(sw, args.output, args.plantilla)
    crear_puntos_sketch(doc, segmentos)
    guardar_doc(doc, args.output)
    cerrar_doc(sw, args.output)

    print()
    print("=" * 62)
    print("  Ensamblaje creado, guardado y cerrado.")
    print(f"  Archivo: {os.path.abspath(args.output)}")
    print("=" * 62)
    print()


if __name__ == "__main__":
    main()
