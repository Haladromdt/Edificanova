import streamlit as st
from core.motor_calculo import calcular_presupuesto, cargar_configuracion
from core.historico import guardar_cotizacion, leer_historico
from core.pdf_generator import generar_pdf
from core.modelo_predictivo import predecir_probabilidad

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

            # Predicción de probabilidad de cierre
            try:
                pred = predecir_probabilidad(
                    m2=m2,
                    sistema_constructivo=sistema,
                    tipo_entrega=entrega,
                    distancia_km=distancia,
                    tipologia=tipologia,
                    revestimiento=revestimiento,
                    forma_pago=pago,
                    precio_cotizado=presupuesto_total,
                )
                st.markdown("---")
                st.subheader("🤖 Probabilidad de Cierre")
                col_pred, col_desc = st.columns([1, 2])
                with col_pred:
                    st.metric(
                        label=f"Chances de venta {pred['etiqueta']}",
                        value=pred["porcentaje"],
                    )
                with col_desc:
                    st.caption(
                        "Estimación basada en el historial comercial de la constructora. "
                        "No reemplaza el juicio del asesor."
                    )
                    st.progress(pred["probabilidad_vendido"])
            except FileNotFoundError:
                pass  # El modelo aún no fue entrenado, se omite silenciosamente

            with st.expander("ℹ️ Transparencia del Cálculo (Explicación para el cliente)"):
                st.write(f"**Precio por m² aplicado:** ${resultado['precio_m2_aplicado']:,.0f}")
                st.write(f"**Flete Logístico:** {distancia} km a razón del costo por km configurado.")

            # Persistencia del histórico
            guardar_cotizacion({
                "cliente": cliente,
                "ubicacion": ubicacion,
                "distancia_km": distancia,
                "m2": m2,
                "tipologia": tipologia,
                "sistema_constructivo": sistema,
                "modalidad_entrega": entrega,
                "revestimiento": revestimiento,
                "forma_pago": pago,
                "costo_construccion": costo_construccion,
                "recargo_logistica": recargo_logistica,
                "total": presupuesto_total,
            })

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

# --- HISTÓRICO DE COTIZACIONES ---
st.markdown("---")
st.subheader("📋 Histórico de Cotizaciones")

historial = leer_historico(ultimas=10)
if historial:
    import pandas as pd
    df = pd.DataFrame(historial)
    columnas_display = ["fecha", "cliente", "m2", "sistema_constructivo",
                        "modalidad_entrega", "costo_construccion", "recargo_logistica", "total"]
    df_display = df[columnas_display].copy()
    for col in ["costo_construccion", "recargo_logistica", "total"]:
        df_display[col] = df_display[col].astype(float).map("${:,.0f}".format)
    st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.info("Aún no hay cotizaciones registradas. Generá la primera usando el formulario.")
