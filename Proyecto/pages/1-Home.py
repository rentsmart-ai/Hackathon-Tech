import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import leafmap.foliumap as leafmap
import requests
import json

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
        
        df['Valor_metro'] = df['Valor'] / df['Metros']
        
#_____________________________________DATAFRAME_________________________________________#
        with st.expander("Vista Previa de Datos", expanded=False):
        # Aplicar formato a los datos para la visualización
            df_formatted = df.style \
                .background_gradient(cmap='YlOrRd', subset=['Valor', 'Metros', 'Administración', 'Baños', 'Garaje', 'Antigüedad']) \
                .highlight_max(subset=['Valor'], color='green') \
                .highlight_min(subset=['Valor'], color='red')

        # Mostrar el editor de datos
            st.dataframe(
                df_formatted,  # Aquí se debe usar el DataFrame original
                column_config={
                    "Imagen": st.column_config.ImageColumn(
                        "Imagen", help="Capturas de pantalla de las aplicaciones de Streamlit"
                    ),
                    
                    "Valor_metro": st.column_config.AreaChartColumn(
                    "Valor por metro cuadrado",
                    width="medium",
                    help="Valor por metro cuadrado calculado a partir de la columna Valor y Metros",
                    y_min=0,
                    y_max=100000,
                    ),
                },
                hide_index=True,

            )
    except Exception as e:
        st.error(f"Error retrieving data: {e}")
#______________________________________ESTILOS CSS______________________________________#
# Cargar el archivo CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Llamar el archivo CSS
local_css("style/styleF.css")
#______________________________________SIDEBAR______________________________________#

with st.sidebar:
    st.title('Filtros')

    if not df.empty:  # Verifica si df no está vacío
        # Función para limpiar caracteres problemáticos
        def clean_text(value):
            try:
                # Forzar el valor a utf-8 y reemplazar caracteres no válidos
                return str(value).encode('utf-8', 'ignore').decode('utf-8')
            except Exception:
                return ""

        # Aplica la limpieza a la columna 'Barrio'
        df['Barrio'] = df['Barrio'].apply(clean_text)

        # Lista de barrios únicos y filtrado por barrio seleccionado
        barrio_list = list(df['Barrio'].unique())[::-1]

        # Mostrar un selectbox con los barrios disponibles
        selected_barrio = st.selectbox('Seleccionar Barrio', barrio_list)

        # Filtrar el DataFrame por el barrio seleccionado
        df_selected = df[df['Barrio'] == selected_barrio]


