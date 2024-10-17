import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import unidecode
import requests
import folium

# Configuración de la página
st.set_page_config(
    page_title="Análisis",
    page_icon="👨‍🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título de la aplicación
st.write(
    f'<h1 style="text-align: center; color: #dd0034;">Visor Interactivo: Locales Comerciales y Puntos de Interés</h1>',
    unsafe_allow_html=True
)
st.write("---")

# _____________________________________CONEXION BASE DE DATOS_________________________________________#
conn = st.connection("postgresql", type="sql")

# _____________________________________FUNCION CACHÉ_________________________________________#
@st.cache_data
def load_data(query):
    return conn.query(query)

# Carga de datos
df = load_data('SELECT * FROM locales')

# Limpiar caracteres en columnas de texto
def clean_text(value):
    return unidecode.unidecode(str(value))

# Aplica la limpieza a las columnas necesarias
df['Barrio'] = df['Barrio'].apply(clean_text)

# ______________________________________SIDEBAR______________________________________#
with st.sidebar:
    st.title('Filtros')

    if not df.empty:  # Verifica si df no está vacío
        # Lista de barrios únicos y filtrado por barrio seleccionado
        barrio_list = list(df['Barrio'].unique())[::-1]
        
        # Agregar el argumento key para que tenga un ID único
        selected_barrio = st.selectbox('Seleccionar Barrio', barrio_list, key="select_barrio")

        # Filtrar el DataFrame por el barrio seleccionado
        df_selected = df[df['Barrio'] == selected_barrio]
    else:
        st.warning("No hay datos disponibles para mostrar.")
        


# ______________________________________LIMPIAR COORDENADAS______________________________________#

def clean_coordinate(value):
    cleaned_value = value.replace('.', '')  # Eliminar todos los puntos
    if len(cleaned_value) > 2:
        cleaned_value = f"{cleaned_value[:-6]}.{cleaned_value[-6:]}"
    
    try:
        return float(cleaned_value)
    except ValueError:
        return None

def is_valid_coordinate(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Crear un nuevo DataFrame con coordenadas válidas
df_selected['Longitud'] = df_selected['Longitud'].apply(clean_coordinate)
df_selected['Latitud'] = df_selected['Latitud'].apply(clean_coordinate)

# Filtrar solo las filas con coordenadas válidas
df_selected = df_selected[
    df_selected['Longitud'].apply(is_valid_coordinate) & 
    df_selected['Latitud'].apply(is_valid_coordinate)
]

# ________________________________________________PUNTOS EN EL MAPA___________________________________________________#

m = leafmap.Map(center=[4.65, -74.08], zoom=12)

if not df_selected.empty:
    m.add_points_from_xy(
        df_selected,
        x="Longitud",
        y="Latitud",
        icon_names=["gear", "map", "leaf", "globe"],
        spin=True,
        add_legend=True
    )
else:
    st.warning("No hay puntos disponibles para el barrio seleccionado.")

# Manejo de excepciones al mostrar el mapa
try:
    # Configuración del mapa según las opciones
    map_option = st.selectbox(
        "Seleccione el tipo de mapa:",
        [
            "Roadmap vs Hybrid",
            "Esri World Topo Map vs OpenTopoMap",
            "NLCD 2001 vs NLCD 2016"
        ]
    )

    # Configuración del mapa según la opción seleccionada
    if map_option == "Roadmap vs Hybrid":
        m.split_map(left_layer="ROADMAP", right_layer="HYBRID")
    elif map_option == "Esri World Topo Map vs OpenTopoMap":
        m.split_map(left_layer="Esri.WorldTopoMap", right_layer="OpenTopoMap", zoom_control=False)
    elif map_option == "NLCD 2001 vs NLCD 2016":
        m.split_map(
            left_layer="NLCD 2001 CONUS Land Cover",
            right_layer="NLCD 2016 CONUS Land Cover",
            left_label="2001",
            right_label="2016",
            label_position="bottom",
            center=[36.1, -114.9],
            zoom=10,
        )

    # Mostrar el mapa en Streamlit
    m.to_streamlit(height=700)

except Exception as e:
    st.error(f"Error al mostrar el mapa: {e}")
# ________________________________________________INFORMACIÓN DE LOS PUNTOS___________________________________________________#

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

st.header('Información de los puntos')

if not df_selected.empty:
    for index, row in df_selected.iterrows():
        with st.expander(row['Barrio']):
            st.markdown(card_style, unsafe_allow_html=True)

            # Crear columnas para el diseño
            col1, col2, col3 = st.columns([1, 1.5, 1.5])

            # Columna 1: Imagen
            with col1:
                st.markdown(f'''
                <div class="card-dos" style="text-align: center; border: 1px solid #ccc; border-radius: 10px; padding: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <div class="card-header" style="background-color: #f8f9fa; border-bottom: 1px solid #ccc; border-radius: 10px 10px 0 0;">Imagen</div>
                    <div class="card-body">
                        <a href="{row['Imagen']}" target="_blank">
                            <img src="{row['Imagen']}" alt="Imagen" style="width: 100%; border-radius: 10px; height: auto;">
                        </a>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

            # Columna 2: Descripción y Metros
            with col2:
                st.markdown(f'''
                <div class="card-dos" style="text-align: center; border: 1px solid #ccc; border-radius: 10px; padding: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <div class="card-header" style="background-color: #f8f9fa; border-bottom: 1px solid #ccc; border-radius: 10px 10px 0 0;">Descripción</div>
                    <div class="card-body">
                        <h3 style="color: #dd0034; font-size: 14px;">{row['Descripción']}</h3>
                    </div>
                    <div class="card-header" style="background-color: #f8f9fa; border-bottom: 1px solid #ccc; border-radius: 10px 10px 0 0;">Metros</div>
                    <div class="card-body">
                        <h3 style="color: #dd0034; font-size: 14px; text-align: center">{row['Metros']} m²</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

            # Columna 3: Dirección y Baños
            with col3:
                st.markdown(f'''
                <div class="card-dos" style="text-align: center; border: 1px solid #ccc; border-radius: 10px; padding: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <div class="card-header" style="background-color: #f8f9fa; border-bottom: 1px solid #ccc; border-radius: 10px 10px 0 0;">Dirección</div>
                    <div class="card-body">
                        <h3 style="color: #dd0034; font-size: 14px;">{row['Ubicación']}</h3>
                    </div>
                    <div class="card-header" style="background-color: #f8f9fa; border-bottom: 1px solid #ccc; border-radius: 10px 10px 0 0;">Baños</div>
                        <div class="card-body">
                        <h3 style="color: #dd0034; font-size: 14px;">{row['Baños']}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
else:
    st.warning("No hay puntos disponibles para el barrio seleccionado.")


st.write("---")