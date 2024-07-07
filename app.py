import streamlit as st
from chatbot.chatbot import Chatbot
from chatbot.embeddings import get_db
import os
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_KEY

# List of available codebases
available_codebases = ["API-Project", "Chat-Help-Center-main"]

# Set up the Streamlit app
st.title("Arcane CodeAI")
st.write("Ask questions about your codebase and get answers from the AI.")

# Dropdown for selecting the codebase
selected_codebase = st.selectbox("Select Codebase", available_codebases)

# Button to create or load embeddings for the selected codebase
if st.button("Create/Load Embeddings"):
    try:
        # Create or load the embeddings database
        db = get_db(selected_codebase, create_new=True)
        st.success(f"Embeddings for {selected_codebase} created/loaded successfully!")
    except Exception as e:
        st.error(f"Error creating/loading embeddings: {e}")

# Text input for the question
question = st.text_input("Enter your question here:")

# Button to submit the question
if st.button("Get Answer"):
    if question and selected_codebase:
        try:
            # Initialize the chatbot with the selected codebase
            chatbot = Chatbot(selected_codebase)
            response = chatbot.get_response(question)
            
            st.write("### Answer")
            st.write(response['answer'])
            
            st.write("### Related Documents")
            related_docs = response['related_docs'].split('\n')
            for doc in related_docs:
                # Create a link to open the file
                file_path = os.path.join(os.path.expanduser('~'), doc)
                encoded_path = base64.b64encode(file_path.encode()).decode()
                href = f'- <a href="file:///{encoded_path}" target="_blank">{doc}</a>'
                st.markdown(href, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question and select a codebase.")

# To run the Streamlit app, use the following command in your terminal:
# streamlit run app.py
