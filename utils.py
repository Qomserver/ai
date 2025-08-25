# توابع کمکی برای سیستم تولید محتوا

def clean_text(text):
    """پاک‌سازی متن از کاراکترهای اضافی"""
    return text.strip() if text else ""

def extract_hashtags(text):
    """استخراج هشتگ‌ها از متن"""
    import re
    return re.findall(r'#\w+', text) if text else []

def extract_emojis(text):
    """استخراج اموجی‌ها از متن"""
    import re
    emojis = re.findall(r'[^\w\s]', text)
    return emojis[:5] if emojis else []

def calculate_read_time(text, words_per_minute=200):
    """محاسبه زمان مطالعه متن (به دقیقه)"""
    if not text:
        return 0
    word_count = len(text.split())
    return max(1, word_count // words_per_minute)
