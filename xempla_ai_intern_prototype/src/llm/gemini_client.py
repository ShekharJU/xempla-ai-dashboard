"""
Gemini LLM Client for Xempla AI Systems Intern Prototype

Provides async HTTP client for Google's Gemini API.
"""
import os
import httpx
import asyncio
from typing import Dict, Any, Optional
from .base import BaseLLMClient
from ..utils.retry import async_retry

# Default configuration
DEFAULT_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

class GeminiClient(BaseLLMClient):
    """Async HTTP client for Google's Gemini API"""
    
    def __init__(self, api_key: str = DEFAULT_GEMINI_API_KEY, api_url: str = DEFAULT_GEMINI_API_URL):
        """Initialize Gemini client
        
        Args:
            api_key: Gemini API key
            api_url: Gemini API endpoint URL
        """
        if not api_key:
            raise ValueError("Gemini API key is required")
        
        self.api_key = api_key
        self.api_url = api_url

    @async_retry(retries=3, delay=2)
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using Gemini API
        
        Args:
            prompt: Input prompt for text generation
            **kwargs: Additional parameters for the API call
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If API call fails
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            **kwargs
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url, 
                json=payload, 
                headers=headers, 
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract text from Gemini API response
            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if len(parts) > 0 and "text" in parts[0]:
                        return parts[0]["text"]
            
            # Fallback response
            return "No response generated"
    
    async def generate_with_context(self, prompt: str, context: Dict[str, Any], **kwargs) -> str:
        """Generate text with additional context
        
        Args:
            prompt: Input prompt
            context: Additional context information
            **kwargs: Additional parameters
            
        Returns:
            Generated text response
        """
        # Combine prompt with context
        context_str = f"Context: {context}\n\nPrompt: {prompt}"
        return await self.generate(context_str, **kwargs) 