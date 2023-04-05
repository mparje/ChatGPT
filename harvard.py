import openai
import streamlit as st

# Prompt the user for their API key
api_key = st.text_input("Enter your OpenAI API key:")

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

# Define a function to generate answers to user questions using the ChatGPT API
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

# Define a function to handle the file upload and answer generation
def handle_file_upload():
    file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if file is not None:
        text = extract_text_from_pdf(file)
        #answered = True  # Set to True initially to prevent first question box from showing 
        question = st.text_input("Enter a question:")
        if st.button("Submit"):
            answer = generate_answer(question, text)
            st.write(answer)

# Define a main function to run the program
def main():
    handle_file_upload()

if __name__ == "__main__":
    main()
