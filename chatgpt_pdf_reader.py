import streamlit as st
import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    text = ""
    for page_num in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page_num).extractText()
    return text

def generate_answer(question, text):
    return f"Esta es una respuesta de ejemplo para la pregunta '{question}'."

def handle_file_upload():
    if "answer" not in st.session_state:
        st.session_state["answer"] = {}

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
