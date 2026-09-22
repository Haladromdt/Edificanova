"""
Motor de cálculo de EdificaNova.

Los costos, multiplicadores y opciones comerciales se leen desde
CSV (data/configuracion_comercial.csv). La lógica permanece separada
de Streamlit para facilitar testing y mantenimiento.
"""
import csv
import os

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "configuracion_comercial.csv")


def cargar_configuracion(path: str = None) -> dict:
    """Carga costos, multiplicadores y opciones comerciales desde un CSV."""
    path = path or _DATA_PATH
    config = {
        "costos": {},
        "sistema_constructivo": {},
        "modalidad_entrega": {},
        "ubicacion": {},
        "forma_pago": {},
        "tipologia": {},
        "revestimiento": {},
    }

    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"categoria", "codigo", "nombre", "valor", "valor_extra", "activo", "descripcion"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError("El CSV debe contener las columnas: categoria,codigo,nombre,valor,valor_extra,activo,descripcion")

        for row in reader:
            if str(row["activo"]).strip().lower() not in {"1", "true", "si", "sí", "yes", "x"}:
                continue

            categoria = row["categoria"].strip()
            codigo = row["codigo"].strip()
            nombre = row["nombre"].strip()
            valor = row["valor"].strip()
            valor_extra = row["valor_extra"].strip()
            descripcion = row["descripcion"].strip()

            if categoria == "costo":
                if not valor:
                    raise ValueError(f"Falta valor para el costo '{codigo}'.")
                config["costos"][codigo] = float(valor)
            elif categoria in config and categoria != "costos":
                item = {
                    "nombre": nombre or codigo,
                    "descripcion": descripcion,
                }
                if valor:
                    item["valor"] = float(valor)
                if valor_extra:
                    item["valor_extra"] = float(valor_extra)
                config[categoria][codigo] = item
            else:
                raise ValueError(f"Categoría desconocida en CSV: {categoria}")

    return config


def cargar_multiplicadores(path: str = None) -> dict:
    """Compatibilidad con el nombre utilizado en versiones anteriores."""
    config = cargar_configuracion(path)
    return {
        "costo_base_m2": config["costos"]["costo_base_m2"],
        "costo_flete_km": config["costos"]["costo_flete_km"],
        "sistema_constructivo": {
            k: v["valor"] for k, v in config["sistema_constructivo"].items()
        },
        "modalidad_entrega": {
            k: v["valor"] for k, v in config["modalidad_entrega"].items()
        },
    }


def calcular_presupuesto(m2: float, sistema: str, entrega: str, distancia: float,
                          multiplicadores: dict = None) -> dict:
    """Calcula el desglose de un presupuesto (RF02)."""
    if multiplicadores is None:
        multiplicadores = cargar_multiplicadores()

    if m2 is None or m2 <= 0:
        raise ValueError("La superficie (m2) debe ser mayor a 0.")
    if distancia is None or distancia < 0:
        raise ValueError("La distancia no puede ser negativa.")
    if sistema not in multiplicadores["sistema_constructivo"]:
        raise ValueError(f"Sistema constructivo desconocido: {sistema}")
    if entrega not in multiplicadores["modalidad_entrega"]:
        raise ValueError(f"Modalidad de entrega desconocida: {entrega}")

    costo_base_m2 = multiplicadores["costo_base_m2"]
    costo_flete_km = multiplicadores["costo_flete_km"]
    mult_sistema = multiplicadores["sistema_constructivo"][sistema]
    mult_entrega = multiplicadores["modalidad_entrega"][entrega]

    precio_m2_aplicado = costo_base_m2 * mult_sistema * mult_entrega
    costo_construccion = m2 * precio_m2_aplicado
    recargo_logistica = distancia * costo_flete_km
    total = costo_construccion + recargo_logistica

    return {
        "precio_m2_aplicado": precio_m2_aplicado,
        "costo_construccion": costo_construccion,
        "recargo_logistica": recargo_logistica,
        "total": total,
    }