#___________________________________________COLUMNAS GENERAL___________________________________________________#
with st.container():
  st.write(f'<h3 style="text-align: center; color: #0b2d43;">Estadística General de los Datos</h3>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Tarjeta para Total de Propiedades
    total_Pro = df['Antigüedad'].count() if not df.empty else 0
    
    st.markdown(f'''
                <div class="card-dos" style="max-width: 18rem, text-align: center;">
                    <div class="card-header">Total Propiedades</div>
                    <div class="card-body">
                    <h3 style="color: #dd0034;"> {total_Pro:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
with col2:
    # Tarjeta para Promedio Valor Total
    promedio_valor = round(df['Valor'].mean()) if not df.empty else 0
    st.markdown(f'''
                <div class="card-dos" style="max-width: 18rem, text-align: center;">
                    <div class="card-header">Promedio Valor</div>
                    <div class="card-body">
                    <h3 style="color: #dd0034;">$ {promedio_valor:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

with col3:
    # Tarjeta para Promedio de valor por metro
    valor_por_metro = (df['Valor'] / df['Metros']).mean() if not df_selected.empty else 0
    valor_por_metro_redondeado = round(valor_por_metro, 2)  # Redondear a 2 decimales
    st.markdown(f'''
                <div class="card-dos" style="max-width: 18rem, text-align: center;">
                    <div class="card-header">Valor por Metro</div>
                    <div class="card-body">
                    <h3 style="color: #dd0034;">$ {valor_por_metro_redondeado:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

with col4:
    # Tarjeta para Total 
    min_antiguedad = df['Antigüedad'].min() if not df.empty else 0
    max_antiguedad = df['Antigüedad'].max() if not df.empty else 0
    st.markdown(f'''
                <div class="card-dos" style="max-width: 18rem, text-align: center;">
                    <div class="card-header">Antigüedad</div>
                    <div class="card-body">
                    <h3 style="color: #dd0034;">Min: {min_antiguedad:,} Max: {max_antiguedad:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

st.write("---")

#___________________________________________GRAFICAS METRICAS GENERAL___________________________________________________#

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(height=420):
        if not df.empty:
                promedio_valor_barrio = df.groupby('Barrio')['Valor'].mean().reset_index()
                fig = px.bar(promedio_valor_barrio,
                            x='Barrio',
                            y='Valor',
                            title='Promedio de Valor por Barrio',
                            labels={'Valor': 'Valor Promedio ($)', 'Barrio': 'Barrio'},
                            color='Valor',  
                            color_continuous_scale='Viridis')
                fig.update_layout(xaxis_title='Barrio', yaxis_title='Valor Promedio ($)', showlegend=False)
                st.plotly_chart(fig)


with col2:
    with st.container(height=420):
        if not df.empty:
            fig = px.scatter(df, x="Metros", y="Valor", color="Valor", size="Metros", hover_name="Barrio")
            fig.update_layout(title="Relación entre Metros y Valor de Propiedades",
                            xaxis_title="Metros",
                            yaxis_title="Valor ($)",
                            hovermode="closest")
            st.plotly_chart(fig, use_container_width=True)

            
with col3:
    with st.container(height=420):
        if not df.empty:
            # Crear un DataFrame con las variables garaje, baños, antigüedad
            df_multicat = df.groupby('Barrio')[['Garaje', 'Baños', 'Antigüedad']].mean().reset_index()

            # Transformar el DataFrame para que sea adecuado para un gráfico de barras horizontales
            df_multicat = df_multicat.melt(id_vars='Barrio', 
                                            value_vars=['Garaje', 'Baños', 'Antigüedad'], 
                                            var_name='Característica', 
                                            value_name='Valor Promedio')

            # Crear un Bar Chart horizontal con eje de categoría múltiple
            fig = px.bar(df_multicat,
                        y='Barrio',  
                        x='Valor Promedio',
                        color='Característica',
                        barmode='group',
                        title='Características por Barrio',
                        labels={'Valor Promedio': 'Valor Promedio', 'Característica': 'Característica', 'Barrio': 'Barrio'},
                        color_discrete_sequence=px.colors.qualitative.Set1)

            fig.update_layout(yaxis_title='Barrio', xaxis_title='Valor Promedio', showlegend=True)
            st.plotly_chart(fig)




st.write("---")

#____________________________________________COLUMNAS BARRIOS__________________________________________________#
with st.container():
  st.write(f'<h3 style="text-align: center; color: #0b2d43;">Estadística por Barrio</h3>',
    unsafe_allow_html=True
)
col1, col2, col3, col4 = st.columns(4)

with col1:
    property_count = df_selected.shape[0] if 'df_selected' in locals() else 0
    st.markdown(f'''
                <div class="card-dos" style="max-width: 18rem, text-align: center;">
                    <div class="card-header">Total Propiedades</div>
                    <div class="card-body">
                    <h3 style="color: #dd0034;">{property_count:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

with col2:
    valor = df_selected['Valor'].mean() if not df_selected.empty else 0
    valor = round(valor)
    st.markdown(f'''
                <div class="card-dos" style="max-width: 18rem, text-align: center;">
                    <div class="card-header">Promedio Valor</div>
                    <div class="card-body">
                    <h3 style="color: #dd0034;">$ {valor:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
with col3:
    area = df_selected['Metros'].mean() if not df_selected.empty else 0
    area = round(area)
    st.markdown(f'''
                <div class="card-dos" style="max-width: 18rem, text-align: center;">
                    <div class="card-header">Promedio Metros</div>
                    <div class="card-body">
                    <h3 style="color: #dd0034;">{area:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        
with col4:
    valor_por_metro_cuadrado = (df_selected['Valor'] / df_selected['Metros']).mean() if not df_selected.empty else 0
    valor_por_metro_cuadrado = round(valor_por_metro_cuadrado, 2)
    st.markdown(f'''
                <div class="card-dos" style="max-width: 18rem, text-align: center;">
                    <div class="card-header">Valor Metro</div>
                    <div class="card-body">
                    <h3 style="color: #dd0034;">$ {valor_por_metro_cuadrado:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)


st.write("---")

#___________________________________________Indicadores Claves___________________________________________________#

with st.container():
  st.write(f'<h3 style="text-align: center; color: #0b2d43;">Indicadores Claves</h3>',
    unsafe_allow_html=True
)
  
# Ruta del archivo Excel
file_path = "data/general.xlsx"  
df2 = pd.read_excel(file_path)

# Sidebar - Selección de barrio
selected_barrio = st.sidebar.selectbox('Selecciona un barrio:', df2['Barrio'].unique())

# Filtrar el DataFrame por el barrio seleccionado
df_selected = df2[df2['Barrio'] == selected_barrio]


col = st.columns((0.3, 0.3, 0.1, 0.3, 0.1), gap='small')

with col[0]:
    total = df_selected['Total'].values[0] if not df_selected.empty else 0
    st.image("img/personas.png", caption= "Población", use_column_width = 'always')
    st.markdown(f'''
                <div class="card-dos" style="max-width: 10rem, text-align: center;">
                    <div class="card-body">
                    <h3 style="color: #dd0034;">{total:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

with col[1]:
    total_hombres = df_selected['Hombres'].values[0] if not df_selected.empty else 0
    st.image("img/hombre.png", caption= "Hombres", use_column_width = 'always')
    st.markdown(f'''
                <div class="card-dos" style="max-width: 18rem, text-align: center;">
                    <div class="card-body">
                    <h3 style="color: #dd0034;">{total_hombres:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

with col[2]:
    Pr_Infancia = df_selected['Primera_Infancia6'].values[0] if not df_selected.empty else 0
    Infancia = df_selected['Infancia4'].values[0] if not df_selected.empty else 0
    Adolescencia = df_selected['Adolescencia1'].values[0] if not df_selected.empty else 0
    Juventud= df_selected['Juventud5'].values[0] if not df_selected.empty else 0
    Adultez = df_selected['Adulto1'].values[0] if not df_selected.empty else 0
    Adulto_mayor = df_selected['Adulto_mayor3'].values[0] if not df_selected.empty else 0
    
    @st.dialog("Tipo de Población", width = "small")
    def mostrar_etapas():
        st.write(f"Pr. Infancia: {Pr_Infancia:,}")
        st.write(f"Infancia: {Infancia:,}")
        st.write(f"Adolescencia: {Adolescencia:,}")
        st.write(f"Juventud: {Juventud:,}")
        st.write(f"Adultez: {Adultez:,}")
        st.write(f"Adulto_mayor: {Adulto_mayor:,}")
        
    # Botón para mostrar el cuadro de diálogo
    if st.button("Tipo H"):
        mostrar_etapas()  # Llamada al cuadro de diálogo

with col[3]:
    total_mujeres = df_selected['Mujeres'].values[0] if not df_selected.empty else 0
    st.image("img/mujer.png", caption= "Mujeres", use_column_width = 'always')
    st.markdown(f'''
                <div class="card-dos" style="max-width: 18rem, text-align: center;">
                    <div class="card-body">
                    <h3 style="color: #dd0034;">{total_mujeres:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

with col[4]:
    Pr_Infancia2 = df_selected['Primera_Infancia2'].values[0] if not df_selected.empty else 0
    Infancia2 = df_selected['Infancia2'].values[0] if not df_selected.empty else 0
    Adolescencia2 = df_selected['Adolescencia2'].values[0] if not df_selected.empty else 0
    Juventud2 = df_selected['Juventud2'].values[0] if not df_selected.empty else 0
    Adultez2 = df_selected['Adulto2'].values[0] if not df_selected.empty else 0
    Adulto_mayor2 = df_selected['Adulto_mayor2'].values[0] if not df_selected.empty else 0
    
    @st.dialog("Tipo de Población", width = "small")
    def mostrar_etapas():
        st.write(f"Pr. Infancia: {Pr_Infancia2:,}")
        st.write(f"Infancia: {Infancia2:,}")
        st.write(f"Adolescencia: {Adolescencia2:,}")
        st.write(f"Juventud: {Juventud2:,}")
        st.write(f"Adultez: {Adultez2:,}")
        st.write(f"Adulto_mayor: {Adulto_mayor2:,}")
        
    # Botón para mostrar el cuadro de diálogo
    if st.button("Tipo M"):
        mostrar_etapas()  # Llamada al cuadro de diálogo

st.write("---")

