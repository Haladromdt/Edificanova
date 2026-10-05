"""
Módulo de generación de PDF para presupuestos — EdificaNova v0.4.0.

Separa la lógica de exportación de la interfaz Streamlit,
permitiendo generar PDFs desde cualquier contexto (tests, CLI, etc.).
"""
import datetime
from fpdf import FPDF


def generar_pdf(
    cliente: str,
    m2: int,
    tipologia: str,
    sistema: str,
    entrega: str,
    revestimiento: str,
    pago: str,
    costo_construccion: float,
    distancia: int,
    recargo_logistica: float,
    total: float,
) -> bytes:
    """
    Genera un PDF profesional con el desglose del presupuesto.

    Parameters
    ----------
    cliente : str
        Nombre completo del cliente.
    m2 : int
        Superficie a construir en metros cuadrados.
    tipologia : str
        Tipología arquitectónica seleccionada.
    sistema : str
        Sistema constructivo seleccionado.
    entrega : str
        Modalidad de entrega seleccionada.
    revestimiento : str
        Revestimiento exterior seleccionado.
    pago : str
        Forma de pago consultada (nombre legible, no clave).
    costo_construccion : float
        Costo de construcción calculado (materiales + mano de obra).
    distancia : int
        Distancia logística en kilómetros.
    recargo_logistica : float
        Recargo por flete calculado.
    total : float
        Total presupuestado.

    Returns
    -------
    bytes
        Contenido del PDF listo para descargar o guardar.
    """
    pdf = FPDF()
    pdf.add_page()

    # Encabezado
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(27, 77, 62)  # Verde oscuro corporativo
    pdf.cell(200, 10, txt="PRESUPUESTO OFICIAL - EDIFICANOVA", ln=True, align='C')
    pdf.ln(5)

    # Datos del Cliente y Fecha
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 8, txt=f"Fecha de Emisión: {datetime.date.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(200, 8, txt=f"Cliente: {cliente.upper()}", ln=True)
    pdf.cell(200, 8, txt=f"Modalidad de Pago Consultada: {pago}", ln=True)
    pdf.ln(5)

    # Especificaciones Técnicas
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Especificaciones Técnicas del Proyecto", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, txt=f"- Superficie a construir: {m2} m2", ln=True)
    pdf.cell(200, 8, txt=f"- Tipología Arquitectónica: {tipologia}", ln=True)
    pdf.cell(200, 8, txt=f"- Sistema Constructivo: {sistema}", ln=True)
    pdf.cell(200, 8, txt=f"- Tipo de Entrega: {entrega}", ln=True)
    pdf.cell(200, 8, txt=f"- Revestimiento Exterior: {revestimiento}", ln=True)
    pdf.ln(8)

    # Desglose Económico
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Desglose de Inversión", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(150, 10, txt="1. Costo de Construcción (Materiales + Mano de Obra):")
    pdf.cell(40, 10, txt=f"${costo_construccion:,.2f}", align='R', ln=True)

    pdf.cell(150, 10, txt=f"2. Costo Logístico (Flete por {distancia} km):")
    pdf.cell(40, 10, txt=f"${recargo_logistica:,.2f}", align='R', ln=True)
    pdf.ln(5)

    # Total Final
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(200, 50, 50)  # Rojo para resaltar el total
    pdf.cell(150, 12, txt="TOTAL PRESUPUESTADO:")
    pdf.cell(40, 12, txt=f"${total:,.2f}", align='R', ln=True)

    return bytes(pdf.output())
