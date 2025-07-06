from django.contrib import admin
from .models import Conversation, UserSession, AIModelConfig


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_id', 'timestamp', 'tokens_used', 'response_time']
    list_filter = ['timestamp', 'user']
    search_fields = ['user_message', 'ai_reply', 'user__username']
    readonly_fields = ['timestamp', 'tokens_used', 'response_time']
    date_hierarchy = 'timestamp'


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'created_at', 'last_activity', 'is_active']
    list_filter = ['is_active', 'created_at', 'last_activity']
    search_fields = ['session_id', 'user__username']
    readonly_fields = ['created_at', 'last_activity']


@admin.register(AIModelConfig)
class AIModelConfigAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'max_tokens', 'temperature', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['model_name']
    readonly_fields = ['created_at', 'updated_at'] 