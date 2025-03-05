import streamlit as st
import psutil
import os
import signal

# ✅ Set page config (must be first)
st.set_page_config(
    page_title="Ollama GUI",
    page_icon="🏠︎",
)

st.write("# Ollama GUI 👋")

st.markdown(
    """
    Check my GitHub for the latest update: [GitHub Repo](https://github.com/liewcc/Ollama-GUI)
    """
)

def terminate_process():
    # Get the current process ID
    current_pid = os.getpid()
    # Find parent process (terminal)
    try:
        parent_process = psutil.Process(current_pid).parent()
        if parent_process:
            parent_process.terminate()  # Terminate the parent process (terminal)
    except psutil.NoSuchProcess:
        pass  # Parent process might not exist

    os.kill(current_pid, signal.SIGTERM)  # Terminate the Streamlit process

# ✅ Center the Shutdown button using Streamlit columns
st.write("")  # Spacer
col1, col2, col3 = st.columns([1, 2, 1])  # Center column is wider

with col2:
    st.markdown(
        """
        <style>
        div.stButton > button {
            display: block;
            margin: 0 auto;
            width: auto !important;
            padding: 10px 20px;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button("Shutdown"):  # Button fills column
        st.warning("Terminating Streamlit process...")
        terminate_process()
        st.stop()

# ✅ Center the warning message properly
st.write("")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        "<p style='text-align: center; font-weight: bold;'>⚠ Close terminal windows manually after shutdown</p>",
        unsafe_allow_html=True
    )
