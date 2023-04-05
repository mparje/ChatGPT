import streamlit as st
import io
import pdfplumber
import openai

# Crear una columna izquierda en la interfaz de Streamlit
left_column = st.sidebar

# Añadir un título y una casilla de entrada para la clave API de OpenAI en la columna izquierda
left_column.title("Evaluador de Calidad Argumentativa")
api_key = left_column.text_input("Ingrese su clave API de OpenAI:", type="password")
openai.api_key = api_key

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def generate_answer(question, text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Texto: {text}\nPregunta: {question}\nRespuesta:",
        temperature=0.5,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

def handle_file_upload():
    if "answer" not in st.session_state:
        st.session_state["answer"] = {}
    
    st.title("Análisis de PDF con GPT-3")
    
    file = st.file_uploader("Sube un archivo PDF (máximo 2 MB)", type=["pdf"], accept_multiple_files=False)
    if file is not None:
        if file.size <= 2 * 1024 * 1024:
            text = extract_text_from_pdf(io.BytesIO(file.read()))
            st.write("Preguntas sugeridas:")

            suggested_questions = [
                "¿Cuál es la tesis del autor?",
                "¿En qué razones se basa el autor para defender su tesis?",
                "¿Qué objeciones a su tesis toma en cuenta el autor?",
                "¿Cómo replica el autor a las objeciones presentadas?",
                "¿Qué consecuencias derivadas de la aceptación de su tesis plantea el autor?",
            ]

            for question in suggested_questions:
                if st.button(question):
                    if question not in st.session_state.answer:
                        st.session_state.answer[question] = generate_answer(question, text)

                    st.write(st.session_state.answer[question])

            custom_question = st.text_input("O ingresa tu propia pregunta:")
            if st.button("Enviar pregunta personalizada"):
                answer = generate_answer(custom_question, text)
                st.write(answer)

if __name__ == "__main__":
    handle_file_upload()
