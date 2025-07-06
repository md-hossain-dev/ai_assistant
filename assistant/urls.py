from django.urls import path
from . import views

app_name = 'assistant'

urlpatterns = [
    # Web interface routes
    path('', views.chat_interface, name='chat'),
    path('about/', views.about_view, name='about'),
    
    # API routes
    path('api/chat/', views.ChatView.as_view(), name='api_chat'),
    path('api/history/', views.ConversationHistoryView.as_view(), name='api_history'),
    path('api/model-info/', views.ModelInfoView.as_view(), name='api_model_info'),
    path('api/health/', views.health_check, name='api_health'),
] 