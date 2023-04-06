import openai
import streamlit as st
from streamlit_chat import message
import pdfplumber
import io

# Create a left column in the Streamlit interface
left_column = st.sidebar

# Add a title and an input box for the OpenAI API key in the left column
left_column.title("Ask my PDF")
api_key = left_column.text_input("Enter your OpenAI API key:", type="password")
openai.api_key = api_key

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Set the model to GPT-4
model = "gpt-4-32k"

# Generate a response
def generate_response(prompt, text=None):
    if text:
        messages = [
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "user", "content": f"Text: {text}\nQuestion: {prompt}"}
        ]
    else:
        messages = [
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "user", "content": prompt}
        ]

    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})
    return response

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def handle_file_upload():
    if "answer" not in st.session_state:
        st.session_state["answer"] = {}
    
    st.title("Ask my PDF")
    
    file = st.file_uploader("Upload a PDF file (max 2 MB)", type=["pdf"], accept_multiple_files=False)
    if file is not None:
        if file.size <= 2 * 1024 * 1024:
            text = extract_text_from_pdf(io.BytesIO(file.read()))

            custom_question = st.text_input("Enter your question:")
            if st.button("Submit question"):
                answer = generate_response(custom_question, text)
                st.write(answer)

if __name__ == "__main__":
    handle_file_upload()
