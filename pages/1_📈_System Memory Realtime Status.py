import streamlit as st
import psutil
import subprocess
import time

def get_system_memory():
    try:
        memory_info = psutil.virtual_memory()
        total_memory = memory_info.total / (1024 ** 3)
        used_memory = memory_info.used / (1024 ** 3)
        used_percentage = memory_info.percent
        return f"System Memory: {used_memory:.1f}/{total_memory:.1f}GB ({used_percentage:.1f}%)"
    except Exception:
        return "System Memory: Error retrieving data."

def get_gpu_memory():
    try:
        result = subprocess.Popen(
            ['nvidia-smi', '--query-gpu=memory.total,memory.used', '--format=csv,noheader,nounits'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = result.communicate()
        if result.returncode == 0:
            total_memory, used_memory = map(int, stdout.strip().split(','))
            total_memory = total_memory / 1024
            used_memory = used_memory / 1024
            used_percentage = (used_memory / total_memory) * 100
            return f"GPU Memory: {used_memory:.1f}/{total_memory:.1f}GB ({used_percentage:.1f}%)"
        else:
            return "GPU Memory: Error retrieving data."
    except Exception:
        return "GPU Memory: Error retrieving data."

if 'memory_info' not in st.session_state:
    st.session_state['memory_info'] = ""

def update_memory_info():
    st.session_state['memory_info'] = f"{get_system_memory()}\n{get_gpu_memory()}"

update_memory_info()
st.subheader("Memory Info")

while True:
    st.text(st.session_state['memory_info'])
    time.sleep(1)
    st.rerun()