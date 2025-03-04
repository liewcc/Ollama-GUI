@echo off
echo Installing virtualenv...
pip install virtualenv

echo Creating virtual environment...
python -m virtualenv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing required packages from requirements.txt...
pip install -r requirements.txt

echo Deactivating virtual environment...
call deactivate

cmd /k echo Installation completed. You may close this terminal window now.
