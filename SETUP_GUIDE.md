# Cybersecurity AI Assistant - Setup Guide

## Quick Setup

### Step 1: Setup
```bash
python setup.py
```

### Step 2: Add OpenAI API Key
Edit `.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=your-openai-api-key-here
```

### Step 3: Start the Application
```bash
python start.py
```

### Step 4: Test Everything
```bash
python start.py test
```

### Step 5: Run Demo
```bash
python start.py demo
```

## Features

- Cybersecurity classification
- Expert responses for security issues
- Polite rejection for non-security questions
- Web interface
- RESTful API

## Usage

1. Web Interface: Visit http://localhost:8000
2. API Testing: Use the provided endpoints
3. Examples:
   - "How do I remove malware from my computer?"
   - "What should I do if my account was hacked?"
   - "How can I protect my network from attacks?"

## API Endpoints

- `POST /api/chat/` - Send messages
- `POST /api/classify/` - Classify queries
- `GET /api/stats/` - Get statistics
- `GET /api/health/` - Health check

## Cybersecurity Topics Covered

- Malware detection and removal
- Network security
- Privacy protection
- System security
- Threat analysis
- Security best practices

## Available Commands

```bash
python start.py          # Start the server
python start.py setup    # Run setup
python start.py test     # Run API tests
python start.py demo     # Run demo
python start.py help     # Show help
```

## Configuration Options

### OpenAI (Recommended)
```env
USE_OPENAI=True
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-3.5-turbo
```

### Local Model (Smaller)
```env
USE_OPENAI=False
AI_MODEL_NAME=microsoft/DialoGPT-medium
MAX_NEW_TOKENS=150
```

---

**Note**: OpenAI option is recommended as it doesn't require downloading large models and provides better responses. 