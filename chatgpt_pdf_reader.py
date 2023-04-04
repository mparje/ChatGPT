import PyPDF2
import openai
import streamlit as st

# Solicitar al usuario su clave de API
st.title("Generador de respuestas con ChatGPT")
api_key = st.text_input("Ingresa tu clave de API de OpenAI:", type="password")

# Configurar la API de OpenAI con la clave de API proporcionada
openai.api_key = api_key

# Definir una función para extraer texto de un archivo PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Definir una función para generar respuestas a preguntas de usuario utilizando la API de ChatGPT
def generate_answer(question, text):
    max_context_length = 4096 - len(question) - 30
    truncated_text = text[:max_context_length]

    prompt = f"{truncated_text}\n\nQuestion: {question}\nAnswer:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    return answer

# Definir una función para manejar la carga de archivos y la generación de respuestas
def handle_file_upload():
    file = st.file_uploader("Sube un archivo PDF", type=["pdf"])
    if file is not None:
        text = extract_text_from_pdf(file)
        question = st.text_input("Ingresa una pregunta:")
        if st.button("Enviar"):
            answer = generate_answer(question, text)
            st.write(answer)

# Definir una función principal para ejecutar el programa
def main():
    handle_file_upload()

if __name__ == "__main__":
    main()
