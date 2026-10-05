"""
Módulo de persistencia del histórico de cotizaciones — EdificaNova v0.3.0.

Guarda cada cotización generada en data/historico.csv y permite
consultarlo sin depender de la interfaz Streamlit.
"""
import csv
import os
from datetime import datetime

_HISTORICO_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "historico.csv"
)

COLUMNAS = [
    "fecha",
    "cliente",
    "ubicacion",
    "distancia_km",
    "m2",
    "tipologia",
    "sistema_constructivo",
    "modalidad_entrega",
    "revestimiento",
    "forma_pago",
    "costo_construccion",
    "recargo_logistica",
    "total",
]


def guardar_cotizacion(datos: dict, path: str = None) -> None:
    """
    Persiste una cotización al final del CSV histórico.

    Parameters
    ----------
    datos : dict
        Debe contener todas las claves de COLUMNAS.
    path : str, opcional
        Ruta al CSV. Por defecto usa data/historico.csv.

    Raises
    ------
    ValueError
        Si faltan campos obligatorios en `datos`.
    """
    path = path or _HISTORICO_PATH

    faltantes = [c for c in COLUMNAS if c not in datos and c != "fecha"]
    if faltantes:
        raise ValueError(f"Faltan campos obligatorios: {faltantes}")

    fila = {col: datos.get(col, "") for col in COLUMNAS}
    if not fila["fecha"]:
        fila["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    archivo_nuevo = not os.path.exists(path) or os.path.getsize(path) == 0

    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS)
        if archivo_nuevo:
            writer.writeheader()
        writer.writerow(fila)


def leer_historico(path: str = None, ultimas: int = None) -> list[dict]:
    """
    Devuelve las cotizaciones guardadas como lista de diccionarios.

    Parameters
    ----------
    path : str, opcional
        Ruta al CSV. Por defecto usa data/historico.csv.
    ultimas : int, opcional
        Si se indica, devuelve solo las N últimas filas.

    Returns
    -------
    list[dict]
        Lista de cotizaciones. Vacía si el archivo no existe.
    """
    path = path or _HISTORICO_PATH

    if not os.path.exists(path):
        return []

    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if ultimas is not None:
        rows = rows[-ultimas:]

    return rows
