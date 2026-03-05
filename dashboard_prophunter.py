import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Prop Hunter - Dashboard", layout="wide")

@st.cache_data
def load_data():
    # Usamos read_excel que es mucho más estable para datos de Zaragoza con eñes y tildes
    df = pd.read_excel("datos.xlsx")
    
    # Limpieza rápida de columnas por si acaso
    df.columns = df.columns.str.strip()
    
    # Convertir a números lo que deba ser número
    cols_moneda = ['GDV VENTA (€)', 'M² TOTALES', 'VIVIENDAS']
    for col in cols_moneda:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

try:
    df = load_data()

    st.title("🚀 Prop Hunter - Análisis de Cartera")
    st.markdown("---")

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

    # Gráficos
    col_a, col_b = st.columns(2)
    
    with col_a:
        if 'PERFIL DE ACTIVO' in df.columns:
            fig1 = px.pie(df, names='PERFIL DE ACTIVO', title="Distribución por Perfil")
            st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        if 'CP' in df.columns:
            # Agrupamos por CP para ver el volumen
            df_cp = df.groupby('CP')['GDV VENTA (€)'].sum().reset_index()
            fig2 = px.bar(df_cp, x='CP', y='GDV VENTA (€)', title="GDV por Código Postal", color='GDV VENTA (€)')
            st.plotly_chart(fig2, use_container_width=True)

    st.success("Dashboard cargado correctamente desde Excel ✅")

except Exception as e:
    st.error(f"Error al cargar el Excel: {e}")
    st.info("Asegúrate de que el archivo se llame 'datos.xlsx' y esté en GitHub.")
