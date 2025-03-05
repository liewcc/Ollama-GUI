import streamlit as st
import subprocess
import json
import time

def is_ollama_running():
    result = subprocess.run(['tasklist'], capture_output=True, text=True, shell=True)
    return 'ollama.exe' in result.stdout.lower() or 'ollama app.exe' in result.stdout.lower()

def start_ollama_server():
    subprocess.Popen(['ollama', 'serve'], shell=True)
    time.sleep(3)  # Give it a few seconds to start
    return is_ollama_running()

def get_available_models():
    result = subprocess.run(['Ollama', 'list'], capture_output=True, text=True, shell=True)
    models = result.stdout.splitlines()
    model_info = []
    for model in models:
        parts = model.split()
        if len(parts) >= 4 and not parts[0].startswith("NAME"):
            name, id, size, modified = parts[0], parts[1], parts[2], " ".join(parts[3:])
            if not size.endswith("GB"):
                size += " GB"
            if modified.startswith("GB"):
                modified = " ".join(modified.split()[1:])
            model_info.append((name, id, size, modified))
    return model_info

def get_loaded_model():
    result = subprocess.run(['Ollama', 'ps'], capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def run_generate_command(model, keep_alive):
    url = 'http://localhost:11434/api/generate'
    try:
        keep_alive = int(keep_alive)
    except ValueError:
        pass
    data = {"model": model, "keep_alive": keep_alive}
    result = subprocess.run(['curl', url, '-d', json.dumps(data)], capture_output=True, text=True, shell=True)
    return result.stdout

if 'reload' not in st.session_state:
    st.session_state.reload = False

if is_ollama_running():
    st.success('Ollama Server is available')
else:
    if st.button('Run Ollama Server'):
        if start_ollama_server():
            st.success('Ollama Server started successfully!')
            st.rerun()
        else:
            st.error('Failed to start Ollama Server.')

if is_ollama_running():
    if st.button('Reload Server Status'):
        st.session_state.reload = not st.session_state.reload
    
    available_models = get_available_models()
    models = [model[0] for model in available_models]
    selected_model = st.selectbox('Select a model to load', models)
    keep_alive_value = st.text_input('Set keep_alive value')
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Load LLM Model'):
            response = run_generate_command(selected_model, keep_alive_value)
            #st.success(f'Model {selected_model} loaded with keep_alive={keep_alive_value}')
    with col2:
        loaded_model = get_loaded_model()
        if loaded_model:
            if st.button('Unload LLM Model'):
                response = run_generate_command(selected_model, 0)
                #st.success(f'Model {selected_model} unloaded (keep_alive=0)')
                st.rerun()
        else:
            st.button('Unload LLM Model', disabled=True)

    st.subheader('Available Models')
    header = "{:<30} {:<20} {:<10} {:<15}".format("NAME", "ID", "SIZE", "MODIFIED")
    model_details = "\n".join(["{:<30} {:<20} {:<10} {:<15}".format(model[0], model[1], model[2], model[3]) for model in available_models])
    st.markdown(f"""
```
{header}
{model_details}
```
""")
    
    st.subheader('Loaded Model')
    loaded_model = get_loaded_model()
    st.markdown(f"""
```
{loaded_model}
```
""")
