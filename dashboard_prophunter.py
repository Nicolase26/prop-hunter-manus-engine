import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Prop Hunter - Dashboard Inversión", layout="wide")

st.title("🚀 Prop Hunter | Zaragoza Real Estate Dashboard V10")
st.markdown("---")

# Carga de datos (Usando el nombre de tu archivo)
@st.cache_data
def load_data():
    # Cargamos la pestaña del listado financiero
    df = pd.read_csv("datos.csv", encoding="latin1")
    # Limpieza básica de números
    df['GDV VENTA (€)'] = pd.to_numeric(df['GDV VENTA (€)'], errors='coerce')
    # Añadimos la columna de Auditoría que pactamos
    if 'ESTADO_AUDITORIA' not in df.columns:
        df['ESTADO_AUDITORIA'] = 'En Estudio'
    return df

df = load_data()

# --- FILTROS LATERALES ---
st.sidebar.header("Filtros de Búsqueda")
zona = st.sidebar.multiselect("Filtrar por CP:", options=df["CP"].unique(), default=df["CP"].unique())
perfil = st.sidebar.multiselect("Perfil de Activo:", options=df["PERFIL DE ACTIVO"].unique(), default=df["PERFIL DE ACTIVO"].unique())

df_filtered = df[(df["CP"].isin(zona)) & (df["PERFIL DE ACTIVO"].isin(perfil))]

# --- BLOQUE 1: KPIs ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Activos", f"{len(df_filtered)}")
with col2:
    total_gdv = df_filtered['GDV VENTA (€)'].sum() / 1e6
    st.metric("GDV Total", f"{total_gdv:,.1f} M€")
with col3:
    total_m2 = df_filtered['M² TOTALES'].sum()
    st.metric("Superficie Total", f"{total_m2:,.0f} m²")
with col4:
    total_viviendas = df_filtered['VIVIENDAS'].sum()
    st.metric("Potencial Viviendas", f"{total_viviendas:,.0f} Uds")

st.markdown("---")

# --- BLOQUE 2: GRÁFICOS ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Distribución por Perfil de Activo")
    fig_perfil = px.pie(df_filtered, names='PERFIL DE ACTIVO', values='GDV VENTA (€)', hole=0.4)
    st.plotly_chart(fig_perfil, use_container_width=True)

with c2:
    st.subheader("Inversión por Código Postal")
    fig_cp = px.bar(df_filtered, x='CP', y='GDV VENTA (€)', color='CP', title="GDV por Zona")
    st.plotly_chart(fig_cp, use_container_width=True)

# --- BLOQUE 3: TABLA DE DATOS ---
st.subheader("Listado Detallado de Activos")
st.dataframe(df_filtered[['ID_OFICIAL', 'DIRECCIÓN', 'CP', 'VIVIENDAS', 'GDV VENTA (€)', 'ESTADO_AUDITORIA']], use_container_width=True)


