"""
تعریف پلتفرم‌ها و انواع محتوا
"""

from enum import Enum
from typing import Dict, List

class PlatformType(Enum):
    """انواع پلتفرم‌های پشتیبانی شده"""
    INSTAGRAM = "instagram"
    TELEGRAM = "telegram"
    WEBSITE = "website"
    EITAA = "eitaa"
    RUBIKA = "rubika"

class ContentType(Enum):
    """انواع محتوا"""
    POST = "post"
    STORY = "story"
    ARTICLE = "article"
    NEWS = "news"
    ADVERTISEMENT = "advertisement"
    VIDEO_SCRIPT = "video_script"
    CAROUSEL = "carousel"
    REEL_SCRIPT = "reel_script"

class ToneType(Enum):
    """انواع لحن"""
    FORMAL = "formal"
    INFORMAL = "informal"
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    HUMOROUS = "humorous"
    MOTIVATIONAL = "motivational"
    EDUCATIONAL = "educational"
    SALES = "sales"

# تنظیمات و محدودیت‌های هر پلتفرم
PLATFORM_CONFIGS = {
    PlatformType.INSTAGRAM: {
        "max_caption_length": 2200,
        "max_hashtags": 30,
        "supports_emojis": True,
        "supports_mentions": True,
        "line_breaks": True,
        "preferred_content_types": [
            ContentType.POST, 
            ContentType.STORY, 
            ContentType.CAROUSEL,
            ContentType.REEL_SCRIPT
        ],
        "hashtag_prefix": "#",
        "mention_prefix": "@",
        "best_posting_times": ["9:00", "12:00", "17:00", "20:00"],
        "character_encoding": "utf-8"
    },
    
    PlatformType.TELEGRAM: {
        "max_caption_length": 4096,
        "max_hashtags": None,  # بدون محدودیت
        "supports_emojis": True,
        "supports_mentions": True,
        "supports_markdown": True,
        "supports_html": True,
        "line_breaks": True,
        "preferred_content_types": [
            ContentType.POST, 
            ContentType.NEWS,
            ContentType.ARTICLE
        ],
        "hashtag_prefix": "#",
        "mention_prefix": "@",
        "best_posting_times": ["8:00", "13:00", "18:00", "21:00"],
        "character_encoding": "utf-8"
    },
    
    PlatformType.WEBSITE: {
        "max_caption_length": None,  # بدون محدودیت
        "supports_html": True,
        "supports_seo": True,
        "requires_headings": True,
        "requires_meta_tags": True,
        "preferred_content_types": [
            ContentType.ARTICLE,
            ContentType.NEWS
        ],
        "seo_requirements": {
            "title_max_length": 60,
            "meta_description_max_length": 160,
            "h1_required": True,
            "alt_text_required": True
        },
        "character_encoding": "utf-8"
    },
    
    PlatformType.EITAA: {
        "max_caption_length": 4096,
        "max_hashtags": 20,
        "supports_emojis": True,
        "supports_mentions": True,
        "line_breaks": True,
        "preferred_content_types": [
            ContentType.POST,
            ContentType.NEWS
        ],
        "hashtag_prefix": "#",
        "mention_prefix": "@",
        "best_posting_times": ["10:00", "14:00", "19:00", "22:00"],
        "character_encoding": "utf-8"
    },
    
    PlatformType.RUBIKA: {
        "max_caption_length": 4096,
        "max_hashtags": 15,
        "supports_emojis": True,
        "supports_mentions": True,
        "line_breaks": True,
        "preferred_content_types": [
            ContentType.POST,
            ContentType.NEWS
        ],
        "hashtag_prefix": "#",
        "mention_prefix": "@",
        "best_posting_times": ["11:00", "15:00", "20:00", "23:00"],
        "character_encoding": "utf-8"
    }
}

# قالب‌های محتوا برای هر پلتفرم
CONTENT_TEMPLATES = {
    PlatformType.INSTAGRAM: {
        ContentType.POST: """
{hook_line}

{main_content}

{cta_line}

{hashtags}
""",
        ContentType.STORY: """
{main_content}

{cta_text}
""",
        ContentType.CAROUSEL: """
اسلاید {slide_number}: {title}

{content}

{navigation_hint}
""",
        ContentType.REEL_SCRIPT: """
🎬 سکانس {scene_number}
⏱️ مدت: {duration} ثانیه

{scene_description}

متن روی صفحه: {overlay_text}
موزیک: {music_suggestion}
"""
    },
    
    PlatformType.TELEGRAM: {
        ContentType.POST: """
<b>{title}</b>

{main_content}

{cta_line}

{hashtags}
""",
        ContentType.NEWS: """
📰 <b>{news_title}</b>

{news_summary}

{full_content}

🔗 منبع: {source}
⏰ {publish_time}

{hashtags}
""",
        ContentType.ARTICLE: """
📝 <b>{article_title}</b>

{introduction}

{body_content}

<i>{conclusion}</i>

{hashtags}
"""
    },
    
    PlatformType.WEBSITE: {
        ContentType.ARTICLE: """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>{seo_title}</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{keywords}">
</head>
<body>
    <article>
        <h1>{main_title}</h1>
        {content_body}
    </article>
</body>
</html>
"""
    }
}

def get_platform_config(platform: PlatformType) -> Dict:
    """دریافت تنظیمات پلتفرم"""
    return PLATFORM_CONFIGS.get(platform, {})

def get_content_template(platform: PlatformType, content_type: ContentType) -> str:
    """دریافت قالب محتوا"""
    platform_templates = CONTENT_TEMPLATES.get(platform, {})
    return platform_templates.get(content_type, "{main_content}")

def get_platform_limitations(platform: PlatformType) -> Dict:
    """دریافت محدودیت‌های پلتفرم"""
    config = get_platform_config(platform)
    return {
        "max_caption_length": config.get("max_caption_length"),
        "max_hashtags": config.get("max_hashtags"),
        "supports_emojis": config.get("supports_emojis", False),
        "supports_mentions": config.get("supports_mentions", False)
    }