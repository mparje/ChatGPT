import streamlit as st
import io
import pdfplumber
import openai

# Create a left column in the Streamlit interface
left_column = st.sidebar

# Add a title and an input box for the OpenAI API key in the left column
left_column.title("Argument Quality Evaluator")
api_key = left_column.text_input("Enter your OpenAI API key:", type="password")
openai.api_key = api_key

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def generate_answer(question, text):
    response = openai.Chat.Completion(
        engine="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "user", "content": f"Text: {text}\nQuestion: {question}"}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def handle_file_upload():
    if "answer" not in st.session_state:
        st.session_state["answer"] = {}
    
    st.title("PDF Analysis with GPT-3.5-turbo")
    
    file = st.file_uploader("Upload a PDF file (max 2 MB)", type=["pdf"], accept_multiple_files=False)
    if file is not None:
        if file.size <= 2 * 1024 * 1024:
            text = extract_text_from_pdf(io.BytesIO(file.read()))

            custom_question = st.text_input("Enter your question:")
            if st.button("Submit question"):
                answer = generate_answer(custom_question, text)
                st.write(answer)

if __name__ == "__main__":
    handle_file_upload()
