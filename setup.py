#!/usr/bin/env python3
"""
Setup script for Cybersecurity AI Assistant
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"Success: {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        env_content = """# Django Settings
SECRET_KEY=django-insecure-cybersecurity-ai-assistant-2024
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI Configuration (Recommended - No model download needed!)
USE_OPENAI=True
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# For local models (if you prefer):
# USE_OPENAI=False
# AI_MODEL_NAME=microsoft/DialoGPT-medium
# MAX_NEW_TOKENS=150

# Logging Configuration
LOG_LEVEL=INFO
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("Success: .env file created")
        print("Warning: Please edit .env file and add your OpenAI API key")
        return True
    else:
        print("Info: .env file already exists")
        return True

def main():
    """Main setup function"""
    print("Cybersecurity AI Assistant - Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8+ is required")
        return False
    
    print(f"Info: Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    else:
        print("Info: Virtual environment already exists")
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Run migrations
    if not run_command(f"{activate_cmd} && python manage.py migrate", "Running database migrations"):
        return False
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: python start.py")
    print("3. Visit: http://localhost:8000")
    print("4. Test API: python test_api.py")
    print("\nFor more information, see SETUP_GUIDE.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 