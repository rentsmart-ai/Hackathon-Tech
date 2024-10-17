import streamlit as st
import pandas as pd
import unidecode
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="Análisis",
    page_icon="👨‍🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.write(
    f'<h1 style="text-align: center; color: #dd0034;">Interfaz Interactiva para la Exploración de Arrendamiento Comercial y Puntos de Interés en Bogotá</h1>',
    unsafe_allow_html=True
)
st.write("---")


# Agregar el iframe del mapa interactivo en la aplicación de Streamlit
st.components.v1.iframe(
    src="https://mapas.bogota.gov.co/?&e=-74.11255834218471,4.561356531808731,-74.04389379140355,4.594424260547611,4686&b=7256&show_menu=true",
    width=1200,  # Ajustar el ancho a tu preferencia
    height=800  # Ajustar la altura a tu preferencia
)