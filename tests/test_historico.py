"""
Tests del módulo core/historico.py — EdificaNova v0.3.0.
"""
import os
import csv
import pytest
from core.historico import guardar_cotizacion, leer_historico, COLUMNAS

# Datos mínimos válidos para una cotización de prueba
COTIZACION_BASE = {
    "fecha": "2025-01-01 10:00:00",
    "cliente": "Test Cliente",
    "ubicacion": "CORDOBA_CAPITAL",
    "distancia_km": 15,
    "m2": 55,
    "tipologia": "AMERICANA",
    "sistema_constructivo": "W.F.",
    "modalidad_entrega": "OBRA GRIS",
    "revestimiento": "LADRILLO",
    "forma_pago": "CONTADO",
    "costo_construccion": 605000,
    "recargo_logistica": 22500,
    "total": 627500,
}


@pytest.fixture
def archivo_tmp(tmp_path):
    """Ruta a un CSV temporal para cada test."""
    return str(tmp_path / "historico_test.csv")


# ── TC-H01: guardar una cotización crea el archivo ────────────────────────────

def test_guardar_crea_archivo(archivo_tmp):
    guardar_cotizacion(COTIZACION_BASE, path=archivo_tmp)
    assert os.path.exists(archivo_tmp)


# ── TC-H02: el archivo incluye encabezado y una fila ──────────────────────────

def test_guardar_escribe_encabezado_y_fila(archivo_tmp):
    guardar_cotizacion(COTIZACION_BASE, path=archivo_tmp)
    with open(archivo_tmp, encoding="utf-8") as f:
        lineas = f.readlines()
    assert len(lineas) == 2  # encabezado + 1 fila


# ── TC-H03: guardar dos cotizaciones produce dos filas ────────────────────────

def test_guardar_acumula_filas(archivo_tmp):
    guardar_cotizacion(COTIZACION_BASE, path=archivo_tmp)
    guardar_cotizacion(COTIZACION_BASE, path=archivo_tmp)
    rows = leer_historico(path=archivo_tmp)
    assert len(rows) == 2


# ── TC-H04: los valores guardados se recuperan correctamente ──────────────────

def test_datos_guardados_son_correctos(archivo_tmp):
    guardar_cotizacion(COTIZACION_BASE, path=archivo_tmp)
    rows = leer_historico(path=archivo_tmp)
    assert rows[0]["cliente"] == "Test Cliente"
    assert float(rows[0]["total"]) == 627500


# ── TC-H05: leer histórico vacío devuelve lista vacía ────────────────────────

def test_leer_historico_sin_archivo(archivo_tmp):
    rows = leer_historico(path=archivo_tmp)
    assert rows == []


# ── TC-H06: parámetro `ultimas` limita la cantidad de filas ──────────────────

def test_leer_ultimas_filas(archivo_tmp):
    for i in range(5):
        c = COTIZACION_BASE.copy()
        c["cliente"] = f"Cliente {i}"
        guardar_cotizacion(c, path=archivo_tmp)
    rows = leer_historico(path=archivo_tmp, ultimas=3)
    assert len(rows) == 3
    assert rows[-1]["cliente"] == "Cliente 4"


# ── TC-H07: guardar sin campos obligatorios lanza ValueError ──────────────────

def test_guardar_sin_campos_falla(archivo_tmp):
    incompleto = {"cliente": "Solo cliente"}
    with pytest.raises(ValueError):
        guardar_cotizacion(incompleto, path=archivo_tmp)


# ── TC-H08: fecha se asigna automáticamente si no se provee ──────────────────

def test_fecha_automatica(archivo_tmp):
    sin_fecha = {k: v for k, v in COTIZACION_BASE.items() if k != "fecha"}
    guardar_cotizacion(sin_fecha, path=archivo_tmp)
    rows = leer_historico(path=archivo_tmp)
    assert rows[0]["fecha"] != ""
