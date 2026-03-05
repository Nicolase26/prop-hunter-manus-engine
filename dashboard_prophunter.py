import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="Prop Hunter - Dashboard", layout="wide", initial_sidebar_state="collapsed")

# ----------------- INYECCIÓN CSS ESTILO DRIBBBLE -----------------
st.markdown("""
<style>
    /* Efecto Glassmorphism para las tarjetas de métricas */
    div[data-testid="metric-container"] {
        background: rgba(30, 33, 43, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 5% 5% 5% 10%;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    /* Efecto Hover (cuando pasas el ratón flotan y se iluminan) */
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(0, 240, 255, 0.5);
        box-shadow: 0 12px 40px 0 rgba(0, 240, 255, 0.2);
    }

    /* Ocultar barra superior por defecto de Streamlit */
    header {visibility: hidden;}
    
    /* Título principal con gradiente corporativo */
    h1 {
        background: -webkit-linear-gradient(45deg, #00F0FF, #0080FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        padding-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)
# -----------------------------------------------------------------

@st.cache_data
def load_data_from_text():
    with open("LISTADO_ACTIVOS_ZARAGOZA_FORMATO_TEXTO.txt", "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    blocks = content.split("------------------------------")
    data = []
    for block in blocks:
        if "ID:" not in block: continue
        try:
            gdv_match = re.search(r"GDV Estimado: (\d+)", block)
            m2_match = re.search(r"Superficie Total: (\d+)", block)
            perfil_match = re.search(r"Perfil: (.*)", block)
            if gdv_match and m2_match and perfil_match:
                data.append({
                    "GDV VENTA (€)": int(gdv_match.group(1)),
                    "M² TOTALES": int(m2_match.group(1)),
                    "PERFIL DE ACTIVO": perfil_match.group(1).strip()
                })
        except:
            pass
    return pd.DataFrame(data)

try:
    df = load_data_from_text()

    st.title("Prop Hunter | Portfolio Zaragoza")
    st.markdown("<br>", unsafe_allow_html=True)

    if len(df) > 0:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("🏢 Total Activos", f"{len(df)}")
        with c2:
            total_gdv = df['GDV VENTA (€)'].sum()
            st.metric("💎 GDV Total", f"{total_gdv:,.0f} €")
        with c3:
            total_m2 = df['M² TOTALES'].sum()
            st.metric("📐 Superficie Total", f"{total_m2:,.0f} m²")

        st.markdown("<br><br>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        
        # Gráfico 1: Tarta tipo Donut con colores Premium y fondo transparente
        with col_a:
            fig1 = px.pie(df, names='PERFIL DE ACTIVO', hole=0.6, 
                          color_discrete_sequence=px.colors.sequential.Tealgrn)
            fig1.update_layout(
                title_text="Distribución de Activos", title_x=0.5,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#A0AEC0"), showlegend=False
            )
            fig1.update_traces(textposition='outside', textinfo='percent+label')
            st.plotly_chart(fig1, use_container_width=True)

        # Gráfico 2: Barras horizontales limpias
        with col_b:
            df_perfil = df.groupby('PERFIL DE ACTIVO')['GDV VENTA (€)'].sum().reset_index()
            fig2 = px.bar(df_perfil, x='GDV VENTA (€)', y='PERFIL DE ACTIVO', orientation='h',
                          color='GDV VENTA (€)', color_continuous_scale="Blues")
            fig2.update_layout(
                title_text="Volumen de GDV (€) por Perfil", title_x=0.5,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#A0AEC0"), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Error técnico: {e}")
