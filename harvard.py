import os
import PyPDF2
import openai
import streamlit as st
import pandas as pd

st.title("Evaluador de ensayos argumentativos")

# Prompt the user for their API key
api_key = st.text_input("Ingrese su clave API de OpenAI:", value="", type="password")

# Set up the OpenAI API with the provided API key
openai.api_key = api_key

# Define a function to extract text from a PDF file
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def parse_evaluation(evaluation_text):
    try:
        evaluation_list = evaluation_text.split("\n")
        criteria = [item.split(":")[0] for item in evaluation_list[:-1]]
        scores = [round(float(item.split(":")[1].strip().split("/")[0])) for item in evaluation_list[:-1]]
        total = round(sum(scores) * (100 / (10 * len(scores))))
        return criteria, scores, total
    except IndexError:
        return None, None, None

# Define a function to evaluate the quality of the argumentation using GPT
def evaluar_argumentacion(texto):
    criterios_harvard = """
    Criterios de la Universidad de Harvard para evaluar la calidad de la argumentación:
    1. Claridad en la declaración del tema o pregunta.
    2. Uso de razones y evidencia apropiadas para respaldar las afirmaciones.
    3. Organización lógica y coherente.
    4. Consideración de puntos de vista alternativos y contraargumentos.
    5. Precisión y exactitud en el uso de términos y conceptos.
    6. Estilo y presentación adecuados, incluida la gramática, la ortografía y la puntuación.
    """

    prompt = f"Evaluar la calidad de la argumentación en el siguiente texto basándose en los criterios de la Universidad de Harvard. Proporcionar una calificación de 1 a 10 para cada criterio y una calificación total sobre 100:\n\n{criterios_harvard}\nTexto:\n{texto}\n\nEvaluación:"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    evaluacion = response.choices[0].text.strip()
    return evaluacion

# Define a function to handle the file upload and evaluation
def handle_file_upload():
    file = st.file_uploader("Suba un archivo PDF", type=["pdf"])
    if file is not None:
        text = extract_text_from_pdf(file)
        if st.button("Evaluar argumentación"):
            evaluacion = evaluar_argumentacion(text)
            criterios, calificaciones, total = parse_evaluation(evaluacion)

            if criterios is not None and calificaciones is not None and total is not None:
                data = {"Criterio": criterios,"Calificación": calificaciones}
                df = pd.DataFrame(data)
                df.loc[len(df.index)] = ["Total", total]

                st.table(df)
            else:
                st.error("Hubo un error al procesar las calificaciones. Por favor, intente de nuevo.")

# Define a main function to run the program
def main():
    handle_file_upload()

if __name__ == "__main__":
    main()
