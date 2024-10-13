import streamlit as st
import pandas as pd
from sqlalchemy import create_engine


#_____________________________________CONFIGURACION INICIAL__________________________________________#
st.set_page_config(
    page_title="Home",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.write(
    f'<h1 style="text-align: center; color: #dd0034;">Interfaz de Análisis de Datos: Resumen de Propiedades</h1>',
    unsafe_allow_html=True
)
st.write("---")

#_____________________________________CONEXION BASE DE DATOS_________________________________________#

conn = st.connection("postgresql", type="sql")

#_____________________________________FUNCION CACHÉ_________________________________________#
@st.cache_data
def load_data(query):
    return conn.query(query)

#_____________________________________FUNCION QUERY_________________________________________#
if conn:
    try:
        # Perform query
        df = conn.query('SELECT * FROM locales')

        # Display the results in a table with color formatting
        with st.expander("Vista Previa de Datos"):
            df_formatted = df.style.background_gradient(cmap='YlOrRd', subset=['Valor', 'Metros', 'Administración', 'Baños', 'Garaje', 'Antigüedad']) \
                                 .highlight_max(subset=['Valor'], color='green') \
                                 .highlight_min(subset=['Valor'], color='red')
            st.dataframe(df_formatted, use_container_width=True)
    except Exception as e:
        st.error(f"Error retrieving data: {e}")
        



#______________________________________SIDEBAR______________________________________#

with st.sidebar:
    st.title('Filtros')

    if not df.empty:  # Verifica si df no está vacío
        # Lista de barrios únicos y filtrado por barrio seleccionado
        barrio_list = list(df['Barrio'].unique())[::-1]
        selected_barrio = st.selectbox('Seleccionar Barrio', barrio_list)

        # Filtrar el DataFrame por el barrio seleccionado
        df_selected = df[df['Barrio'] == selected_barrio]
    else:
        st.warning("No hay datos disponibles para mostrar.")

#________________________________COLUMNAS______________________________________#

# Estilos CSS para las tarjetas
card_style = """
<style>
.card {
    background-color: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 20px;
    margin: 10px;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
}
</style>
"""

st.markdown(card_style, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Tarjeta para Total de Propiedades
    total_banos = df['Antigüedad'].count() if not df.empty else 0
    st.markdown(f'<div class="card" style="text-align: center;"><h4>Total Propiedades</h4><h3 style="color: #dd0034;"> {total_banos:,}</h3></div>', unsafe_allow_html=True)
    
with col2:
    # Tarjeta para Promedio Valor Total
    promedio_valor = round(df['Valor'].mean()) if not df.empty else 0
    st.markdown(f'<div class="card" style="text-align: center;"><h4>Promedio Total</h4><h3 style="color: #dd0034;">$ {promedio_valor:,}</h3></div>', unsafe_allow_html=True)

with col3:
    # Tarjeta para Total de Propiedades
    total_banos = df['Antigüedad'].count() if not df.empty else 0
    st.markdown(f'<div class="card" style="text-align: center;"><h4>Total Propiedades</h4><h3 style="color: #dd0034;">$ {total_banos:,}</h3></div>', unsafe_allow_html=True)

with col4:
    # Tarjeta para Total de Propiedades
    total_banos = df['Antigüedad'].count() if not df.empty else 0
    st.markdown(f'<div class="card" style="text-align: center;"><h4>Total Propiedades</h4><h3 style="color: #dd0034;">$ {total_banos:,}</h3></div>', unsafe_allow_html=True)

st.write("---")

#________________________________COLUMNAS______________________________________#

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('#### Recuento de Propiedades')
    property_count = df_selected.shape[0] if 'df_selected' in locals() else 0
    st.metric(label=f"{selected_barrio}", value=property_count)

with col2:
    st.markdown('#### Precio Promedio Ubicación')
    valor = df_selected['Valor'].mean() if not df_selected.empty else 0
    st.metric(label="Precio Promedio", value=f"${valor:,.2f}")

with col3:
    st.markdown('#### Área Promedio deacuerdo a la Ubicación')
    area = df_selected['Metros'].mean() if not df_selected.empty else 0
    st.metric(label="Área Promedio", value=f"{area:} m²")
        
with col4:
    st.markdown('#### Valor por Metro Cuadrado')
    valor_por_metro_cuadrado = (df_selected['Valor'] / df_selected['Metros']).mean() if not df_selected.empty else 0
    st.metric(label="", value=f"${valor_por_metro_cuadrado:,.2f}")


st.write("---")



