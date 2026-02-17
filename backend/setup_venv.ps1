# PowerShell script to set up Python virtual environment for backend

Write-Host "Setting up Python virtual environment for AI-photobooth backend..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Green
python -m venv venv

if (-Not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "Virtual environment created successfully!" -ForegroundColor Green

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Green
python -m pip install --upgrade pip

# Install requirements
Write-Host "`nInstalling requirements from requirements.txt..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nTo activate the virtual environment in the future, run:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "`nTo deactivate the virtual environment, run:" -ForegroundColor Yellow
Write-Host "  deactivate" -ForegroundColor White
Write-Host "`nTo run the backend server:" -ForegroundColor Yellow
Write-Host "  uvicorn main:app --reload" -ForegroundColor White
