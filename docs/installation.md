# Installation Guide

This guide will help you set up the Dark Tech Project 2025 environment on your local machine. Follow the steps below to
get started.

## Clone the Repository

First, clone the repository to your local machine using Git:

```bash
git clone git@gitlab.fdmci.hva.nl:studio/dark-tech/projects/2025-2026-semester-1/miilaabuuboo60.git dark-tech
cd dark-tech
```

## Backend Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Virtual Environment (Recommended)

Using a virtual environment isolates your project dependencies from system Python packages.

Navigate to the backend directory:

```bash
cd backend
```

#### For Windows (PowerShell):

```powershell
# Run the setup script
.\setup_venv.ps1

# Or manually create and activate:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### For Linux/Mac:

```bash
# Run the setup script
chmod +x setup_venv.sh
./setup_venv.sh

# Or manually create and activate:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Install packages (without virtual environment)

If you prefer not to use a virtual environment, navigate to the backend directory and install the required packages directly:

```bash
cd backend
pip install -r requirements.txt
```

### Add a Gemini API Key

Get a free Gemini API Key from [Google AI Studio](https://aistudio.google.com/api-keys)

Create a `.env` file in the `backend` directory and add your Gemini API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Run the Backend Server

Make sure your virtual environment is activated (if using one), then start the FastAPI server using Uvicorn:

```bash
# Activate virtual environment first (if not already activated)
# Windows: .\venv\Scripts\Activate.ps1
# Linux/Mac: source venv/bin/activate

uvicorn main:app --reload
```

The backend server will run on `http://localhost:8000`.

## Frontend Setup

### Prerequisites

- Node.js (version 14 or higher)
- npm (Node package manager)

### Install packages

Navigate to the frontend directory and install the required packages:

```bash
cd ../frontend
npm install
```

### Run the Frontend Server

Start the Vue.js development server:

```bash
npm run dev
```

The frontend server will run on `http://localhost:3000`.

## Access the Application

Open your web browser and navigate to `http://localhost:3000` to access the Dark Tech Project 2025 application.

## Access the VPS

## manual docker setup to vps

open docker desktop

### Go to backend folder in dark-tech

```bash
cd backend
```

### Build backend docker file

```bash
docker build -t emetain/dark-tech-backend-review:dev .
```

### Go to frontend folder in dark-tech

```bash
cd ../frontend
```

### Build frontend docker file
```bash
docker build -t emetain/dark-tech-frontend-review:dev .
```

### Save images as tars
```bash
docker save emetain/dark-tech-frontend-review:dev -o frontend.tar
```

```bash
cd ../backend
```

```bash
docker save emetain/dark-tech-backend-review:dev -o backend.tar
```

### Upload files to vps

open FileZilla

enter credentials


```bash
cd ../home/dark-tech
```

### Access vps through terminal

```bash
ssh root@185.228.82.235
```

### Go to the correct folder

```bash
cd ../home/dark-tech
```

### Load docker images

```bash
docker load -i backend.tar
```

```bash
docker load -i frontend.tar
```

### Check if the image is there

```bash
docker images
```

### Check if there are containers running

```bash
docker ps
```

### Delete containers if necessary

```bash
docker stop <container-id>
```

### Run new container for prod

```bash
docker-compose -f docker-compose.prod.yml down -v --remove-orphans
docker-compose -f docker-compose.prod.yml up -d --force-recreate
```

### Run new container for dev
```bash
docker-compose -f docker-compose.dev.yml down -v --remove-orphans
docker-compose -f docker-compose.dev.yml up -d --force-recreate

```