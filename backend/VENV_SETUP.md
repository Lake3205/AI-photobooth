# Backend Virtual Environment Setup

This guide explains how to set up and use a Python virtual environment for the backend.

## Quick Setup

### Windows (PowerShell)
```powershell
cd backend
.\setup_venv.ps1
```

### Linux/Mac
```bash
cd backend
chmod +x setup_venv.sh
./setup_venv.sh
```

## Manual Setup

If you prefer to set it up manually:

### Windows
```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Linux/Mac
```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## Daily Usage

### Activate the Environment

**Windows:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
cd backend
source venv/bin/activate
```

When activated, you'll see `(venv)` in your terminal prompt.

### Run the Backend Server

```bash
uvicorn main:app --reload
```

### Deactivate the Environment

When you're done working:
```bash
deactivate
```

## Benefits of Using Virtual Environment

- **Isolation**: Dependencies are isolated from system Python packages
- **Reproducibility**: Ensures all developers use the same package versions
- **Clean system**: Avoids polluting global Python installation
- **Multiple projects**: Different projects can have different dependency versions

## Troubleshooting

### PowerShell Execution Policy Error

If you get an error about execution policies on Windows:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python command not found

Make sure Python is installed and added to your PATH:
- Windows: Download from [python.org](https://www.python.org/downloads/)
- Mac: `brew install python3`
- Linux: `sudo apt install python3 python3-venv` (Ubuntu/Debian)

### Virtual environment already exists

If you need to recreate the virtual environment:

```bash
# Delete the old one
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows CMD
Remove-Item -Recurse -Force venv  # Windows PowerShell

# Create new one
python -m venv venv
```
