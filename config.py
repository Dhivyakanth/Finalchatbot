import os

class Config:
    @staticmethod
    def validate_api_key():
        api_key = os.getenv("GEMINI_API_KEY")
        return bool(api_key and api_key.strip()) 