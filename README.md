# Cybersecurity AI Assistant

A domain-specific AI agent built with Django that specializes in cybersecurity and malware removal. The assistant uses intelligent classification to determine if queries are cybersecurity-related and provides expert guidance for security issues.

## Quick Start

**Setup:**
```bash
python setup.py
# Edit .env file with OpenAI API key
python start.py
```

**Test:**
```bash
python start.py test
python start.py demo
```

## Features

### Domain-Specific Focus
- Intelligent classification system for cybersecurity queries
- Specialized responses for different security categories
- Polite rejection for non-cybersecurity topics

### AI-Powered Responses
- OpenAI API integration (default)
- Local model support (optional)
- Contextual prompts for accurate responses

### Web Interface
- Real-time chat interface
- Classification indicators
- Session management
- Statistics display

### Cybersecurity Expertise
- Malware detection and removal guidance
- Security best practices
- Network security advice
- Privacy protection tips
- System security recommendations
- Threat analysis support

## API Endpoints

- `POST /api/chat/` - Send messages and get AI responses
- `POST /api/classify/` - Classify queries without generating responses
- `GET /api/history/` - Retrieve conversation history
- `GET /api/model-info/` - Get AI model information
- `GET /api/stats/` - Get cybersecurity statistics
- `GET /api/health/` - Health check endpoint

## Configuration

### OpenAI (Recommended)
```env
USE_OPENAI=True
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-3.5-turbo
```

### Local Model
```env
USE_OPENAI=False
AI_MODEL_NAME=microsoft/DialoGPT-medium
MAX_NEW_TOKENS=150
```

## Project Structure

```
ai_assistant/
├── ai_assistant/          # Django project settings
├── assistant/             # Main application
│   ├── classifier.py      # Cybersecurity classification logic
│   ├── models.py          # Database models
│   ├── services.py        # AI service integration
│   ├── views.py           # API and web views
│   └── urls.py            # URL routing
├── templates/             # HTML templates
├── static/                # Static files
├── requirements.txt       # Python dependencies
├── setup.py              # Setup script
├── start.py              # Start script
├── test_api.py           # API test script
├── demo.py               # Demo script
└── README.md             # This file
```

## Installation

1. Clone the repository
2. Run `python setup.py`
3. Add OpenAI API key to `.env` file
4. Run `python start.py`
5. Visit http://localhost:8000

## Testing

```bash
python start.py test     # Run comprehensive tests
python start.py demo     # Run demo
```

## Security Considerations

- Input validation and sanitization
- CSRF protection enabled
- SQL injection prevention
- XSS protection
- Secure session management

## License

This project is licensed under the MIT License.

## Support

For issues and questions, create an issue on GitHub or check the documentation.

---

**Note**: This AI assistant is designed for educational and guidance purposes. For serious security incidents, always consult with professional cybersecurity experts.