import streamlit as st
import subprocess
import json

def is_ollama_running():
    result = subprocess.run(['tasklist', '|', 'findstr', '/i', 'ollama'], capture_output=True, text=True, shell=True)
    return 'ollama' in result.stdout

def get_available_models():
    result = subprocess.run(['Ollama', 'list'], capture_output=True, text=True, shell=True)
    models = result.stdout.splitlines()
    model_info = []
    for model in models:
        # Simulate model info extraction
        parts = model.split()  # Assuming output is space-separated
        if len(parts) >= 4 and not parts[0].startswith("NAME"):  # Ensure there are enough parts to unpack and skip header
            name, id, size, modified = parts[0], parts[1], parts[2], " ".join(parts[3:])
            if not size.endswith("GB"):
                size += " GB"  # Append 'GB' to the size if not already present
            if modified.startswith("GB"):
                modified = " ".join(modified.split()[1:])  # Remove 'GB' from the modified string
            model_info.append((name, id, size, modified))
    return model_info

def get_loaded_model():
    result = subprocess.run(['Ollama', 'ps'], capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def run_generate_command(model, keep_alive):
    url = 'http://localhost:11434/api/generate'
    try:
        keep_alive = int(keep_alive)  # Convert to integer if possible
    except ValueError:
        pass  # Keep as string if conversion fails
    data = {"model": model, "keep_alive": keep_alive}
    result = subprocess.run(['curl', url, '-d', json.dumps(data)], capture_output=True, text=True, shell=True)
    return result.stdout


if 'reload' not in st.session_state:
    st.session_state.reload = False

if is_ollama_running():
    st.success('Ollama Server is available')

    if st.button('Reload Server Status'):
        st.session_state.reload = not st.session_state.reload

    available_models = get_available_models()
    models = [model[0] for model in available_models]
    selected_model = st.selectbox('Select a model to load', models)
    
    # Use st.text_input to allow any text or number
    keep_alive_value = st.text_input('Set keep_alive value')

    if st.button('Load LLM Model'):
        response = run_generate_command(selected_model, keep_alive_value)
        st.markdown(f"```\n{response}\n```")

    st.subheader('Available Models')
    header = "{:<30} {:<20} {:<10} {:<15}".format("NAME", "ID", "SIZE", "MODIFIED")
    model_details = "\n".join(["{:<30} {:<20} {:<10} {:<15}".format(model[0], model[1], model[2], model[3]) for model in available_models])
    st.markdown(f"```\n{header}\n{model_details}\n```")

    st.subheader('Loaded Model')
    loaded_model = get_loaded_model()
    st.markdown(f"```\n{loaded_model}\n```")
else:
    st.error('Ollama Server has not started')
    st.button('Reload', disabled=True)


