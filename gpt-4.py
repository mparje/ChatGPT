import openai
import streamlit as st
from streamlit_chat import message
import pdfplumber
import io

# Setting page title and header
st.set_page_config(page_title="Ask my PDF", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Ask my PDF</h1>", unsafe_allow_html=True)

# Create a left column in the Streamlit interface
left_column = st.sidebar

# Add a title and an input box for the OpenAI API key in the left column
left_column.title("Argument Quality Evaluator")
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
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.title("Sidebar")
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"
else:
    model = "gpt-4"

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

# generate a response
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
    messages=st.session_state['messages']
)
response = completion.choices[0].message.content
st.session_state['messages'].append({"role": "assistant", "content": response})

total_tokens = completion.usage.total_tokens
prompt_tokens = completion.usage.prompt_tokens
completion_tokens = completion.usage.completion_tokens
return response, total_tokens, prompt_tokens, completion_tokens

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
                answer, total_tokens, prompt_tokens, completion_tokens = generate_response(custom_question, text)
                st.write(answer)

if __name__ == "__main__":
    handle_file_upload()
