"""
LLM Router for Xempla AI Systems Intern Prototype

Routes requests to appropriate LLM providers based on configuration and availability.
"""
import os
from typing import Optional
from .gemini_client import GeminiClient

class LLMRouter:
    """Routes LLM requests to appropriate providers"""
    
    def __init__(self):
        """Initialize the LLM router with available providers"""
        self.gemini = None
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available LLM providers"""
        # Initialize Gemini if API key is available
        gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        if gemini_api_key:
            try:
                self.gemini = GeminiClient(api_key=gemini_api_key)
            except Exception:
                self.gemini = None
    
    async def generate(self, prompt: str, provider: str = "auto", **kwargs) -> str:
        """Generate text using the specified or best available provider
        
        Args:
            prompt: Input prompt for text generation
            provider: Provider to use ("gemini", "auto")
            **kwargs: Additional parameters
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If no providers are available
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        
        # Auto-select provider if not specified
        if provider == "auto":
            if self.gemini:
                provider = "gemini"
            else:
                raise Exception("No LLM providers available")
        
        # Route to appropriate provider
        if provider == "gemini" and self.gemini:
            return await self.gemini.generate(prompt, **kwargs)
        else:
            raise Exception(f"Provider '{provider}' not available")
    
    def get_available_providers(self) -> list:
        """Get list of available providers
        
        Returns:
            List of available provider names
        """
        providers = []
        if self.gemini:
            providers.append("gemini")
        return providers 