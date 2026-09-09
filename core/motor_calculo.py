"""
Motor de cálculo de EdificaNova.

Funciones puras, sin dependencia de Streamlit, para que puedan
testearse de forma aislada (ver tests/test_motor_calculo.py).

Los valores de costos y multiplicadores NO están hardcodeados acá:
se leen de data/multiplicadores.json (RD01 - tabla editable).
"""
import json
import os

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "multiplicadores.json")


def cargar_multiplicadores(path: str = None) -> dict:
    """Carga la tabla de costos y multiplicadores desde el JSON editable."""
    path = path or _DATA_PATH
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def calcular_presupuesto(m2: float, sistema: str, entrega: str, distancia: float,
                          multiplicadores: dict = None) -> dict:
    """
    Calcula el desglose de un presupuesto (RF02).

    Parámetros:
        m2: superficie a construir (debe ser > 0)
        sistema: clave de sistema constructivo (ej. "E.E", "W.F", "S.F")
        entrega: clave de modalidad de entrega (ej. "OBRA GRIS", "LLAVE EN MANO")
        distancia: distancia logística en km (debe ser >= 0)
        multiplicadores: tabla ya cargada (opcional, para inyectar en tests).
            Si no se pasa, se carga desde data/multiplicadores.json.

    Devuelve un dict con: precio_m2_aplicado, costo_construccion,
    recargo_logistica, total.

    Lanza ValueError si algún input es inválido (RNF03: cálculo
    reproducible y sin intervención manual ante datos incorrectos).
    """
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
