import streamlit as st
import requests
from streamlit_lottie import st_lottie

# Configuracion de la etiqueta
st.set_page_config(
    page_title="RentSmart",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded")


st.logo("img/local.png",size="large")

# Función animación
def load_lottieurl(url):
  r = requests.get(url)
  if r.status_code != 200:
    return None
  return r.json()
#Segunda parte
lottie_coding3 = load_lottieurl("https://lottie.host/d8b13abd-07bb-4315-a969-b0420a41b1c5/xR87YNsrin.json")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&display=swap');

body {
  font-family: 'Raleway', sans-serif;   

}
</style>
""", unsafe_allow_html=True)

# Body
st_lottie(lottie_coding3, height=300, key="coding1")
    
st.write(
    f'<h1 style="text-align: center; color: #dd0034; font-size: 80px;">RentSmart</h1>',
    unsafe_allow_html=True
    )

st.write(
    f'<h1 style="text-align: center; color: #0b2d43; font-size: 40px;">Transforme los datos en decisiones</h1>',
    unsafe_allow_html=True
)

col = st.columns((1.5, 1.5, 1.5, 1.5, 1.5), gap='large')

with col[0]:
    st.image('img/logo.svg', width=100)  

with col[1]:
    st.image('img/banner2.jfif', width=70) 

with col[2]:

    st.image('img/logomano.png', width=70)  

with col[3]:

    st.image('img/hackathon.png', width=70)  
    
with col[4]:

    st.image('img/p4s.jfif', width=70) 

st.write(" ")
# Footer
with st.container():
  st.write(f'<h6 style="text-align: center; color: #0b2d43;">🌐2024</h6>',
    unsafe_allow_html=True
)
