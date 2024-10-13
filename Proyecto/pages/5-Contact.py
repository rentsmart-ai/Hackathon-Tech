
import streamlit as st
import requests
from streamlit_lottie import st_lottie

from forms.contact import contact_form

# Page configuration
st.set_page_config(
    page_title="Contact",
    page_icon="📫",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()


# Header
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./img/vida.png", width=230)
with col2:
    st.title("Victor Guzmán-Brand", anchor=False)
    st.write(
        "Profesional en psicología. Ingeniería de Sistemas. Esp. en Analítica de datos. Esp. Desarrollo Integral de la Infancia y Adolescencia."
    )
    if st.button("👨🏽‍🔬Contact Me"):
        show_contact_form()
        
# experiencia
st.write("\n")
st.subheader("Experiencia & Practica", anchor=False)
st.write(
    """
    - Asesor e investigador en proyectos académicos en educación, administración e inteligencia artificial.
    - Experiencia en Analitica de datos y trabajo social.
    - Ponente en varios congresos internacionales.
    """
)
#---SKILLS---
st.write("\n")
st.subheader("Habilidades", anchor=False)
st.write(
    """
    - Desarrollador: Python, Java, SQL, HTML, CSS, JavaScript.
    - Visualización de Datos: Power BI, Plotly, Tableau.
    - Machine Learning: Redes Neuronales, XGBoost, decision tree, random forest, clustering, series de tiempo.
    - PLataformas: Microsoft Azure ML, Colab, Weka, Knime.
    - Base de Datos: PostgreSQL, MongoDB, MySQL.
    """
)
st.write("\n")
st.subheader("Redes Sociales de Investigación", anchor=False)
st.write(
    """
    - https://scholar.google.com/citations?user=a27XGQcAAAAJ&hl=es
    - https://www.researchgate.net/
    - https://orcid.org/0000-0002-6051-3153
    - htps://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001799523
    - Email: victor.alfonso.guzman.brand@gmail.com
    """
)
#FOOTER
with st.container():
    st.markdown("""
        <div style="text-align: center;">
            <h3>© Deep Psychology</h3>
            <h5>2024</h5>
        </div>
    """, unsafe_allow_html=True)
  
