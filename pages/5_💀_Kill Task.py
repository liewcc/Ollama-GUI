import subprocess
import pandas as pd
import streamlit as st

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
            # Ensure "ollama" and "app.exe" appear in the same cell for "Image Name"
            if image_name == "ollama app.exe":
                parts = [image_name] + parts[2:]  # Adjust index to keep "app.exe" together
            rows.append(parts[:5])  # Extract the relevant columns
    df = pd.DataFrame(rows, columns=columns)
    return df

# Streamlit app
st.title('Ollama Process Information')

# Get the tasklist info and create a DataFrame
tasklist_info = get_tasklist_info()
if tasklist_info:
    df = create_dataframe(tasklist_info)
    if not df.empty:
        st.write('### Process Information')
        # Convert DataFrame to string with fixed-width formatting and added spaces between columns
        header = "{:<20}  {:<8}  {:<15}  {:<10}  {:<12}".format("Image Name", "PID", "Session Name", "Session#", "Mem Usage")
        table_string = "\n".join([header] + [("{:<20}  {:<8}  {:<15}  {:<10}  {:<12}".format(*row)) for row in df.values])
        st.markdown(f"```\n{table_string}\n```")
    else:
        st.write('No "ollama" or "ollama app" processes found.')
else:
    st.write('Error running the command.')


# import subprocess
# import pandas as pd
# import streamlit as st

# # Function to run the tasklist command
# def get_tasklist_info():
    # result = subprocess.run(['tasklist'], stdout=subprocess.PIPE, text=True, shell=True)
    # return result.stdout

# # Process the output and create a DataFrame
# def create_dataframe(data):
    # columns = ["Image Name", "PID", "Session Name", "Session#", "Mem Usage"]
    # rows = []
    # for line in data.splitlines():
        # if "ollama.exe" in line or "ollama app.exe" in line:
            # parts = list(filter(None, line.split(" ")))
            # if "ollama.exe" in line:
                # image_name = "ollama.exe"
            # else:
                # image_name = "ollama app.exe"
            # # Ensure "ollama" and "app.exe" appear in the same cell for "Image Name"
            # if image_name == "ollama app.exe":
                # parts = [image_name] + parts[2:]  # Adjust index to keep "app.exe" together
            # rows.append(parts[:5])  # Extract the relevant columns
    # df = pd.DataFrame(rows, columns=columns)
    # return df

# # Streamlit app
# st.title('Ollama Process Information')

# # Get the tasklist info and create a DataFrame
# tasklist_info = get_tasklist_info()
# if tasklist_info:
    # df = create_dataframe(tasklist_info)
    # if not df.empty:
        # st.write('### Process Information')

        # # Add a checkbox column to the DataFrame
        # df['Select'] = False

        # # Display the DataFrame with checkboxes
        # for idx, row in df.iterrows():
            # df.at[idx, 'Select'] = st.checkbox(f"{row['Image Name']} | PID: {row['PID']}", key=idx)

        # # Display the updated DataFrame
        # st.dataframe(df)
    # else:
        # st.write('No "ollama" or "ollama app" processes found.')
# else:
    # st.write('Error running the command.')
