import openai
import streamlit as st
import time

# Debe ser el primer comando de Streamlit
st.set_page_config(page_title="Assistant", page_icon=":speech_balloon:")

openai.api_key = st.secrets["general"]["OPENAI_API_KEY"]
assistant_id = "asst_vK4aY2e2YMCBm9dbqRjNnLAk"

client = openai

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.write(
    f'<h1 style="text-align: center; color: #50C4ED;">¡Bienvenid@ al Asistente de Primeros Auxilios Psicológicos!</h1>',
    unsafe_allow_html=True
    )
st.write("---")
with st.container():
    st.markdown("""
        <div style="text-align: center;">
            <p color="50C4ED">Queremos recordarte que estamos aquí para proporcionarte apoyo y orientación en momentos difíciles. Los primeros auxilios psicológicos son herramientas útiles para manejar situaciones de crisis o estrés, pero es importante tener en cuenta que no sustituyen la ayuda profesional de un terapeuta o psicólogo.
                            Recuerda que cada persona es única y puede experimentar situaciones de manera diferente. Algunos mensajes pueden estar sesgados o no aplicar a tu situación específica. Siempre es recomendable buscar la orientación de un profesional en salud mental para recibir el apoyo adecuado y personalizado.
                            Estamos aquí para acompañarte en tu camino hacia el bienestar, ¡No dudes en contactarnos si necesitas ayuda!"</p>
        </div>
    """, unsafe_allow_html=True)
st.write("---")


left_column, right_column = st.columns([4, 1])

with left_column:
    if st.button("Start Chat"):
        st.session_state.start_chat = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id


if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("¿Cómo te has estado sintiendo últimamente?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="Ten en cuenta el documento anexo, se concreto y las respuestas que generes no superen las 200 palabras. Siempre responde de forma amable y respetuosa: Hola, soy un chatbot especializado en atención de primeros auxilios psicológicos. Si estás aquí, es probable que estés buscando información sobre la conducta suicida. Estoy aquí para ayudarte a comprender mejor este tema y brindarte el apoyo necesario. ¿En qué puedo asistirte hoy?"

        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

with right_column:
    if st.button("Exit Chat"):
        st.session_state.messages = []  
        st.session_state.start_chat = False 
        st.session_state.thread_id = None


#FOOTER
with st.container():
    st.markdown("""
        <div style="text-align: center;">
            <h3>© Deep Psychology</h3>
            <h5>2024</h5>
        </div>
    """, unsafe_allow_html=True)


