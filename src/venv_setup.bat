@echo off
echo Creating virtual environment...
python -m venv shell_helper_env

echo Activating virtual environment...
call shell_helper_env\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo %cd%

echo Installing requirements from src/...
pip install -r "%~dp0requirements.txt"

echo ✅ Setup complete!
echo 👉 To activate later: call shell_helper_env\Scripts\activate.bat
pause

@REM @echo off
@REM echo Creating virtual environment...
@REM python -m venv shell_helper_env

@REM echo Activating virtual environment...
@REM call shell_helper_env\Scripts\activate.bat

@REM echo Upgrading pip...
@REM python -m pip install --upgrade pip

@REM echo Installing requirements from src/...
@REM pip install -r src\requirements.txt

@REM echo ✅ Setup complete!
@REM echo  To activate later: call shell_helper_env\Scripts\activate.bat
@REM pause