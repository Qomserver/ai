import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.0-flash-exp"
    
    # Platform-specific settings
    INSTAGRAM_MAX_CAPTION_LENGTH = 2200
    TELEGRAM_MAX_MESSAGE_LENGTH = 4096
    WEBSITE_MAX_TITLE_LENGTH = 60
    WEBSITE_MAX_DESCRIPTION_LENGTH = 160
    
    # Content generation settings
    DEFAULT_TONE = "professional"
    DEFAULT_LANGUAGE = "persian"
    
    # SEO settings
    SEO_KEYWORDS_COUNT = 5
    SEO_DESCRIPTION_LENGTH = 155
    
    # Visual content suggestions
    IMAGE_STYLES = [
        "modern", "minimalist", "vibrant", "professional", 
        "creative", "elegant", "bold", "playful"
    ]
    
    VIDEO_DURATIONS = [15, 30, 60, 90, 120]
    
    # Hashtag settings
    MAX_HASHTAGS = 30
    MIN_HASHTAGS = 5