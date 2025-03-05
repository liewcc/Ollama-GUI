import streamlit as st
import psutil
import subprocess
import time

def get_ollama_processes():
    """Check for processes with 'ollama' in the name and return their details."""
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            name = proc.info['name'].lower()
            if 'ollama' in name:
                processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes

def get_ollama_status():
    """Execute 'ollama ps' and return the output."""
    try:
        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing 'ollama ps': {e}"
    except FileNotFoundError:
        return "Ollama CLI not found. Ensure it's installed and accessible."

placeholder = st.empty()

# Auto-refresh logic using session state
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

while True:
    processes = get_ollama_processes()
    output = "### Ollama Processes Found\n"
    
    if processes:
        status = get_ollama_status()
        for proc in processes:
            output += f"- **PID:** {proc['pid']} | **Name:** {proc['name']}\n"
        output += f"\n### Loaded Model\n```\n{status}\n```\n"
    else:
        output = "### No Ollama processes detected."
    
    placeholder.markdown(output)
    time.sleep(1)
