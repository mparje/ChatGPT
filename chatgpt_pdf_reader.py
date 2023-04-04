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
    file = st.file_uploader("Sube un archivo PDF (máximo 2 MB)", type=["pdf"], accept_multiple_files=False)
    if file is not None:
        if file.size <= 2 * 1024 * 1024:
            text = extract_text_from_pdf(file)
            st.write("Preguntas sugeridas:")
            suggested_questions = [
                "¿Cuál es la tesis del autor?",
                "¿En qué razones se basa el autor para defender su tesis?",
                "¿Qué objeciones a su tesis toma en cuenta el autor?",
                "¿Cómo replica el autor a las objeciones presentadas?",
                "¿Qué consecuencias derivadas de la aceptación de su tesis plantea el autor?",
            ]

            total_score = 0
            question_count = 0

            for question in suggested_questions:
                if st.button(question):
                    answer = generate_answer(question, text)
                    st.write(answer)
                    rating = st.selectbox(f"Califica la respuesta del 1 al 5 para la pregunta '{question}':", [1, 2, 3, 4, 5])
                    total_score += rating
                    question_count += 1
                    st.write(f"Has calificado la respuesta con un {rating}.")

            custom_question = st.text_input("O ingresa tu propia pregunta:")
            if st.button("Enviar pregunta personalizada"):
                answer = generate_answer(custom_question, text)
                st.write(answer)
                rating = st.selectbox("Califica la respuesta del 1 al 5:", [1, 2, 3, 4, 5])
                total_score += rating
                question_count += 1
                st.write(f"Has calificado la respuesta con un {rating}.")

            if st.button("Mostrar puntuación total"):
                if question_count > 0:
                                        total_score_percentage = (total_score / (question_count * 5)) * 100
                    st.write(f"Tu puntuación total es {total_score} de {question_count * 5} puntos, lo que equivale a {total_score_percentage:.2f}%.")
                else:
                    st.write("No has calificado ninguna respuesta. Por favor, haz algunas preguntas y califica las respuestas para ver la puntuación total.")
        else:
            st.error("El archivo supera el límite de tamaño permitido de 2 MB. Por favor, sube un archivo más pequeño.")

# Definir una función principal para ejecutar el programa
def main():
    handle_file_upload()

if __name__ == "__main__":
    main()
