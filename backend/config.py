"""
Environment configuration loader
Loads appropriate .env file based on environment
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Get the project root directory (one level up from backend)
PROJECT_ROOT = Path(__file__).parent.parent

# Determine which env file to load
ENV = os.getenv('ENV', 'development')

if ENV == 'development':
    env_file = PROJECT_ROOT / '.env.development'
elif ENV == 'production':
    env_file = PROJECT_ROOT / '.env'
else:
    env_file = PROJECT_ROOT / '.env'

# Load the environment file
if env_file.exists():
    load_dotenv(dotenv_path=env_file)
    print(f"Loaded environment from: {env_file}")
else:
    print(f"Warning: Environment file not found: {env_file}")
    # Fallback to root .env
    fallback_env = PROJECT_ROOT / '.env'
    if fallback_env.exists():
        load_dotenv(dotenv_path=fallback_env)
        print(f"Loaded fallback environment from: {fallback_env}")
    else:
        load_dotenv()  # Try to load from default .env

# Export commonly used environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE_URL = os.getenv('OPENAI_API_BASE_URL')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this-in-production')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')