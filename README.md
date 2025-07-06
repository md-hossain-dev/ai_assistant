# AI Assistant - DeepSeek Powered Chat Application

A professional AI chat assistant built with Django and powered by DeepSeek AI models through HuggingFace Transformers.

## 🚀 Features

- **Advanced AI Model**: Powered by DeepSeek AI models for intelligent conversations
- **Real-time Chat Interface**: Modern, responsive web interface with real-time messaging
- **Conversation History**: Persistent storage of all conversations with session management
- **Programming Expert**: Specialized in programming languages and software development
- **Professional UI/UX**: Beautiful, modern interface with smooth animations
- **Session Management**: Secure session handling with unique session IDs
- **Performance Monitoring**: Track response times and token usage
- **Error Handling**: Robust error handling and logging
- **RESTful API**: Complete API for integration with other applications

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **AI Model**: DeepSeek AI (via HuggingFace Transformers)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (configurable for PostgreSQL/MySQL)
- **API**: Django REST Framework
- **Styling**: Custom CSS with gradient designs
- **Icons**: Font Awesome

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- At least 8GB RAM (for running the AI model)
- GPU recommended for better performance

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai_assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure it:

```bash
cp env.example .env
```

Edit `.env` file with your settings:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# AI Model Settings
AI_MODEL_NAME=deepseek-ai/deepseek-coder-6.7b-instruct
MAX_NEW_TOKENS=300
```

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Application

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## 📖 Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Start chatting with the AI assistant
3. Your conversations will be automatically saved
4. Use the session ID to retrieve conversation history

### API Endpoints

#### Chat API
```http
POST /api/chat/
Content-Type: application/json

{
    "message": "Your message here",
    "session_id": "optional-session-id"
}
```

#### Conversation History
```http
GET /api/history/?session_id=your-session-id
```

#### Model Information
```http
GET /api/model-info/
```

#### Health Check
```http
GET /api/health/
```

## 🔧 Configuration

### AI Model Configuration

You can change the AI model by modifying the `AI_MODEL_NAME` in your `.env` file:

```env
# Available models:
AI_MODEL_NAME=deepseek-ai/deepseek-coder-6.7b-instruct
AI_MODEL_NAME=deepseek-ai/deepseek-coder-33b-instruct
AI_MODEL_NAME=deepseek-ai/deepseek-llm-7b-chat
```

### Performance Settings

Adjust the model parameters in `settings.py`:

```python
MAX_NEW_TOKENS = 300  # Maximum tokens to generate
```

## 📁 Project Structure

```
ai_assistant/
├── ai_assistant/          # Main Django project
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── assistant/            # AI Assistant app
│   ├── models.py        # Database models
│   ├── views.py         # API views and web views
│   ├── services.py      # AI model service
│   ├── admin.py         # Django admin configuration
│   └── urls.py          # App URL configuration
├── templates/           # HTML templates
│   └── assistant/
│       ├── chat.html    # Main chat interface
│       └── about.html   # About page
├── static/              # Static files
│   └── css/
│       └── style.css    # Custom styles
├── logs/                # Application logs
├── requirements.txt     # Python dependencies
├── manage.py           # Django management script
└── README.md           # This file
```

## 🔒 Security Features

- CSRF protection enabled
- Session management with secure session IDs
- Input validation and sanitization
- Error handling without exposing sensitive information
- Environment variable configuration

## 📊 Monitoring and Logging

The application includes comprehensive logging:

- Request/response logging
- Error tracking
- Performance monitoring
- AI model interaction logs

Logs are stored in the `logs/` directory.

## 🚀 Deployment

### Production Deployment

1. Set `DEBUG=False` in your environment
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure your web server (Nginx + Gunicorn recommended)
5. Set up SSL certificates

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "ai_assistant.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the logs in the `logs/` directory
2. Verify your environment configuration
3. Ensure all dependencies are installed
4. Check the Django documentation for common issues

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Multiple AI model support
- [ ] File upload and processing
- [ ] Voice input/output
- [ ] Mobile application
- [ ] Advanced conversation analytics
- [ ] Integration with external APIs
- [ ] Multi-language support

## 🙏 Acknowledgments

- DeepSeek AI for providing the language models
- HuggingFace for the transformers library
- Django community for the excellent framework
- Bootstrap team for the UI components

---

**Note**: This application requires significant computational resources to run the AI model. For production use, consider using cloud services or dedicated hardware with GPU support.