import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import leafmap.foliumap as leafmap
import requests



# Page configuration
st.set_page_config(
    page_title="Análisis",
    page_icon="👨‍🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Agregar el iframe del mapa interactivo en la aplicación de Streamlit
st.components.v1.iframe(
    src="https://mapas.bogota.gov.co/?&e=-74.11255834218471,4.561356531808731,-74.04389379140355,4.594424260547611,4686&b=7256&show_menu=true",
    width=1000,  # Ajustar el ancho a tu preferencia
    height=800  # Ajustar la altura a tu preferencia
)

# Otras partes de la aplicación
st.write("Mapa interactivo de Bogotá")


