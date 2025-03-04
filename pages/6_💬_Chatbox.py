import streamlit as st
import os
import signal
import requests
import psutil
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

st.set_page_config(page_title="LLM Chatbox", page_icon="💬")

# Model name
model_name = "deepseek-r1-abliterated:14b"

# Prevent auto-start of Ollama
embeddings = None
vector_store = None
model = None

template = """
You are an AI assistant. Your task is to provide a detailed answer to the question based on the given context. Use complete sentences and avoid repetition.
Context: {context}
Question: {question}
"""

def check_ollama_process():
    """Check if Ollama process is running."""
    for proc in psutil.process_iter(['name']):
        if 'ollama' in proc.info['name'].lower():
            return True
    return False

def check_ollama_status():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def check_model_availability(model_name):
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(model["name"] == model_name for model in models)
    except requests.RequestException:
        return False
    return False

# Display an alert if no Ollama process is running
if not check_ollama_process():
    st.warning("No Ollama process detected! Please start Ollama before using this page.")

class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}

def upload_file(file):
    with open(file.name, "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    return [Document(doc.page_content, doc.metadata) for doc in documents]

def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return [Document(f.read(), {"source": file_path})]

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    return text_splitter.split_documents(documents)

def index_docs(documents):
    vector_store.add_documents(documents)

def retrieve_docs(query):
    return vector_store.similarity_search(query)

def answer_question(question, context, documents):
    context_text = "\n\n".join([doc.page_content for doc in documents])
    combined_context = f"{context}\n\n{context_text}"
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": combined_context})

uploaded_file = st.sidebar.file_uploader("Upload File", type=["pdf", "txt"], accept_multiple_files=False)
context = st.session_state.get("context", "")
user_context = st.sidebar.text_area("Enter context:")

if "history" not in st.session_state:
    st.session_state.history = []

if uploaded_file:
    if not check_ollama_status():
        st.error("Ollama service is not running. Please start Ollama and reload the app.")
        if st.sidebar.button("Exit"):
            exit_script()
        st.stop()

    if not check_model_availability(model_name):
        st.error(f"Model '{model_name}' is not available. Please download or load the model correctly.")
        if st.sidebar.button("Exit"):
            exit_script()
        st.stop()

    # Initialize Ollama components only when needed
    embeddings = OllamaEmbeddings(model=model_name)
    vector_store = InMemoryVectorStore(embeddings)
    model = OllamaLLM(model=model_name, temperature=0.8)

    upload_file(uploaded_file)
    file_path = uploaded_file.name
    if uploaded_file.type == "application/pdf":
        documents = load_pdf(file_path)
    elif uploaded_file.type == "text/plain":
        documents = load_txt(file_path)
    
    chunked_documents = split_text(documents)
    index_docs(chunked_documents)
    
    question = st.chat_input()
    if question:
        st.chat_message("user").write(question)
        related_documents = retrieve_docs(question)
        answer = answer_question(question, user_context, related_documents)
        st.session_state["context"] = f"{context}\n\n{answer}"
        st.chat_message("assistant").write(answer)
        st.session_state.history.append((question, answer))

# Display chat history
for q, a in st.session_state.history:
    st.chat_message("user").write(q)
    st.chat_message("assistant").write(a)