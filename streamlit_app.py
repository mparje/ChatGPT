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
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Text: {text}\nQuestion: {question}\nAnswer:",
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

def handle_file_upload():
    if "answer" not in st.session_state:
        st.session_state["answer"] = {}
    
    st.title("PDF Analysis with GPT-3")
    
    file = st.file_uploader("Upload a PDF file (max 2 MB)", type=["pdf"], accept_multiple_files=False)
    if file is not None:
        if file.size <= 2 * 1024 * 1024:
            text = extract_text_from_pdf(io.BytesIO(file.read()))
            st.write("Suggested questions:")

            suggested_questions = [
                "What is the author's thesis?",
                "On what grounds does the author defend their thesis?",
                "What objections to their thesis does the author consider?",
                "How does the author respond to the objections presented?",
                "What consequences arising from the acceptance of their thesis does the author discuss?",
            ]

            for question in suggested_questions:
                if st.button(question):
                    if question not in st.session_state.answer:
                        st.session_state.answer[question] = generate_answer(question, text)

                    st.write(st.session_state.answer[question])

            custom_question = st.text_input("Or enter your own question:")
            if st.button("Submit custom question"):
                answer = generate_answer(custom_question, text)
                st.write(answer)

if __name__ == "__main__":
    handle_file_upload()
