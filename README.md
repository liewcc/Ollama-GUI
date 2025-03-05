# About
This is a straightforward Python script running on a Streamlit GUI, designed for users to test all features of Ollama on a local computer.

Currently, most available Ollama GUIs (e.g. [Open WebUI](https://github.com/open-webui/open-webui) or [Chatbox](https://chatboxai.app/)) require external virtual environment packages (e.g. Docker) to be installed. Alternatively, I decided to create a simple Ollama GUI using Python's built-in virtual environment tool.

The goal of this project is to build an ultra-lightweight, easy-to-install, and fast-deployable repository for users to test all Ollama features.

## Table of Contents
1. [Installation](#installation)

## Installation
1. Install packages listed below:

  - [Python](https://www.python.org/downloads/)

  - [Ollama](https://github.com/ollama/ollama)

  - [LLM Models](https://ollama.com/search)

> ## :bulb: Tip: LLM Models
> Please note that for LLM models located on the Ollama server, you can either download the model manually or Ollama will automatically start the downloading process when you run Ollama with the assigned model for the first time. Ollama stores all downloaded models in:

>`C:\Users\[user name]\.ollama\models\manifests\registry.ollama.ai\library\` 

>If you want to use any LLM model from a website other than Ollama, make sure to place the model in the folder mentioned above.

2. Navigate to the folder where you want to install the repository. Hold down the **Shift** key and right-click on an empty space within the folder. From the context menu that appears, select **"Open command window here"** or **"Open PowerShell window here"** (depending on your system configuration). Copy and paste the following commands into terminal windows:
```sh
git clone https://github.com/liewcc/Ollama-GUI.git
cd Ollama-GUI
setup
```
3. Close terminal window.

4. Run Ollama-GUI.bat

> ## :bulb: Tip: Creating a Desktop Shortcut for *Ollama-GUI.bat* on Windows
> 
> Follow these steps to create a desktop shortcut for the `Ollama-GUI.bat`:
> 
> 1. **Navigate to the File Location:**
>    - Open **File Explorer**.
>    - Go to the Ollama-GUI root directory and find `Ollama-GUI.bat`
> 
> 2. **Create the Shortcut:**
>    - Right-click on the `Ollama-GUI.bat` file.
>    - Select **Send to** and then click on **Desktop (create shortcut)**.
> 
> 3. **Rename the Shortcut (Optional):**
>    - Go to your desktop and find the newly created shortcut.
>    - Right-click on the shortcut and select **Rename**.
>    - Enter a new name for the shortcut if desired (e.g., **Ollama-GUI**).
> 
> 4. **Set Shortcut Properties (Optional):**
>    - Right-click on the shortcut and select **Properties**.
>    - Under the **Shortcut** tab, you can:
>      - **Change the icon** by clicking on **Change Icon...**.
>      - You can find Ollama ico file inside `icon\` folder.
> 
> 5. **Apply Changes:**
>    - Click **Apply** and then **OK** to save any changes made.
> 
> You now have a desktop shortcut to easily access your `Ollama-GUI.bat` file.
