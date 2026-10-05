"""
Tests del módulo core/pdf_generator.py — EdificaNova v0.4.0.
"""
import pytest
from core.pdf_generator import generar_pdf

# Datos base para todos los tests
KWARGS_BASE = dict(
    cliente="Ana García",
    m2=80,
    tipologia="AMERICANA",
    sistema="W.F.",
    entrega="OBRA GRIS",
    revestimiento="LADRILLO",
    pago="Contado",
    costo_construccion=880000.0,
    distancia=20,
    recargo_logistica=30000.0,
    total=910000.0,
)


# ── TC-P01: la función retorna bytes ─────────────────────────────────────────

def test_retorna_bytes():
    resultado = generar_pdf(**KWARGS_BASE)
    assert isinstance(resultado, bytes)


# ── TC-P02: el PDF tiene tamaño razonable (> 1 KB) ───────────────────────────

def test_tamano_minimo():
    resultado = generar_pdf(**KWARGS_BASE)
    assert len(resultado) > 1024


# ── TC-P03: la firma del PDF es válida (%PDF-) ───────────────────────────────

def test_firma_pdf():
    resultado = generar_pdf(**KWARGS_BASE)
    assert resultado.startswith(b"%PDF-")


# ── TC-P04: PDFs con distinto cliente tienen distinto tamaño o contenido ──────
# fpdf2 comprime el stream; no se puede buscar texto en crudo.
# Verificamos que dos clientes distintos producen bytes distintos.

def test_pdf_varia_por_cliente():
    pdf1 = generar_pdf(**KWARGS_BASE)
    pdf2 = generar_pdf(**{**KWARGS_BASE, "cliente": "Otro Cliente"})
    assert pdf1 != pdf2


# ── TC-P05: PDFs con distinto total tienen distinto contenido ─────────────────

def test_pdf_varia_por_total():
    pdf1 = generar_pdf(**KWARGS_BASE)
    pdf2 = generar_pdf(**{**KWARGS_BASE, "total": 999999.0})
    assert pdf1 != pdf2


# ── TC-P06: PDFs distintos para clientes distintos ───────────────────────────

def test_pdfs_distintos_por_cliente():
    pdf1 = generar_pdf(**KWARGS_BASE)
    kwargs2 = {**KWARGS_BASE, "cliente": "Carlos López"}
    pdf2 = generar_pdf(**kwargs2)
    assert pdf1 != pdf2


# ── TC-P07: funciona con distancia 0 ─────────────────────────────────────────

def test_distancia_cero():
    kwargs = {**KWARGS_BASE, "distancia": 0, "recargo_logistica": 0.0}
    resultado = generar_pdf(**kwargs)
    assert resultado.startswith(b"%PDF-")


# ── TC-P08: funciona con m2 mínimo (20) ──────────────────────────────────────

def test_m2_minimo():
    kwargs = {**KWARGS_BASE, "m2": 20, "costo_construccion": 220000.0, "total": 220000.0}
    resultado = generar_pdf(**kwargs)
    assert len(resultado) > 1024
