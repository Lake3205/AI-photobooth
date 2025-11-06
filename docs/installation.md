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

### Install packages

Navigate to the backend directory and install the required packages:

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

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

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
