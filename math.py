import streamlit as st
import io
import pdfplumber
import openai

# Crear una columna izquierda en la interfaz de Streamlit
left_column = st.sidebar

# Añadir un título y una casilla de entrada para la clave API de OpenAI en la columna izquierda
left_column.title("Evaluador de Problemas de Matemáticas")
api_key = left_column.text_input("Ingrese su clave API de OpenAI:", type="password")
openai.api_key = api_key


def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def generate_feedback(problem, solution):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Problema: {problem}\nSolución propuesta: {solution}\nRetroalimentación:",
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

def handle_file_upload():
    problem = st.text_input("Ingrese el problema matemático:")

    uploaded_file = st.file_uploader("Sube un archivo PDF con la solución propuesta (máximo 2 MB)", type=["pdf"])
    if uploaded_file is not None:
        if uploaded_file.size <= 2 * 1024 * 1024:
            solution = extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
            if st.button("Calificar solución"):
                feedback = generate_feedback(problem, solution)
                st.write(feedback)
        else:
            st.error("El archivo supera el límite de tamaño permitido de 2 MB. Por favor, sube un archivo más pequeño.")

if __name__ == "__main__":
    handle_file_upload()
