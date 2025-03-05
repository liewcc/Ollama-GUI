import streamlit as st
import psutil
import os
import signal
import sys

def terminate_process():
    # Get the current process ID
    current_pid = os.getpid()
    # Find parent process (terminal)
    parent_process = psutil.Process(current_pid).parent()
    # Terminate the Streamlit process
    os.kill(current_pid, signal.SIGTERM)
    # Terminate the parent process (terminal)
    parent_process.terminate()

st.set_page_config(
    page_title="Hello",
    page_icon="🏠︎",
)

st.write("# Welcome to Streamlit! :wave:")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
"""
)

if st.button("Terminate Streamlit"):
    st.warning("Terminating Streamlit process...")
    terminate_process()
    st.stop()