#!/bin/bash
# Bash script to set up Python virtual environment for backend

echo "Setting up Python virtual environment for AI-photobooth backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"

# Create virtual environment
echo -e "\nCreating virtual environment..."
python3 -m venv venv

if [ ! -f "venv/bin/activate" ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "Virtual environment created successfully!"

# Activate virtual environment
echo -e "\nActivating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo -e "\nUpgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo -e "\nInstalling requirements from requirements.txt..."
pip install -r requirements.txt

echo -e "\n========================================"
echo "Setup completed successfully!"
echo "========================================"
echo -e "\nTo activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo -e "\nTo deactivate the virtual environment, run:"
echo "  deactivate"
echo -e "\nTo run the backend server:"
echo "  uvicorn main:app --reload"
