@echo off
echo Creating a virtual environment...
py -m venv myenv

if exist myenv\Scripts\activate.bat (
    echo Activation of the virtual environment...
    call myenv\Scripts\activate.bat

    echo Pip update...
    py -m pip install --upgrade pip

    echo Installing dependencies from requirements.txt ...
    py -m pip install -r requirements.txt

    echo Launch main.py ...
    py main.py

    pause
) else (
    echo The virtual environment has not been created. Make sure you have Python and venv installed.
    pause
)
