import os
import streamlit as st
from langchain.chains import RetrievalQA
from bs4 import BeautifulSoup
from langchain.prompts.chat import (ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
import requests
from twocaptcha import TwoCaptcha

# Define the system template for answering questions
system_template = """Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer."""

# Create message templates for system and human messages
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]

# Create a chat prompt template from the messages
prompt = ChatPromptTemplate.from_messages(messages)

def bypass_captcha(site_key, url, api_key):
    solver = TwoCaptcha(api_key)
    result = solver.recaptcha(sitekey=site_key, url=url)
    return result['code']

def main():
    # Set up the Streamlit app interface
    st.title('🦜🔗 Chat With Website')
    st.subheader('Input your website URL, ask questions, and receive answers directly from the website.')
    google_api_key = st.text_input("Enter the Google API key", type='password')
    anticaptcha_api_key = st.text_input("Enter the 2Captcha API key", type='password')
    url = st.text_input("Insert The website URL")
    user_question = st.text_input("Ask a question (query/prompt)")

    if st.button("Submit Query", type="primary"):
        ABS_PATH = os.path.dirname(os.path.abspath(__file__))
        DB_DIR = os.path.join(ABS_PATH, "db")
        
        os.environ['GOOGLE_API_KEY'] = google_api_key  # Set the Google API key
        
        # Load HTML content from the URL
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Check if there is a CAPTCHA
        captcha_div = soup.find('div', {'class': 'g-recaptcha'})
        if captcha_div:
            captcha_site_key = captcha_div['data-sitekey']
            captcha_response = bypass_captcha(captcha_site_key, url, anticaptcha_api_key)
            r = requests.post(url, data={'g-recaptcha-response': captcha_response})
            soup = BeautifulSoup(r.content, 'html.parser')
        
        # Extract text from the HTML content
        text = soup.get_text(separator='\n')
        
        # Split the text data into chunks
        text_splitter = CharacterTextSplitter(separator='\n', chunk_size=512, chunk_overlap=100)
        docs = text_splitter.split_text(text)

        # Create Google Generative AI embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Create a Chroma vector database from the text documents
        vectordb = Chroma.from_texts(texts=docs, embedding=embeddings, persist_directory=DB_DIR)
        vectordb.persist()

        # Create a retriever from the Chroma vector database
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})

        # Use a ChatGroq model for question-answering
        llm = ChatGroq(model="llama3-70b-8192", groq_api_key="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")

        # Create a RetrievalQA instance from the model and retriever
        chain = ConversationalRetrievalChain.from_llm(
            llm,
            retriever=retriever,
            return_source_documents=True,
            chain_type="stuff",
            verbose=True,
        )
        chat_history = []

        # Run the prompt and return the response
        response = chain({"question": user_question, "chat_history": chat_history})

        # Extract and display the result
        if 'answer' in response:
            st.write(response['answer'])
        else:
            st.write("Answer not found.")

if __name__ == '__main__':
    main()