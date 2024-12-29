from openai import OpenAI
import streamlit as st
from event_handler import StreamlitAssistantEventHandler
# Constants
height = 600
title = "🏗️ Asistente de Proyectos"
icon = ":robot:"

# Set page title and icon
st.set_page_config(page_title=title, page_icon=icon)

def toggle_clicked():
    if st.session_state.clicked is True:
        st.session_state.clicked = False
    else:
        st.session_state.clicked = True

if "messages" not in st.session_state:
    st.session_state.messages = []

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

# Create the OpenAI assistant
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
instructions = (
    "Eres un experto asistiendo proyectos de arquitectura. "
    "Usa tu base de conocimiento para responder preguntas "
    "sobre las especificaciones técnicas de un proyecto de arquitectura."
)
assistant = client.beta.assistants.create(
    name="Asistente de proyectos de arquitectura",
    instructions=instructions,
    model="gpt-4o-mini-2024-07-18",
    tools=[{"type": "file_search"}],
)

# Create vector store
vector_store = client.beta.vector_stores.create(name="Especificaciones Técnicas de Construcción")

col1, col2 = st.columns([4, 1], gap="large", vertical_alignment="bottom" )
with col1:
    st.header(title)
with col2:
    if st.session_state.clicked is True:
        st.button("Cerrar", on_click=toggle_clicked)
    else:
        st.button("Cargar EETT", on_click=toggle_clicked)

if st.session_state.clicked:
    uploaded_file = st.file_uploader(
        "Carga las especificaciones técnicas de construcción",
        type=["pdf"],
    )
    if uploaded_file:
        # First upload the file to OpenAI
        file_obj = client.files.create(
            file=uploaded_file,
            purpose="assistants"
        )
        file = client.beta.vector_stores.files.create_and_poll(
            vector_store_id=vector_store.id,
            file_id=file_obj.id
        )
        st.success(f"Archivo cargado: {file.id}")
        # Update the assistant with the new vector store
        assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("¿Qué vamos a construir hoy?"):
    # Add user message to UI and state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create thread
    thread = client.beta.threads.create(
        messages=[{ "role": "user", "content": prompt }],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store.id]
            }
        }
    )

    # Create assistant response container
    with st.chat_message("assistant"):
        try:
            # Create and stream the run
            with client.beta.threads.runs.stream(
                thread_id=thread.id,
                assistant_id=assistant.id,
                event_handler=StreamlitAssistantEventHandler(st.container())
            ) as stream:
                response = stream.get_final_messages()[0].content[0].text.value
                
            # Add assistant response to session state
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
