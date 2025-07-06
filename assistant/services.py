import time
import logging
from typing import Optional, Dict, Any
from django.conf import settings
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

logger = logging.getLogger(__name__)


class AIService:
    """Service class for handling AI model interactions"""
    
    def __init__(self):
        self.model_name = settings.AI_MODEL_NAME
        self.max_new_tokens = settings.MAX_NEW_TOKENS
        self.pipe = None
        self.tokenizer = None
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the AI model and tokenizer"""
        try:
            logger.info(f"Initializing AI model: {self.model_name}")
            
            # Initialize the pipeline for text generation
            self.pipe = pipeline(
                "text-generation",
                model=self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )
            
            logger.info("AI model initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing AI model: {str(e)}")
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
            # Prepare the prompt
            prompt = self._prepare_prompt(user_message)
            
            # Generate response
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
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Estimate tokens used (rough calculation)
            tokens_used = len(ai_response.split()) * 1.3  # Rough estimation
            
            logger.info(f"Generated response in {response_time:.2f}s, tokens: {tokens_used:.0f}")
            
            return {
                'response': ai_response,
                'response_time': response_time,
                'tokens_used': int(tokens_used),
                'model_name': self.model_name
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    def _prepare_prompt(self, user_message: str) -> str:
        """
        Prepare the prompt for the AI model
        
        Args:
            user_message: The user's input message
            
        Returns:
            Formatted prompt string
        """
        # For DeepSeek models, use their specific prompt format
        if "deepseek" in self.model_name.lower():
            prompt = f"<|im_start|>user\n{user_message}<|im_end|>\n<|im_start|>assistant\n"
        else:
            # Generic prompt format
            prompt = f"User: {user_message}\nAssistant: "
        
        return prompt
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            'model_name': self.model_name,
            'max_tokens': self.max_new_tokens,
            'is_loaded': self.pipe is not None
        }


# Global instance of AI service
ai_service = AIService() 