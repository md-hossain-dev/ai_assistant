import time
import logging
import os
from typing import Optional, Dict, Any
from django.conf import settings
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from .classifier import cybersecurity_classifier

logger = logging.getLogger(__name__)


class AIService:
    """Service class for handling AI model interactions"""
    
    def __init__(self):
        self.model_name = settings.AI_MODEL_NAME
        self.max_new_tokens = settings.MAX_NEW_TOKENS
        self.use_openai = os.getenv('USE_OPENAI', 'True').lower() == 'true'  # Default to OpenAI
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        
        # Local model components
        self.pipe = None
        self.tokenizer = None
        self.model = None
        
        if not self.use_openai:
            self._initialize_local_model()
        else:
            self._initialize_openai()
    
    def _initialize_local_model(self):
        """Initialize the local AI model and tokenizer"""
        try:
            logger.info(f"Initializing local AI model: {self.model_name}")
            
            # Initialize the pipeline for text generation
            self.pipe = pipeline(
                "text-generation",
                model=self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )
            
            logger.info("Local AI model initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing local AI model: {str(e)}")
            raise
    
    def _initialize_openai(self):
        """Initialize OpenAI client"""
        try:
            if not self.openai_api_key:
                raise ValueError("OpenAI API key not found in environment variables")
            
            import openai
            self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
            logger.info("OpenAI client initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing OpenAI: {str(e)}")
            raise
    
    def generate_response(self, user_message: str, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """
        Generate AI response for user message
        
        Args:
            user_message: The user's input message
            max_tokens: Maximum tokens to generate (optional)
            
        Returns:
            Dictionary containing response and metadata
        """
        start_time = time.time()
        
        try:
            # First, classify the query
            classification = cybersecurity_classifier.classify_query(user_message)
            
            if not classification['is_cybersecurity']:
                # Return rejection message for non-cybersecurity queries
                response_time = time.time() - start_time
                return {
                    'response': cybersecurity_classifier.get_rejection_message(),
                    'response_time': response_time,
                    'tokens_used': 0,
                    'model_name': 'classification_rejection',
                    'classification': classification,
                    'is_cybersecurity': False
                }
            
            # Generate cybersecurity-specific response
            if self.use_openai:
                ai_response = self._generate_openai_response(user_message, classification, max_tokens)
            else:
                ai_response = self._generate_local_response(user_message, classification, max_tokens)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Estimate tokens used (rough calculation)
            tokens_used = len(ai_response.split()) * 1.3  # Rough estimation
            
            logger.info(f"Generated cybersecurity response in {response_time:.2f}s, tokens: {tokens_used:.0f}")
            
            return {
                'response': ai_response,
                'response_time': response_time,
                'tokens_used': int(tokens_used),
                'model_name': self.openai_model if self.use_openai else self.model_name,
                'classification': classification,
                'is_cybersecurity': True
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    def _generate_openai_response(self, user_message: str, classification: Dict[str, Any], max_tokens: Optional[int] = None) -> str:
        """Generate response using OpenAI API"""
        try:
            # Get cybersecurity-specific prompt
            prompt = cybersecurity_classifier.get_cybersecurity_prompt(
                user_message, 
                classification.get('primary_category', 'general')
            )
            
            max_new_tokens = max_tokens or self.max_new_tokens
            
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=max_new_tokens,
                temperature=0.7,
                top_p=0.95
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {str(e)}")
            raise
    
    def _generate_local_response(self, user_message: str, classification: Dict[str, Any], max_tokens: Optional[int] = None) -> str:
        """Generate response using local model"""
        try:
            # Get cybersecurity-specific prompt
            prompt = cybersecurity_classifier.get_cybersecurity_prompt(
                user_message, 
                classification.get('primary_category', 'general')
            )
            
            max_new_tokens = max_tokens or self.max_new_tokens
            
            output = self.pipe(
                prompt,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.1,
                pad_token_id=self.pipe.tokenizer.eos_token_id
            )
            
            # Extract the generated text
            generated_text = output[0]['generated_text']
            
            # Remove the original prompt from the response
            ai_response = generated_text[len(prompt):].strip()
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error generating local response: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            'model_name': self.openai_model if self.use_openai else self.model_name,
            'max_tokens': self.max_new_tokens,
            'is_loaded': True,
            'provider': 'OpenAI' if self.use_openai else 'Local',
            'use_openai': self.use_openai
        }


# Global instance of AI service
ai_service = AIService() 