from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Conversation(models.Model):
    """Model to store conversation history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    user_message = models.TextField()
    ai_reply = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    tokens_used = models.IntegerField(default=0)
    response_time = models.FloatField(default=0.0)  # in seconds
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
    
    def __str__(self):
        return f"Conversation {self.id} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class UserSession(models.Model):
    """Model to track user sessions"""
    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-last_activity']
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
    
    def __str__(self):
        return f"Session {self.session_id} - {self.user.username if self.user else 'Anonymous'}"


class AIModelConfig(models.Model):
    """Model to store AI model configuration"""
    model_name = models.CharField(max_length=200, unique=True)
    max_tokens = models.IntegerField(default=300)
    temperature = models.FloatField(default=0.7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'AI Model Configuration'
        verbose_name_plural = 'AI Model Configurations'
    
    def __str__(self):
        return f"{self.model_name} (Active: {self.is_active})" 