import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Análisis",
    page_icon="👨‍🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.write(
    f'<h1 style="text-align: center; color: #dd0034;">Visor Interactivo: Locales Comerciales y Puntos de Interés</h1>',
    unsafe_allow_html=True
)
st.write("---")

#_____________________________________CONEXION BASE DE DATOS_________________________________________#
conn = st.connection("postgresql", type="sql")

#_____________________________________FUNCION CACHÉ_________________________________________#
@st.cache_data
def load_data(query):
    return conn.query(query)

# Carga de datos
df = load_data('SELECT * FROM locales')

# Limpiar caracteres en columnas de texto
def clean_text(value):
    try:
        return str(value).encode('utf-8', 'replace').decode('utf-8')
    except Exception:
        return ""

# Aplica la limpieza a las columnas necesarias
df['Barrio'] = df['Barrio'].apply(clean_text)

#______________________________________SIDEBAR______________________________________#
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

#______________________________________LIMPIAR COORDENADAS______________________________________#

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

#______________________________________________PUNTOS EN EL MAPA___________________________________________________#
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
    m.to_streamlit(height=700)
except Exception as e:
    st.error(f"Error al mostrar el mapa: {e}")

