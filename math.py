import streamlit as st
import io
import pdfplumber
import openai

left_column = st.sidebar

left_column.title("Evaluador de Problemas Matemáticos")
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
    st.title("Evaluación de problemas matemáticos con GPT-3")

    problem = st.text_input("Ingrese el problema matemático:")
    solution = st.text_input("Ingrese la solución propuesta:")

    if st.button("Calificar solución"):
        feedback = generate_feedback(problem, solution)
        st.write(feedback)

if __name__ == "__main__":
    handle_file_upload()
