import subprocess
import pandas as pd
import streamlit as st
import time

# Function to run the tasklist command
def get_tasklist_info():
    result = subprocess.run(['tasklist'], stdout=subprocess.PIPE, text=True, shell=True)
    return result.stdout

# Process the output and create a DataFrame
def create_dataframe(data):
    columns = ["Image Name", "PID", "Session Name", "Session#", "Mem Usage"]
    rows = []
    for line in data.splitlines():
        if "ollama.exe" in line or "ollama app.exe" in line:
            parts = list(filter(None, line.split(" ")))
            if "ollama.exe" in line:
                image_name = "ollama.exe"
            else:
                image_name = "ollama app.exe"
            
            if image_name == "ollama app.exe":
                parts = [image_name] + parts[2:]  # Ensure "app.exe" remains together
            
            rows.append(parts[:5])  # Extract relevant columns
    
    df = pd.DataFrame(rows, columns=columns)
    return df

# Function to terminate selected processes
def kill_process(pids):
    for pid in pids:
        subprocess.run(["taskkill", "/PID", str(pid), "/F"], shell=True)

# Function to kill all tasks and ensure they are terminated
def kill_all_tasks(df):
    while not df.empty:
        pids = df["PID"].tolist()
        kill_process(pids)
        time.sleep(2)  # Wait before checking again
        tasklist_info = get_tasklist_info()
        df = create_dataframe(tasklist_info) if tasklist_info else pd.DataFrame()

# Streamlit app
tasklist_info = get_tasklist_info()
df = create_dataframe(tasklist_info) if tasklist_info else pd.DataFrame()

if not df.empty:
    st.write('### Process Information')
    header = "{:<20}  {:<8}  {:<15}  {:<10}  {:<12}".format("Image Name", "PID", "Session Name", "Session#", "Mem Usage")
    table_string = "\n".join([header] + [("{:<20}  {:<8}  {:<15}  {:<10}  {:<12}".format(*row)) for row in df.values])
    st.code(table_string, language="text")
    
    st.write('### Select Processes to Terminate')
    
    selected_pids = []
    for index, row in df.iterrows():
        checkbox = st.checkbox(f"{row['Image Name']} (PID: {row['PID']})", key=row['PID'])
        if checkbox:
            selected_pids.append(row['PID'])
    
    if st.button("Kill Selected Process"):
        if selected_pids:
            kill_process(selected_pids)
            st.rerun()  # Reload the page to update process list
        else:
            st.warning("No process selected.")
    
    if st.button("Kill All Processes"):
        kill_all_tasks(df)
        st.rerun()
else:
    st.error('No "ollama" or "ollama app" processes found.')
