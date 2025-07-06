import logging
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Conversation, UserSession
from .services import ai_service

logger = logging.getLogger(__name__)


class ChatView(APIView):
    """API view for handling chat requests"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Handle chat message and generate AI response"""
        try:
            user_message = request.data.get('message', '').strip()
            session_id = request.data.get('session_id')
            
            if not user_message:
                return Response(
                    {'error': 'Message is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Generate session ID if not provided
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Generate AI response
            ai_result = ai_service.generate_response(user_message)
            
            # Save conversation to database
            conversation = Conversation.objects.create(
                session_id=session_id,
                user_message=user_message,
                ai_reply=ai_result['response'],
                tokens_used=ai_result['tokens_used'],
                response_time=ai_result['response_time']
            )
            
            # Update or create user session
            session, created = UserSession.objects.get_or_create(
                session_id=session_id,
                defaults={'last_activity': conversation.timestamp}
            )
            if not created:
                session.last_activity = conversation.timestamp
                session.save()
            
            logger.info(f"Chat response generated for session {session_id}")
            
            return Response({
                'response': ai_result['response'],
                'session_id': session_id,
                'response_time': ai_result['response_time'],
                'tokens_used': ai_result['tokens_used'],
                'conversation_id': conversation.id
            })
            
        except Exception as e:
            logger.error(f"Error in chat view: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ConversationHistoryView(APIView):
    """API view for retrieving conversation history"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get conversation history for a session"""
        try:
            session_id = request.GET.get('session_id')
            
            if not session_id:
                return Response(
                    {'error': 'Session ID is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            conversations = Conversation.objects.filter(
                session_id=session_id
            ).order_by('timestamp')
            
            history = []
            for conv in conversations:
                history.append({
                    'id': conv.id,
                    'user_message': conv.user_message,
                    'ai_reply': conv.ai_reply,
                    'timestamp': conv.timestamp.isoformat(),
                    'response_time': conv.response_time
                })
            
            return Response({
                'session_id': session_id,
                'conversations': history,
                'total_conversations': len(history)
            })
            
        except Exception as e:
            logger.error(f"Error retrieving conversation history: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ModelInfoView(APIView):
    """API view for getting model information"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get information about the current AI model"""
        try:
            model_info = ai_service.get_model_info()
            return Response(model_info)
        except Exception as e:
            logger.error(f"Error getting model info: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'service': 'AI Assistant',
        'model': ai_service.get_model_info()
    })


# Template views for web interface
def chat_interface(request):
    """Render the main chat interface"""
    return render(request, 'assistant/chat.html')


def about_view(request):
    """Render the about page"""
    return render(request, 'assistant/about.html') 