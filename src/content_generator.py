"""
تولیدکننده محتوا برای پلتفرم‌های مختلف
"""

import asyncio
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from .platforms import (
    PlatformType, ContentType, ToneType,
    get_platform_config, get_content_template,
    PLATFORM_CONFIGS
)
from .models import PlatformContent

logger = logging.getLogger(__name__)

class ContentGenerator:
    """کلاس اصلی تولید محتوا"""
    
    def __init__(self):
        self.generated_count = 0
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, Any]:
        """بارگذاری قالب‌های محتوا"""
        return {
            "instagram_hooks": [
                "آیا می‌دانستید که...",
                "راز موفقیت در...",
                "۵ نکته طلایی برای...",
                "چرا باید...",
                "بهترین روش برای...",
                "اگر می‌خواهید...",
                "سوالی که همه می‌پرسند:",
                "حقیقتی که کمتر می‌دانند:",
            ],
            
            "cta_templates": {
                PlatformType.INSTAGRAM: [
                    "نظرتون رو در کامنت بنویسید 👇",
                    "این پست رو ذخیره کنید 💾",
                    "با دوستاتون به اشتراک بگذارید 🔄",
                    "برای محتوای بیشتر فالو کنید 🔔",
                    "در استوری نشانمون بدید 📱"
                ],
                PlatformType.TELEGRAM: [
                    "نظرات خود را در گروه مطرح کنید",
                    "این پیام را فوروارد کنید",
                    "به کانال ما بپیوندید",
                    "لینک را با دوستان خود به اشتراک بگذارید",
                    "برای اطلاعات بیشتر کلیک کنید"
                ],
                PlatformType.WEBSITE: [
                    "مطالعه بیشتر مقالات مرتبط",
                    "عضویت در خبرنامه",
                    "دانلود راهنمای رایگان",
                    "تماس با کارشناسان ما",
                    "درخواست مشاوره رایگان"
                ]
            },
            
            "hashtag_categories": {
                "عمومی": ["محتوا", "آموزش", "اطلاعات", "مفید", "جالب"],
                "تکنولوژی": ["تکنولوژی", "نوآوری", "دیجیتال", "آینده"],
                "کسب_و_کار": ["کسب_و_کار", "موفقیت", "استارتاپ", "کارآفرینی"],
                "سبک_زندگی": ["سبک_زندگی", "سلامت", "تناسب_اندام", "آرامش"],
                "آموزش": ["آموزش", "یادگیری", "مهارت", "توسعه_فردی"]
            }
        }
    
    async def generate_for_platform(
        self,
        platform: PlatformType,
        topic: str,
        keywords: List[str],
        tone: ToneType,
        target_audience: Optional[str] = None,
        content_type: ContentType = ContentType.POST
    ) -> PlatformContent:
        """تولید محتوا برای یک پلتفرم خاص"""
        
        logger.info(f"تولید محتوا برای {platform.value} - موضوع: {topic}")
        
        # دریافت تنظیمات پلتفرم
        config = get_platform_config(platform)
        template = get_content_template(platform, content_type)
        
        # تولید محتوای اصلی
        main_content = await self._generate_main_content(
            topic=topic,
            keywords=keywords,
            tone=tone,
            platform=platform,
            content_type=content_type,
            target_audience=target_audience
        )
        
        # اعمال قالب
        formatted_content = await self._apply_template(
            content=main_content,
            template=template,
            platform=platform,
            topic=topic
        )
        
        # تولید هشتگ‌ها
        hashtags = await self._generate_platform_hashtags(
            keywords=keywords,
            platform=platform,
            topic=topic
        )
        
        # محاسبه آمار
        char_count = len(formatted_content)
        reading_time = self._estimate_reading_time(formatted_content)
        engagement_score = await self._calculate_engagement_score(
            content=formatted_content,
            platform=platform,
            hashtags=hashtags
        )
        
        # اعمال محدودیت‌های پلتفرم
        if config.get("max_caption_length"):
            formatted_content = self._truncate_content(
                formatted_content, 
                config["max_caption_length"]
            )
        
        self.generated_count += 1
        
        return PlatformContent(
            platform=platform,
            content=formatted_content,
            hashtags=hashtags,
            character_count=char_count,
            estimated_reading_time=reading_time,
            engagement_score=engagement_score
        )
    
    async def _generate_main_content(
        self,
        topic: str,
        keywords: List[str],
        tone: ToneType,
        platform: PlatformType,
        content_type: ContentType,
        target_audience: Optional[str] = None
    ) -> str:
        """تولید محتوای اصلی"""
        
        # شخصی‌سازی بر اساس لحن
        tone_adjustments = {
            ToneType.FORMAL: "لطفاً به شیوه‌ای رسمی و حرفه‌ای",
            ToneType.INFORMAL: "به شکل صمیمی و دوستانه",
            ToneType.FRIENDLY: "با لحنی گرم و دوستانه",
            ToneType.PROFESSIONAL: "با رویکرد کاملاً حرفه‌ای",
            ToneType.HUMOROUS: "با طنز مناسب و شوخ‌طبعی",
            ToneType.MOTIVATIONAL: "با انگیزه‌دهی و انرژی مثبت",
            ToneType.EDUCATIONAL: "به شیوه آموزشی و توضیحی",
            ToneType.SALES: "با رویکرد فروشی اما نه تهاجمی"
        }
        
        # تولید محتوا بر اساس نوع
        if content_type == ContentType.POST:
            content = await self._generate_post_content(topic, keywords, tone_adjustments.get(tone, ""))
        elif content_type == ContentType.STORY:
            content = await self._generate_story_content(topic, keywords)
        elif content_type == ContentType.ARTICLE:
            content = await self._generate_article_content(topic, keywords, tone_adjustments.get(tone, ""))
        elif content_type == ContentType.NEWS:
            content = await self._generate_news_content(topic, keywords)
        elif content_type == ContentType.VIDEO_SCRIPT:
            content = await self._generate_video_script(topic, keywords)
        else:
            content = await self._generate_default_content(topic, keywords, tone_adjustments.get(tone, ""))
        
        return content
    
    async def _generate_post_content(self, topic: str, keywords: List[str], tone_instruction: str) -> str:
        """تولید محتوای پست"""
        
        # الگوریتم تولید محتوای هوشمند
        # در اینجا می‌توانید از API های مختلف AI استفاده کنید
        
        content_structure = {
            "hook": f"موضوع جذاب درباره {topic}",
            "body": f"محتوای اصلی که کلمات کلیدی {', '.join(keywords)} را شامل می‌شود",
            "value": "ارزش و فایده برای مخاطب",
            "conclusion": "جمع‌بندی و نتیجه‌گیری"
        }
        
        # ترکیب محتوا
        content = f"""
{content_structure['hook']}

{content_structure['body']}

💡 {content_structure['value']}

{content_structure['conclusion']}
""".strip()
        
        return content
    
    async def _generate_story_content(self, topic: str, keywords: List[str]) -> str:
        """تولید محتوای استوری"""
        return f"📱 {topic}\n\n{' '.join(keywords[:3])}"
    
    async def _generate_article_content(self, topic: str, keywords: List[str], tone_instruction: str) -> str:
        """تولید محتوای مقاله"""
        return f"""
# {topic}

## مقدمه
در این مقاله به بررسی {topic} می‌پردازیم.

## بخش اصلی
محتوای مفصل درباره {', '.join(keywords)}.

## نتیجه‌گیری
خلاصه و جمع‌بندی مطالب.
"""
    
    async def _generate_news_content(self, topic: str, keywords: List[str]) -> str:
        """تولید محتوای خبری"""
        return f"""
🗞️ خبر: {topic}

📍 خلاصه خبر مربوط به {', '.join(keywords[:3])}

📊 جزئیات و اطلاعات تکمیلی

🔗 منابع معتبر
"""
    
    async def _generate_video_script(self, topic: str, keywords: List[str]) -> str:
        """تولید اسکریپت ویدئو"""
        return f"""
🎬 اسکریپت ویدئو: {topic}

[سکانس 1 - معرفی]
سلام و معرفی موضوع {topic}

[سکانس 2 - محتوای اصلی]
توضیح درباره {', '.join(keywords)}

[سکانس 3 - خاتمه]
جمع‌بندی و تشکر از بینندگان
"""
    
    async def _generate_default_content(self, topic: str, keywords: List[str], tone_instruction: str) -> str:
        """تولید محتوای پیش‌فرض"""
        return f"{tone_instruction} درباره {topic} و مرتبط با {', '.join(keywords)} محتوایی تولید کنید."
    
    async def _apply_template(
        self, 
        content: str, 
        template: str, 
        platform: PlatformType,
        topic: str
    ) -> str:
        """اعمال قالب به محتوا"""
        
        # جایگزینی متغیرها در قالب
        formatted_content = template.format(
            main_content=content,
            hook_line=self._get_random_hook(),
            title=topic,
            cta_line=self._get_random_cta(platform),
            hashtags="",  # هشتگ‌ها جداگانه اضافه می‌شوند
            publish_time=datetime.now().strftime("%Y/%m/%d - %H:%M")
        )
        
        return formatted_content.strip()
    
    def _get_random_hook(self) -> str:
        """انتخاب تصادفی hook"""
        import random
        hooks = self.templates["instagram_hooks"]
        return random.choice(hooks)
    
    def _get_random_cta(self, platform: PlatformType) -> str:
        """انتخاب تصادفی CTA"""
        import random
        ctas = self.templates["cta_templates"].get(platform, ["عملکرد انجام دهید"])
        return random.choice(ctas)
    
    async def _generate_platform_hashtags(
        self, 
        keywords: List[str], 
        platform: PlatformType, 
        topic: str
    ) -> List[str]:
        """تولید هشتگ‌های مناسب برای پلتفرم"""
        
        config = get_platform_config(platform)
        max_hashtags = config.get("max_hashtags", 10)
        
        hashtags = []
        
        # هشتگ‌های مبتنی بر کلمات کلیدی
        for keyword in keywords:
            hashtag = self._clean_hashtag(keyword)
            if hashtag:
                hashtags.append(f"#{hashtag}")
        
        # هشتگ‌های مرتبط با موضوع
        topic_hashtags = self._generate_topic_hashtags(topic)
        hashtags.extend(topic_hashtags)
        
        # هشتگ‌های عمومی پلتفرم
        general_hashtags = self._get_general_hashtags(platform)
        hashtags.extend(general_hashtags[:3])
        
        # حذف تکراری و محدود کردن تعداد
        unique_hashtags = list(dict.fromkeys(hashtags))
        
        if max_hashtags:
            unique_hashtags = unique_hashtags[:max_hashtags]
        
        return unique_hashtags
    
    def _clean_hashtag(self, text: str) -> str:
        """تمیز کردن متن برای هشتگ"""
        # حذف کاراکترهای غیرمجاز
        cleaned = re.sub(r'[^\w\u0600-\u06FF]', '', text)
        return cleaned if len(cleaned) > 1 else None
    
    def _generate_topic_hashtags(self, topic: str) -> List[str]:
        """تولید هشتگ‌های مرتبط با موضوع"""
        words = topic.split()
        hashtags = []
        
        for word in words:
            cleaned = self._clean_hashtag(word)
            if cleaned and len(cleaned) > 2:
                hashtags.append(f"#{cleaned}")
        
        return hashtags[:5]
    
    def _get_general_hashtags(self, platform: PlatformType) -> List[str]:
        """دریافت هشتگ‌های عمومی پلتفرم"""
        general_tags = {
            PlatformType.INSTAGRAM: ["#اینستاگرام", "#محتوا", "#ایران"],
            PlatformType.TELEGRAM: ["#تلگرام", "#اطلاعات", "#مفید"],
            PlatformType.EITAA: ["#ایتا", "#داخلی", "#ایرانی"],
            PlatformType.RUBIKA: ["#روبیکا", "#پیام_رسان"]
        }
        return general_tags.get(platform, [])
    
    def _estimate_reading_time(self, content: str) -> int:
        """تخمین زمان مطالعه (ثانیه)"""
        words_count = len(content.split())
        # میانگین سرعت خواندن فارسی: ۱۵۰ کلمه در دقیقه
        reading_time_minutes = words_count / 150
        return int(reading_time_minutes * 60)
    
    async def _calculate_engagement_score(
        self, 
        content: str, 
        platform: PlatformType, 
        hashtags: List[str]
    ) -> float:
        """محاسبه امتیاز جذابیت پیش‌بینی شده"""
        
        score = 0.0
        
        # طول مناسب
        length = len(content)
        if platform == PlatformType.INSTAGRAM:
            if 100 <= length <= 500:
                score += 2.0
        elif platform == PlatformType.TELEGRAM:
            if 50 <= length <= 1000:
                score += 2.0
        
        # تعداد هشتگ
        hashtag_count = len(hashtags)
        if 5 <= hashtag_count <= 15:
            score += 1.5
        
        # وجود ایموجی
        emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', content))
        if emoji_count > 0:
            score += 1.0
        
        # وجود سوال
        if '؟' in content:
            score += 0.5
        
        # وجود فراخوان عمل
        cta_keywords = ['کامنت', 'ذخیره', 'اشتراک', 'فالو', 'کلیک']
        if any(keyword in content for keyword in cta_keywords):
            score += 1.0
        
        return min(score, 10.0)  # حداکثر ۱۰
    
    def _truncate_content(self, content: str, max_length: int) -> str:
        """کوتاه کردن محتوا در صورت تجاوز از حد مجاز"""
        if len(content) <= max_length:
            return content
        
        # کوتاه کردن با حفظ کلمات
        truncated = content[:max_length-3]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    async def generate_hashtags(
        self, 
        topic: str, 
        keywords: List[str], 
        platforms: List[PlatformType]
    ) -> Dict[str, List[str]]:
        """تولید هشتگ‌ها برای همه پلتفرم‌ها"""
        
        all_hashtags = {}
        
        for platform in platforms:
            hashtags = await self._generate_platform_hashtags(keywords, platform, topic)
            all_hashtags[platform.value] = hashtags
        
        return all_hashtags
    
    async def generate_cta_suggestions(
        self, 
        topic: str, 
        platforms: List[PlatformType],
        content_type: ContentType
    ) -> List[str]:
        """تولید پیشنهادات فراخوان عمل"""
        
        suggestions = []
        
        for platform in platforms:
            platform_ctas = self.templates["cta_templates"].get(platform, [])
            suggestions.extend(platform_ctas[:2])  # دو پیشنهاد از هر پلتفرم
        
        # حذف تکراری
        unique_suggestions = list(dict.fromkeys(suggestions))
        
        return unique_suggestions[:10]  # حداکثر ۱۰ پیشنهاد
    
    async def get_total_generated(self) -> int:
        """دریافت تعداد کل محتواهای تولید شده"""
        return self.generated_count