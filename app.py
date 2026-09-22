import streamlit as st
from fpdf import FPDF
import datetime

from core.motor_calculo import calcular_presupuesto, cargar_configuracion

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cotizador EdificaNova", page_icon="🏗️", layout="wide")

# La información comercial y de costos se administra desde un único CSV editable.
try:
    CONFIG = cargar_configuracion()
except (OSError, ValueError) as e:
    st.error(f"No se pudo cargar la configuración comercial: {e}")
    st.stop()

def opciones(categoria):
    return {k: v.get("nombre", k) for k, v in CONFIG[categoria].items()}



def generar_pdf(cliente, m2, tipologia, sistema, entrega, revestimiento, pago,
                 costo_const, distancia, recargo_flete, total):
    """Genera un archivo PDF profesional con el desglose del presupuesto"""
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
    pdf.cell(40, 10, txt=f"${costo_const:,.2f}", align='R', ln=True)

    pdf.cell(150, 10, txt=f"2. Costo Logístico (Flete por {distancia} km):")
    pdf.cell(40, 10, txt=f"${recargo_flete:,.2f}", align='R', ln=True)
    pdf.ln(5)

    # Total Final
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(200, 50, 50)  # Rojo para resaltar el total
    pdf.cell(150, 12, txt="TOTAL PRESUPUESTADO:")
    pdf.cell(40, 12, txt=f"${total:,.2f}", align='R', ln=True)

    return pdf.output(dest="S").encode("latin-1")


# --- INTERFAZ GRÁFICA ---
st.title("🏗️ Cotizador Comercial - EdificaNova")
st.markdown("Generación de presupuestos paramétricos basados en reglas de negocio.")

col_cliente, col_tecnica = st.columns([1, 2])

with col_cliente:
    st.header("👤 Datos del Cliente")
    cliente = st.text_input("Nombre y Apellido", placeholder="Ej: Juan Pérez")
    ubicaciones = opciones("ubicacion")
    ubicacion = st.selectbox("Ubicación de la Obra", list(ubicaciones), format_func=lambda x: ubicaciones[x])
    distancia_default = int(CONFIG["ubicacion"][ubicacion].get("valor_extra", 0))
    distancia = st.number_input("Distancia Logística Exacta (km)", min_value=0, value=distancia_default, step=5,
                                 help="Distancia editable. El valor inicial se obtiene del CSV según la ubicación.")
    pagos = opciones("forma_pago")
    pago = st.selectbox("Forma de Pago de Interés", list(pagos), format_func=lambda x: pagos[x])

with col_tecnica:
    st.header("📐 Especificaciones del Proyecto")
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        m2 = st.number_input("Superficie de Referencia (m²)", min_value=20, value=55, step=5)
        tipologias = opciones("tipologia")
        tipologia = st.selectbox("Tipología", list(tipologias), format_func=lambda x: tipologias[x])
    with row1_col2:
        sistemas = opciones("sistema_constructivo")
        sistema = st.selectbox("Sistema Constructivo", list(sistemas), format_func=lambda x: sistemas[x],
                                help="Los valores se administran desde configuracion_comercial.csv")
        entregas = opciones("modalidad_entrega")
        entrega = st.selectbox("Modalidad de Entrega", list(entregas), format_func=lambda x: entregas[x])
        revestimientos = opciones("revestimiento")
        revestimiento = st.selectbox("Revestimiento", list(revestimientos), format_func=lambda x: revestimientos[x])

st.markdown("---")

if st.button("Generar Cotización Formal", type="primary", use_container_width=True):
    if not cliente:
        st.warning("⚠️ Por favor, ingrese el nombre del cliente antes de cotizar.")
    else:
        try:
            resultado = calcular_presupuesto(m2=m2, sistema=sistema, entrega=entrega, distancia=distancia)
        except ValueError as e:
            st.error(f"⚠️ No se pudo calcular el presupuesto: {e}")
        else:
            costo_construccion = resultado["costo_construccion"]
            recargo_logistica = resultado["recargo_logistica"]
            presupuesto_total = resultado["total"]

            st.header("📊 Resumen Económico")

            col_a, col_b, col_c = st.columns(3)
            col_a.metric(label="Valor Construcción", value=f"${costo_construccion:,.0f}")
            col_b.metric(label="Logística y Fletes", value=f"${recargo_logistica:,.0f}")
            col_c.metric(label="VALOR TOTAL", value=f"${presupuesto_total:,.0f}")

            with st.expander("ℹ️ Transparencia del Cálculo (Explicación para el cliente)"):
                st.write(f"**Precio por m² aplicado:** ${resultado['precio_m2_aplicado']:,.0f}")
                st.write(f"**Flete Logístico:** {distancia} km a razón del costo por km configurado.")

            st.markdown("---")
            st.subheader("📄 Documentación Comercial")

            pdf_bytes = generar_pdf(
                cliente, m2, tipologia, sistema, entrega, revestimiento, pagos[pago],
                costo_construccion, distancia, recargo_logistica, presupuesto_total
            )

            st.download_button(
                label=f"⬇️ Descargar Presupuesto de {cliente} (PDF)",
                data=pdf_bytes,
                file_name=f"Presupuesto_EdificaNova_{cliente.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
