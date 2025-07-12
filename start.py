#!/usr/bin/env python3
"""
Start script for Cybersecurity AI Assistant
"""

import os
import sys
import subprocess
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has OpenAI API key"""
    if not os.path.exists('.env'):
        print("Error: .env file not found!")
        print("Please run: python setup.py")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'your-openai-api-key-here' in content:
            print("Warning: Please edit .env file and add your OpenAI API key")
            print("Get your API key from: https://platform.openai.com/api-keys")
            return False
    
    return True

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import django
        import openai
        import transformers
        return True
    except ImportError as e:
        print(f"Error: Missing dependency: {e}")
        print("Please run: python setup.py")
        return False

def run_server():
    """Run the Django development server"""
    print("Starting Cybersecurity AI Assistant...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("Error: manage.py not found. Please run this script from the project root.")
        return False
    
    # Check environment and dependencies
    if not check_env_file():
        return False
    
    if not check_dependencies():
        return False
    
    print("Environment check passed")
    print("Starting server at http://localhost:8000")
    print("Web Interface: http://localhost:8000")
    print("API Health: http://localhost:8000/api/health/")
    print("API Test: python test_api.py")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Run the server
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\nServer stopped. Goodbye!")
    except Exception as e:
        print(f"Error starting server: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("Cybersecurity AI Assistant")
    print("Domain-specific AI agent for cybersecurity and malware removal")
    print()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "setup":
            print("Running setup...")
            subprocess.run([sys.executable, "setup.py"])
        elif command == "test":
            print("Running API tests...")
            subprocess.run([sys.executable, "test_api.py"])
        elif command == "demo":
            print("Running demo...")
            subprocess.run([sys.executable, "demo.py"])
        elif command == "help":
            print("Available commands:")
            print("  python start.py          - Start the server")
            print("  python start.py setup    - Run setup")
            print("  python start.py test     - Run API tests")
            print("  python start.py demo     - Run demo")
            print("  python start.py help     - Show this help")
        else:
            print(f"Error: Unknown command: {command}")
            print("Use 'python start.py help' for available commands")
    else:
        run_server()

if __name__ == "__main__":
    main() 