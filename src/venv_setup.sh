#!/bin/bash

echo " Creating virtual environment..."
python3 -m venv shell_helper_env

echo " Activating environment..."
source shell_helper_env/bin/activate

echo "⬆ Upgrading pip..."
pip install --upgrade pip

echo " Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo " Run app using: source shell_helper_env/bin/activate && python main.py"
