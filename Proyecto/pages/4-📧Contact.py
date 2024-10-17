
import streamlit as st
import requests


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
    st.image("./img/logomano.png", width=230)
with col2:
    st.title("¿Quiénes Somos?", anchor=False)
    st.write(
        
"Somos un equipo comprometido con el aprendizaje y la innovación, pertenecientes al BootCampBootcamp Talento Tech en los cursos de desarrollo web e inteligencia artificial. Nuestro objetivo es mostrar las habilidades clave aprendidas que permitan destacar en un entorno tecnológico en constante evolución."
    )
    if st.button("👨🏽‍🔬Contact Me"):
        show_contact_form()
        


st.write("_____")
# Footer
with st.container():
  st.write(f'<h6 style="text-align: center; color: #0b2d43;">🌐2024</h6>',
    unsafe_allow_html=True
)

