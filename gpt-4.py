import openai
import streamlit as st
import io
import pdfplumber
import docx

# Create a left column in the Streamlit interface
left_column = st.sidebar

# Add a title and an input box for the OpenAI API key in the left column
left_column.title("Ask my Documents")
api_key = left_column.text_input("Enter your OpenAI API key:", type="password")
openai.api_key = api_key

# Add a description and instructions in the left column
left_column.subheader("Description")
left_column.write("This tool allows you to upload a PDF or DOCX file and ask questions related to the document's content. The AI assistant will generate a response based on the information in the document.")

left_column.subheader("Instructions")
left_column.write("""
1. Upload a PDF or DOCX file (max 2 MB).
2. Make sure the document is no more than 4000 words or approximately 8 pages.
3. Type your question related to the document in the text box.
4. Click the 'Submit question' button to get a response.
5. Documents will be deleted from the server after 10 minutes of inactivity.
""")

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
model = "gpt-4"

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

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def handle_file_upload():
    if "answer" not in st.session_state:
        st.session_state["answer"] = {}
    
    st.title("Ask my Documents")
    
    file = st.file_uploader("Upload a PDF or DOCX file (max 2 MB)", type=["pdf", "docx"], accept_multiple_files=False)
    if file is not None:
        if file.size <= 2 * 1024 * 1024:
            if file.type == "application/pdf":
                text = extract_text_from_pdf(io.BytesIO(file.read()))
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document text = extract_text_from_docx(io.BytesIO(file.read()))

            custom_question = st.text_input("Enter your question:")
            if st.button("Submit question"):
                answer = generate_response(custom_question, text)
                st.write(answer)

if __name__ == "__main__":
    handle_file_upload()
