import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")
GEMINI_API_URL = os.getenv(
    "GEMINI_API_URL",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
) 