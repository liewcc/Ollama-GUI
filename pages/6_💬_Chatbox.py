import streamlit as st
import os
import requests
import psutil
import subprocess
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

st.set_page_config(page_title="LLM Chatbox", page_icon="\U0001F4AC")

# Directory & Configurations
CONFIG_FILE = "Ollama_Config.txt"
UPLOAD_PREFIX = "[upload path]"
UPLOAD_DIR = "uploaded_files"

# Template text for the context box
DEFAULT_TEMPLATE = """You are an AI assistant. Your task is to provide a detailed answer to the question based on the given context. Use complete sentences and avoid repetition.
Context: {context}
Question: {question}"""

# Define the function to get the current Ollama model name
def get_ollama_model_name():
    try:
        result = subprocess.run(["ollama", "ps"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        return lines[1].split()[0] if len(lines) > 1 else None
    except subprocess.CalledProcessError:
        return None

# Ensure model_name is updated every time
model_name = get_ollama_model_name()
if not model_name:
    st.error("No active Ollama model detected! Please start Ollama and ensure a model is running.")
    st.stop()

st.session_state.model_name = model_name
st.session_state.embeddings = OllamaEmbeddings(model=model_name)
st.session_state.vector_store = InMemoryVectorStore(st.session_state.embeddings)
st.session_state.model = OllamaLLM(model=model_name, temperature=0.8)

def check_ollama_process():
    return any('ollama' in proc.info['name'].lower() for proc in psutil.process_iter(['name']))

def check_ollama_status():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def save_uploaded_file_path(file_path):
    with open(CONFIG_FILE, "w") as f:
        f.write(f"{UPLOAD_PREFIX}{file_path}")

def load_last_uploaded_file():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            content = f.read().strip()
            return content[len(UPLOAD_PREFIX):].split("\n")[0] if content.startswith(UPLOAD_PREFIX) else None
    return None

def upload_file(file):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path

def load_document(file_path):
    if file_path.endswith(".pdf"):
        return [Document(doc.page_content, {"source": file_path}) for doc in PDFPlumberLoader(file_path).load()]
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return [Document(f.read(), {"source": file_path})]
    return []

def split_text(documents):
    return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True).split_documents(documents)

def index_docs(documents):
    if documents:
        st.session_state.vector_store.add_documents(documents)
        st.session_state.indexed_documents = documents
        st.session_state.indexing_complete = True
        #st.sidebar.success(f"Indexed {len(documents)} documents successfully.")
    else:
        st.sidebar.error("No documents to index.")

def retrieve_docs(query):
    if "vector_store" not in st.session_state or st.session_state.vector_store is None:
        st.warning("No documents are indexed yet! Please upload and process a file first.")
        return []
    return st.session_state.vector_store.similarity_search(query)

def answer_question(question, context, documents):
    template = """
    You are an AI assistant. Your task is to provide a detailed answer to the question based on the given context. Use complete sentences and avoid repetition.
    Context: {context}
    Question: {question}
    """
    combined_context = "\n\n".join([doc.page_content for doc in documents])
    chain = ChatPromptTemplate.from_template(template) | st.session_state.model
    response = chain.invoke({"question": question, "context": combined_context})
    #return f"**Model Used:** {st.session_state.model_name}\n\n**File Processed:** {st.session_state.uploaded_file_path}\n\n{response}"
    file_name = os.path.basename(st.session_state.uploaded_file_path)  # Extract file name only
    return f"**Model Used:** {st.session_state.model_name}\n\n**File Processed:** {file_name}\n\n{response}"


class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content or ""
        self.metadata = metadata or {}

if "history" not in st.session_state:
    st.session_state.history = []
if "context" not in st.session_state:
    st.session_state.context = DEFAULT_TEMPLATE

# Upload File Handling
last_uploaded_file = load_last_uploaded_file()
uploaded_file = st.sidebar.file_uploader("Upload File", type=["pdf", "txt"], accept_multiple_files=False)

if uploaded_file:
    file_path = upload_file(uploaded_file)
    save_uploaded_file_path(file_path)
    st.session_state.uploaded_file_path = file_path
    st.sidebar.success(f"New file uploaded: {os.path.basename(file_path)}")
    documents = load_document(file_path)
    st.sidebar.success(f"Loaded documents: {len(documents)}")
    split_docs = split_text(documents)
    st.sidebar.success(f"Number of chunks after splitting: {len(split_docs)}")
    index_docs(split_docs)
elif last_uploaded_file:
    st.session_state.uploaded_file_path = last_uploaded_file
    st.sidebar.info(f"Using previous file: {os.path.basename(last_uploaded_file)}")
    documents = load_document(last_uploaded_file)
    split_docs = split_text(documents)
    index_docs(split_docs)

context = st.sidebar.text_area("Provide context for your question here", value=st.session_state.context, height=200)
st.session_state.context = context
question = st.chat_input("Ask me a question!")

if question and context:
    related_documents = retrieve_docs(question)
    answer = answer_question(question, context, related_documents)
    st.session_state.history.append((question, answer))

for q, a in st.session_state.history:
    st.chat_message("user").write(q)
    st.chat_message("assistant").write(a)

    # # Start document loading, indexing, and rerun
    # if "indexed_documents" not in st.session_state or not st.session_state.indexing_complete:
        # st.write("Starting document loading process...")
        # documents = load_document(file_path)
        # st.write(f"Loaded documents: {len(documents)}")
        # chunked_documents = split_text(documents)
        # st.write(f"Number of chunks after splitting: {len(chunked_documents)}")
        # index_docs(chunked_documents)
        # st.session_state.indexed_documents = chunked_documents
        # # Prevent infinite loop: Don't rerun after indexing is complete
        # if not st.session_state.indexing_complete:
            # st.session_state.indexing_complete = True
            # st.experimental_rerun()  # Trigger rerun after indexing completes