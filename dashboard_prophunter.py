import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="Prop Hunter - Dashboard", layout="wide")

# Función especial para leer tu archivo de texto plano a prueba de fallos
@st.cache_data
def load_data_from_text():
    # Abrimos el archivo de texto
    with open("LISTADO_ACTIVOS_ZARAGOZA_FORMATO_TEXTO.txt", "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    # Separamos la información por la línea de guiones que tiene tu archivo
    blocks = content.split("------------------------------")
    
    data = []
    for block in blocks:
        if "ID:" not in block: 
            continue
            
        # El escáner busca las palabras clave y extrae los números
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

    st.title("🚀 Prop Hunter - Análisis de Cartera")
    st.markdown("---")

    # Si por algún casual lee 0 activos, lanzamos aviso
    if len(df) == 0:
        st.warning("No se han podido leer los datos. Asegúrate de que el archivo TXT está subido a GitHub con el nombre exacto.")
    else:
        # KPIs Principales
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Activos", f"{len(df)}")
        with c2:
            total_gdv = df['GDV VENTA (€)'].sum()
            st.metric("GDV Total", f"{total_gdv:,.0f} €")
        with c3:
            total_m2 = df['M² TOTALES'].sum()
            st.metric("Superficie Total", f"{total_m2:,.0f} m²")

        st.markdown("---")

        # Gráficos adaptados
        col_a, col_b = st.columns(2)
        
        with col_a:
            fig1 = px.pie(df, names='PERFIL DE ACTIVO', title="Distribución de Activos por Perfil")
            st.plotly_chart(fig1, use_container_width=True)

        with col_b:
            df_perfil = df.groupby('PERFIL DE ACTIVO')['GDV VENTA (€)'].sum().reset_index()
            fig2 = px.bar(df_perfil, x='PERFIL DE ACTIVO', y='GDV VENTA (€)', 
                          title="Volumen de GDV (€) por Perfil", color='PERFIL DE ACTIVO')
            st.plotly_chart(fig2, use_container_width=True)

        st.success("✅ Dashboard escaneado y cargado perfectamente desde archivo de texto.")

except Exception as e:
    st.error(f"Error técnico: {e}")
