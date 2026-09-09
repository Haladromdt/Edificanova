"""
Tests del motor de cálculo — alcance v0.2.0 (Semanas 5-7).

Cubren los casos de prueba 1, 2 y 5 definidos en la Evidencia de
Aprendizaje de Testeo de Software. Los casos 3 (PDF) y 4 (histórico)
se agregan en v0.3.0, cuando esas piezas existan.
"""
import pytest
from core.motor_calculo import calcular_presupuesto

MULTIPLICADORES_TEST = {
    "costo_base_m2": 280000,
    "costo_flete_km": 1500,
    "sistema_constructivo": {"E.E": 1.0, "W.F": 1.15, "S.F": 1.25},
    "modalidad_entrega": {"OBRA GRIS": 1.0, "LLAVE EN MANO": 1.40},
}


# --- Caso 1: Cálculo correcto de presupuesto según sistema constructivo ---

def test_calculo_correcto_segun_sistema():
    resultado = calcular_presupuesto(
        m2=55, sistema="W.F", entrega="OBRA GRIS", distancia=15,
        multiplicadores=MULTIPLICADORES_TEST,
    )
    precio_m2_esperado = 280000 * 1.15 * 1.0
    assert resultado["precio_m2_aplicado"] == precio_m2_esperado
    assert resultado["costo_construccion"] == 55 * precio_m2_esperado
    assert resultado["recargo_logistica"] == 15 * 1500
    assert resultado["total"] == resultado["costo_construccion"] + resultado["recargo_logistica"]


def test_modalidad_llave_en_mano_encarece_respecto_a_obra_gris():
    obra_gris = calcular_presupuesto(m2=55, sistema="E.E", entrega="OBRA GRIS", distancia=15,
                                      multiplicadores=MULTIPLICADORES_TEST)
    llave_en_mano = calcular_presupuesto(m2=55, sistema="E.E", entrega="LLAVE EN MANO", distancia=15,
                                          multiplicadores=MULTIPLICADORES_TEST)
    assert llave_en_mano["total"] > obra_gris["total"]


# --- Caso 2: Validación de campos obligatorios / inválidos ---

def test_rechaza_sistema_constructivo_desconocido():
    with pytest.raises(ValueError):
        calcular_presupuesto(m2=55, sistema="NO_EXISTE", entrega="OBRA GRIS", distancia=15,
                              multiplicadores=MULTIPLICADORES_TEST)


def test_rechaza_modalidad_entrega_desconocida():
    with pytest.raises(ValueError):
        calcular_presupuesto(m2=55, sistema="E.E", entrega="NO_EXISTE", distancia=15,
                              multiplicadores=MULTIPLICADORES_TEST)


def test_rechaza_m2_cero_o_negativo():
    with pytest.raises(ValueError):
        calcular_presupuesto(m2=0, sistema="E.E", entrega="OBRA GRIS", distancia=15,
                              multiplicadores=MULTIPLICADORES_TEST)
    with pytest.raises(ValueError):
        calcular_presupuesto(m2=-10, sistema="E.E", entrega="OBRA GRIS", distancia=15,
                              multiplicadores=MULTIPLICADORES_TEST)


def test_rechaza_distancia_negativa():
    with pytest.raises(ValueError):
        calcular_presupuesto(m2=55, sistema="E.E", entrega="OBRA GRIS", distancia=-5,
                              multiplicadores=MULTIPLICADORES_TEST)


# --- Caso 5: Cálculo con valores límite ---

def test_valores_limite_m2_muy_bajo():
    resultado = calcular_presupuesto(m2=1, sistema="E.E", entrega="OBRA GRIS", distancia=0,
                                      multiplicadores=MULTIPLICADORES_TEST)
    assert resultado["total"] > 0


def test_valores_limite_m2_muy_alto():
    resultado = calcular_presupuesto(m2=100000, sistema="S.F", entrega="LLAVE EN MANO", distancia=500,
                                      multiplicadores=MULTIPLICADORES_TEST)
    assert resultado["total"] > 0
    assert resultado["costo_construccion"] > resultado["recargo_logistica"]
