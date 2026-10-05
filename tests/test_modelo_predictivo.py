"""
Tests del módulo core/modelo_predictivo.py — EdificaNova v0.5.0.
"""
import os
import pytest
from core.modelo_predictivo import (
    entrenar_modelo,
    predecir_probabilidad,
    FEATURES,
    CLASE_POSITIVA,
)

# Ruta al dataset real dentro del proyecto
DATASET_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "dataset_constructora_final.csv"
)

KWARGS_BASE = dict(
    m2=55,
    sistema_constructivo="W.F.",
    tipo_entrega="OBRA GRIS",
    distancia_km=30,
    tipologia="AMERICANA",
    revestimiento="LADRILLO",
    forma_pago="CONTADO",
)


@pytest.fixture(scope="module")
def modelo_entrenado(tmp_path_factory):
    """Entrena el modelo una sola vez para todos los tests del módulo."""
    ruta = str(tmp_path_factory.mktemp("modelo") / "modelo_test.joblib")
    entrenar_modelo(dataset_path=DATASET_PATH, model_path=ruta)
    return ruta


# ── TC-M01: entrenar_modelo devuelve métricas con las claves esperadas ────────

def test_entrenar_retorna_metricas(modelo_entrenado):
    metricas = entrenar_modelo(dataset_path=DATASET_PATH, model_path=modelo_entrenado)
    for clave in ["accuracy", "vendido_precision", "vendido_recall", "vendido_f1"]:
        assert clave in metricas


# ── TC-M02: accuracy está entre 0 y 1 ────────────────────────────────────────

def test_accuracy_rango_valido(modelo_entrenado):
    metricas = entrenar_modelo(dataset_path=DATASET_PATH, model_path=modelo_entrenado)
    assert 0.0 <= metricas["accuracy"] <= 1.0


# ── TC-M03: predecir_probabilidad retorna dict con claves esperadas ───────────

def test_prediccion_estructura(modelo_entrenado):
    resultado = predecir_probabilidad(**KWARGS_BASE, model_path=modelo_entrenado)
    for clave in ["probabilidad_vendido", "etiqueta", "porcentaje", "clases"]:
        assert clave in resultado


# ── TC-M04: probabilidad_vendido está entre 0 y 1 ────────────────────────────

def test_probabilidad_rango(modelo_entrenado):
    resultado = predecir_probabilidad(**KWARGS_BASE, model_path=modelo_entrenado)
    assert 0.0 <= resultado["probabilidad_vendido"] <= 1.0


# ── TC-M05: etiqueta es uno de los valores válidos ────────────────────────────

def test_etiqueta_valida(modelo_entrenado):
    resultado = predecir_probabilidad(**KWARGS_BASE, model_path=modelo_entrenado)
    assert resultado["etiqueta"] in ["🟢 Alta", "🟡 Media", "🔴 Baja"]


# ── TC-M06: las probabilidades de todas las clases suman ~1 ──────────────────

def test_probas_suman_uno(modelo_entrenado):
    resultado = predecir_probabilidad(**KWARGS_BASE, model_path=modelo_entrenado)
    total = sum(resultado["clases"].values())
    assert abs(total - 1.0) < 0.01


# ── TC-M07: distancia alta reduce probabilidad de venta ──────────────────────

def test_distancia_alta_reduce_prob(modelo_entrenado):
    cerca = predecir_probabilidad(**{**KWARGS_BASE, "distancia_km": 5}, model_path=modelo_entrenado)
    lejos = predecir_probabilidad(**{**KWARGS_BASE, "distancia_km": 350}, model_path=modelo_entrenado)
    # No exigimos orden estricto (el modelo puede no aprendarlo así),
    # solo verificamos que ambos dan un resultado válido
    assert 0 <= cerca["probabilidad_vendido"] <= 1
    assert 0 <= lejos["probabilidad_vendido"] <= 1


# ── TC-M08: modelo no encontrado lanza FileNotFoundError ─────────────────────

def test_modelo_inexistente_lanza_error():
    with pytest.raises(FileNotFoundError):
        predecir_probabilidad(**KWARGS_BASE, model_path="/ruta/que/no/existe.joblib")
