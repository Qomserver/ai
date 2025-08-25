from typing import Dict, Any, List, Optional
from models import ContentRequest, ContentResponse, Platform, PlatformContent, WebsiteContent, VisualSuggestion
from gemini_client import GeminiClient
from config import Config
import random

class ContentGenerator:
    def __init__(self):
        self.gemini_client = GeminiClient()
    
    def generate_content(self, request: ContentRequest) -> ContentResponse:
        """تولید محتوای چندپلتفرمی"""
        try:
            # تحلیل موضوع
            topic_analysis = self._analyze_topic(request)
            
            # تولید محتوا برای هر پلتفرم
            content_responses = {}
            
            if Platform.INSTAGRAM in request.platforms:
                content_responses['instagram'] = self._generate_instagram_content(request)
            
            if Platform.TELEGRAM in request.platforms:
                content_responses['telegram'] = self._generate_telegram_content(request)
            
            if Platform.WEBSITE in request.platforms:
                content_responses['website'] = self._generate_website_content(request)
            
            if Platform.EITAA in request.platforms:
                content_responses['eitaa'] = self._generate_eitaa_content(request)
            
            if Platform.RUBIKA in request.platforms:
                content_responses['rubika'] = self._generate_rubika_content(request)
            
            # تولید هشتگ‌ها
            hashtags = self._generate_hashtags(request.keywords, request.topic)
            
            # تولید ایده‌های بصری
            visual_suggestions = self._generate_visual_suggestions(request)
            
            # تولید پیشنهادات CTA
            cta_suggestions = self._generate_cta_suggestions(request.tone)
            
            # بهینه‌سازی SEO
            seo_optimization = None
            if request.include_seo and Platform.WEBSITE in request.platforms:
                seo_optimization = self._optimize_for_seo(request)
            
            return ContentResponse(
                topic_analysis=topic_analysis,
                instagram_content=content_responses.get('instagram'),
                telegram_content=content_responses.get('telegram'),
                website_content=content_responses.get('website'),
                eitaa_content=content_responses.get('eitaa'),
                rubika_content=content_responses.get('rubika'),
                hashtags=hashtags,
                visual_suggestions=visual_suggestions,
                cta_suggestions=cta_suggestions,
                seo_optimization=seo_optimization
            )
            
        except Exception as e:
            raise Exception(f"خطا در تولید محتوا: {str(e)}")
    
    def _analyze_topic(self, request: ContentRequest) -> Dict[str, Any]:
        """تحلیل موضوع و ایده‌پردازی"""
        prompt = f"""
        تحلیل موضوع: {request.topic}
        کلمات کلیدی: {', '.join(request.keywords)}
        مخاطب هدف: {request.target_audience}
        لحن: {request.tone}
        
        لطفاً تحلیل کاملی از موضوع ارائه دهید شامل:
        1. خلاصه موضوع
        2. نکات کلیدی
        3. ایده‌های خلاقانه
        4. زاویه‌های مختلف برای ارائه
        """
        
        response = self.gemini_client.generate_content(prompt)
        return {
            "analysis": response.get("text", ""),
            "key_points": self._extract_key_points(response.get("text", "")),
            "creative_angles": self._extract_creative_angles(response.get("text", ""))
        }
    
    def _generate_instagram_content(self, request: ContentRequest) -> Dict[str, str]:
        """تولید محتوای اینستاگرام"""
        prompt = f"""
        برای اینستاگرام محتوای جذاب تولید کنید:
        موضوع: {request.topic}
        لحن: {request.tone}
        مخاطب: {request.target_audience}
        
        شامل:
        1. کپشن جذاب (حداکثر 2200 کاراکتر)
        2. هشتگ‌های مرتبط
        3. اموجی‌های مناسب
        4. CTA موثر
        """
        
        response = self.gemini_client.generate_content(prompt)
        return {
            "caption": response.get("text", "")[:Config.INSTAGRAM_MAX_CAPTION_LENGTH],
            "hashtags": self._extract_hashtags(response.get("text", "")),
            "emojis": self._extract_emojis(response.get("text", "")),
            "cta": self._extract_cta(response.get("text", ""))
        }
    
    def _generate_telegram_content(self, request: ContentRequest) -> Dict[str, str]:
        """تولید محتوای تلگرام"""
        prompt = f"""
        برای تلگرام محتوای کامل و مفصل تولید کنید:
        موضوع: {request.topic}
        لحن: {request.tone}
        مخاطب: {request.target_audience}
        
        شامل:
        1. متن کامل و مفصل
        2. هشتگ‌های مرتبط
        3. اموجی‌های مناسب
        4. CTA موثر
        """
        
        response = self.gemini_client.generate_content(prompt)
        return {
            "content": response.get("text", ""),
            "hashtags": self._extract_hashtags(response.get("text", "")),
            "emojis": self._extract_emojis(response.get("text", "")),
            "cta": self._extract_cta(response.get("text", ""))
        }
    
    def _generate_website_content(self, request: ContentRequest) -> Dict[str, str]:
        """تولید محتوای وب‌سایت"""
        prompt = f"""
        برای وب‌سایت محتوای SEO-friendly تولید کنید:
        موضوع: {request.topic}
        کلمات کلیدی: {', '.join(request.keywords)}
        لحن: {request.tone}
        مخاطب: {request.target_audience}
        
        شامل:
        1. عنوان صفحه (حداکثر 60 کاراکتر)
        2. توضیحات متا (حداکثر 160 کاراکتر)
        3. محتوای اصلی با هدینگ‌های مناسب
        4. کلمات کلیدی SEO
        """
        
        response = self.gemini_client.generate_content(prompt)
        return {
            "title": self._extract_title(response.get("text", "")),
            "meta_description": self._extract_meta_description(response.get("text", "")),
            "content": response.get("text", ""),
            "headings": self._extract_headings(response.get("text", "")),
            "keywords": request.keywords
        }
    
    def _generate_eitaa_content(self, request: ContentRequest) -> Dict[str, str]:
        """تولید محتوای ایتا"""
        prompt = f"""
        برای ایتا محتوای مناسب تولید کنید:
        موضوع: {request.topic}
        لحن: {request.tone}
        مخاطب: {request.target_audience}
        
        شامل:
        1. متن کامل و جذاب
        2. هشتگ‌های مرتبط
        3. اموجی‌های مناسب
        4. CTA موثر
        """
        
        response = self.gemini_client.generate_content(prompt)
        return {
            "content": response.get("text", ""),
            "hashtags": self._extract_hashtags(response.get("text", "")),
            "emojis": self._extract_emojis(response.get("text", "")),
            "cta": self._extract_cta(response.get("text", ""))
        }
    
    def _generate_rubika_content(self, request: ContentRequest) -> Dict[str, str]:
        """تولید محتوای روبیکا"""
        prompt = f"""
        برای روبیکا محتوای بهینه تولید کنید:
        موضوع: {request.topic}
        لحن: {request.tone}
        مخاطب: {request.target_audience}
        
        شامل:
        1. متن جذاب و کوتاه
        2. هشتگ‌های مرتبط
        3. اموجی‌های مناسب
        4. CTA موثر
        """
        
        response = self.gemini_client.generate_content(prompt)
        return {
            "content": response.get("text", ""),
            "hashtags": self._extract_hashtags(response.get("text", "")),
            "emojis": self._extract_emojis(response.get("text", "")),
            "cta": self._extract_cta(response.get("text", ""))
        }
    
    def _generate_hashtags(self, keywords: List[str], topic: str) -> List[str]:
        """تولید هشتگ‌های پیشنهادی"""
        base_hashtags = [f"#{keyword.replace(' ', '')}" for keyword in keywords]
        
        # اضافه کردن هشتگ‌های مرتبط
        related_hashtags = [
            f"#{topic.replace(' ', '')}",
            "#محتوای_دیجیتال",
            "#بازاریابی_دیجیتال",
            "#شبکه_های_اجتماعی"
        ]
        
        all_hashtags = base_hashtags + related_hashtags
        return list(set(all_hashtags))[:Config.MAX_HASHTAGS]
    
    def _generate_visual_suggestions(self, request: ContentRequest) -> Dict[str, Any]:
        """تولید ایده‌های بصری"""
        image_style = random.choice(Config.IMAGE_STYLES)
        video_duration = random.choice(Config.VIDEO_DURATIONS)
        
        return {
            "image_style": image_style,
            "color_scheme": self._generate_color_scheme(image_style),
            "composition": self._generate_composition(image_style),
            "video_duration": video_duration,
            "video_style": self._generate_video_style(request.tone)
        }
    
    def _generate_cta_suggestions(self, tone: str) -> List[str]:
        """تولید پیشنهادات CTA"""
        cta_templates = {
            "professional": [
                "برای اطلاعات بیشتر با ما تماس بگیرید",
                "همین امروز شروع کنید",
                "درخواست مشاوره رایگان"
            ],
            "friendly": [
                "نظرتون چیه؟",
                "تجربه‌تون رو به اشتراک بگذارید",
                "سوالی دارید؟"
            ],
            "creative": [
                "ایده‌های جدید رو کشف کنید",
                "خلاقیت‌تون رو بروز بدید",
                "ماجراجویی رو شروع کنید"
            ]
        }
        
        return cta_templates.get(tone, cta_templates["professional"])
    
    def _optimize_for_seo(self, request: ContentRequest) -> Dict[str, str]:
        """بهینه‌سازی SEO"""
        prompt = f"""
        برای موضوع '{request.topic}' و کلمات کلیدی {', '.join(request.keywords)}:
        1. عنوان SEO بهینه (حداکثر 60 کاراکتر)
        2. توضیحات متا (حداکثر 160 کاراکتر)
        3. هدینگ‌های H1, H2, H3
        4. کلمات کلیدی اصلی
        """
        
        response = self.gemini_client.generate_content(prompt)
        return {
            "title": self._extract_title(response.get("text", "")),
            "meta_description": self._extract_meta_description(response.get("text", "")),
            "headings": self._extract_headings(response.get("text", "")),
            "keywords": request.keywords
        }
    
    # Helper methods for extracting content
    def _extract_key_points(self, text: str) -> List[str]:
        """استخراج نکات کلیدی از متن"""
        # این متد می‌تواند با NLP پیشرفته‌تر شود
        return [text[:100] + "..."] if text else []
    
    def _extract_creative_angles(self, text: str) -> List[str]:
        """استخراج زاویه‌های خلاقانه"""
        return [text[:100] + "..."] if text else []
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """استخراج هشتگ‌ها از متن"""
        import re
        hashtags = re.findall(r'#\w+', text)
        return hashtags[:10]
    
    def _extract_emojis(self, text: str) -> List[str]:
        """استخراج اموجی‌ها از متن"""
        import re
        emojis = re.findall(r'[^\w\s]', text)
        return emojis[:5]
    
    def _extract_cta(self, text: str) -> str:
        """استخراج CTA از متن"""
        cta_keywords = ["تماس", "شروع", "کلیک", "ببینید", "دانلود"]
        for keyword in cta_keywords:
            if keyword in text:
                return keyword
        return "بیشتر بدانید"
    
    def _extract_title(self, text: str) -> str:
        """استخراج عنوان از متن"""
        lines = text.split('\n')
        for line in lines:
            if line.strip() and len(line.strip()) <= 60:
                return line.strip()
        return text[:60] + "..."
    
    def _extract_meta_description(self, text: str) -> str:
        """استخراج توضیحات متا از متن"""
        return text[:160] + "..." if len(text) > 160 else text
    
    def _extract_headings(self, text: str) -> List[str]:
        """استخراج هدینگ‌ها از متن"""
        lines = text.split('\n')
        headings = []
        for line in lines:
            if line.strip().startswith('#') or line.strip().isupper():
                headings.append(line.strip())
        return headings[:5]
    
    def _generate_color_scheme(self, style: str) -> List[str]:
        """تولید رنگ‌بندی بر اساس سبک"""
        color_schemes = {
            "modern": ["#2C3E50", "#3498DB", "#ECF0F1"],
            "minimalist": ["#FFFFFF", "#000000", "#F5F5F5"],
            "vibrant": ["#E74C3C", "#F39C12", "#2ECC71"],
            "professional": ["#34495E", "#7F8C8D", "#BDC3C7"]
        }
        return color_schemes.get(style, ["#000000", "#FFFFFF"])
    
    def _generate_composition(self, style: str) -> str:
        """تولید ترکیب‌بندی بر اساس سبک"""
        compositions = {
            "modern": "ترکیب‌بندی متقارن با فضای سفید",
            "minimalist": "ترکیب‌بندی ساده و تمیز",
            "vibrant": "ترکیب‌بندی پویا و رنگی",
            "professional": "ترکیب‌بندی متعادل و حرفه‌ای"
        }
        return compositions.get(style, "ترکیب‌بندی استاندارد")
    
    def _generate_video_style(self, tone: str) -> str:
        """تولید سبک ویدئو بر اساس لحن"""
        video_styles = {
            "professional": "ویدئوی آموزشی با انیمیشن‌های ساده",
            "friendly": "ویدئوی تعاملی و دوستانه",
            "creative": "ویدئوی خلاقانه با افکت‌های ویژه"
        }
        return video_styles.get(tone, "ویدئوی استاندارد")