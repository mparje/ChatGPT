import openai
import streamlit as st
import pdfplumber
import io
from docx import Document

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def generate_response(prompt, text=None):
    messages = [
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
    ]
    if text:
        messages.append({"role": "user", "content": f"Text: {text}\nQuestion: {prompt}"})
    else:
        messages.append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    response = completion.choices[0].message.content
    return response.strip()

def handle_file_upload(api_key):
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
        return

    openai.api_key = api_key

    st.title("Ask my Documents")

    left_column = st.sidebar
    left_column.title("Instructions")
    left_column.write("This tool allows you to ask questions about the contents of your PDF or DOCX documents. Upload a document with a maximum of 4000 words or approximately 8 pages. Documents are removed from the server after 10 minutes of inactivity.")

    file = st.file_uploader("Upload a PDF or DOCX file (max 2 MB)", type=["pdf", "docx"], accept_multiple_files=False)
    if file is not None:
        if file.size <= 2 * 1024 * 1024:
            if file.type == "application/pdf":
                text = extract_text_from_pdf(io.BytesIO(file.read()))
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = extract_text_from_docx(io.BytesIO(file.read()))

            custom_question = st.text_input("Enter your question:")
            if st.button("Submit question"):
                answer = generate_response(custom_question, text)
                st.write(answer)

if __name__ == "__main__":
    api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
    handle_file_upload(api_key)
