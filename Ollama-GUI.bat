@echo off

call venv\Scripts\activate.bat

python run_entrypoint.py

call deactivate

cmd /k
