"""
تولیدکننده ایده‌های بصری برای محتوا
"""

import asyncio
import random
from typing import Dict, List, Any, Optional
import logging

from .platforms import PlatformType, ContentType

logger = logging.getLogger(__name__)

class VisualIdeaGenerator:
    """کلاس تولید ایده‌های بصری"""
    
    def __init__(self):
        self.visual_templates = self._load_visual_templates()
        self.color_palettes = self._load_color_palettes()
        self.design_trends = self._load_design_trends()
    
    def _load_visual_templates(self) -> Dict[str, Any]:
        """بارگذاری قالب‌های بصری"""
        return {
            "image_styles": {
                "minimalist": "طراحی مینیمال با فضای خالی زیاد",
                "colorful": "طراحی رنگارنگ و پر انرژی",
                "professional": "طراحی حرفه‌ای و جدی",
                "modern": "طراحی مدرن با خطوط تمیز",
                "vintage": "طراحی کلاسیک و قدیمی",
                "geometric": "طراحی هندسی با اشکال منظم",
                "organic": "طراحی طبیعی با فرم‌های ارگانیک",
                "gradient": "طراحی با گرادیان‌های زیبا"
            },
            
            "layout_types": {
                "single_focus": "یک عنصر اصلی در مرکز",
                "grid": "چیدمان شبکه‌ای منظم",
                "asymmetric": "چیدمان نامتقارن و پویا",
                "layered": "لایه‌بندی عمق‌دار",
                "split_screen": "تقسیم صفحه به دو بخش",
                "circular": "چیدمان دایره‌ای",
                "diagonal": "خطوط مورب و پویا",
                "frame": "استفاده از قاب و مرز"
            },
            
            "typography_styles": {
                "bold_headers": "عناوین ضخیم و چشمگیر",
                "script_fonts": "فونت‌های دست‌نویس",
                "modern_sans": "فونت‌های مدرن بدون سریف",
                "classic_serif": "فونت‌های کلاسیک با سریف",
                "display_fonts": "فونت‌های نمایشی خاص",
                "minimal_text": "حداقل متن با تأکید بر بصری"
            },
            
            "content_elements": {
                "icons": "آیکون‌های مناسب موضوع",
                "illustrations": "تصاویر وکتوری سفارشی",
                "photos": "عکس‌های با کیفیت",
                "graphics": "گرافیک‌های اطلاعاتی",
                "patterns": "الگوها و بافت‌ها",
                "charts": "نمودارها و آمار",
                "quotes": "نقل قول‌های بصری",
                "logos": "لوگو و نمادها"
            }
        }
    
    def _load_color_palettes(self) -> Dict[str, List[str]]:
        """بارگذاری پالت‌های رنگی"""
        return {
            "warm": ["#FF6B35", "#F7931E", "#FFD23F", "#FFF1D0"],
            "cool": ["#06BCC1", "#0F4C75", "#3282B8", "#BBE1FA"],
            "natural": ["#2F5233", "#81A684", "#C7E9B0", "#F4F9E7"],
            "professional": ["#2C3E50", "#34495E", "#95A5A6", "#ECF0F1"],
            "vibrant": ["#E74C3C", "#9B59B6", "#3498DB", "#1ABC9C"],
            "pastel": ["#FFC3A0", "#FFAFCC", "#BDE0FF", "#A8E6CF"],
            "monochrome": ["#000000", "#333333", "#666666", "#999999", "#CCCCCC", "#FFFFFF"],
            "sunset": ["#FF7F7F", "#FFBF7F", "#FFDF7F", "#FFFF7F"],
            "ocean": ["#000080", "#0066CC", "#4DA6FF", "#99CCFF"],
            "earth": ["#8B4513", "#CD853F", "#DEB887", "#F5DEB3"]
        }
    
    def _load_design_trends(self) -> Dict[str, str]:
        """بارگذاری ترندهای طراحی"""
        return {
            "glassmorphism": "افکت شیشه‌ای و شفافیت",
            "neumorphism": "طراحی soft UI با سایه نرم",
            "dark_mode": "حالت تاریک با کنتراست بالا",
            "3d_elements": "عناصر سه‌بعدی و عمق",
            "abstract_shapes": "اشکال انتزاعی و هندسی",
            "hand_drawn": "عناصر دست‌کشیده و طبیعی",
            "vintage_retro": "طراحی وینتیج و رترو",
            "minimalist_brutalism": "مینیمالیسم با عناصر قوی"
        }
    
    async def generate_ideas(
        self,
        content: str,
        platform: PlatformType,
        content_type: ContentType = ContentType.POST,
        style_preferences: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """تولید ایده‌های بصری برای محتوا"""
        
        logger.info(f"تولید ایده‌های بصری برای {platform.value}")
        
        # تحلیل محتوا برای استخراج موضوع
        content_analysis = await self._analyze_content_theme(content)
        
        # تولید ایده‌های تصویری
        image_ideas = await self._generate_image_ideas(
            content_analysis, platform, content_type, style_preferences
        )
        
        # تولید ایده‌های ویدئویی
        video_ideas = await self._generate_video_ideas(
            content_analysis, platform, content_type
        )
        
        # پیشنهاد عناصر گرافیکی
        graphic_elements = await self._suggest_graphic_elements(
            content_analysis, platform
        )
        
        # پیشنهاد رنگ‌ها
        color_suggestions = await self._suggest_colors(
            content_analysis, style_preferences
        )
        
        # پیشنهاد تایپوگرافی
        typography_suggestions = await self._suggest_typography(
            platform, content_type
        )
        
        # پیشنهاد چیدمان
        layout_suggestions = await self._suggest_layouts(
            platform, content_type, content_analysis
        )
        
        return {
            "image_ideas": image_ideas,
            "video_ideas": video_ideas,
            "graphic_elements": graphic_elements,
            "color_suggestions": color_suggestions,
            "typography_suggestions": typography_suggestions,
            "layout_suggestions": layout_suggestions,
            "generated_at": "now",
            "platform_optimized": True
        }
    
    async def _analyze_content_theme(self, content: str) -> Dict[str, Any]:
        """تحلیل محتوا برای تشخیص موضوع و حس‌وحال"""
        
        # کلمات کلیدی موضوعی
        themes = {
            "technology": ["تکنولوژی", "فناوری", "دیجیتال", "نرم‌افزار", "هوش مصنوعی"],
            "business": ["کسب‌وکار", "بازاریابی", "فروش", "درآمد", "موفقیت"],
            "health": ["سلامت", "تناسب اندام", "تغذیه", "ورزش", "درمان"],
            "lifestyle": ["سبک زندگی", "زیبایی", "مد", "آرایش", "دکوراسیون"],
            "education": ["آموزش", "یادگیری", "مهارت", "دانش", "توسعه"],
            "travel": ["سفر", "گردشگری", "مکان", "شهر", "کشور"],
            "food": ["غذا", "آشپزی", "رستوران", "طعم", "دستپخت"],
            "entertainment": ["سرگرمی", "فیلم", "موسیقی", "بازی", "تفریح"]
        }
        
        # تشخیص موضوع اصلی
        detected_theme = "general"
        max_matches = 0
        
        content_lower = content.lower()
        for theme, keywords in themes.items():
            matches = sum(1 for keyword in keywords if keyword in content_lower)
            if matches > max_matches:
                max_matches = matches
                detected_theme = theme
        
        # تحلیل حس‌وحال
        mood = self._detect_mood(content)
        
        # استخراج کلمات کلیدی بصری
        visual_keywords = self._extract_visual_keywords(content)
        
        return {
            "theme": detected_theme,
            "mood": mood,
            "visual_keywords": visual_keywords,
            "content_length": len(content),
            "has_numbers": bool(any(char.isdigit() for char in content)),
            "has_questions": "؟" in content
        }
    
    def _detect_mood(self, content: str) -> str:
        """تشخیص حس‌وحال محتوا"""
        
        positive_words = ["خوب", "عالی", "موفق", "بهترین", "زیبا", "شاد", "مثبت"]
        negative_words = ["بد", "مشکل", "ناراحت", "غمگین", "منفی", "سخت"]
        energetic_words = ["انرژی", "هیجان", "پویا", "سریع", "قوی", "پرقدرت"]
        calm_words = ["آرام", "آرامش", "صلح", "نرم", "ملایم", "ساکت"]
        
        content_lower = content.lower()
        
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        energetic_count = sum(1 for word in energetic_words if word in content_lower)
        calm_count = sum(1 for word in calm_words if word in content_lower)
        
        if energetic_count > 0:
            return "energetic"
        elif calm_count > 0:
            return "calm"
        elif positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "serious"
        else:
            return "neutral"
    
    def _extract_visual_keywords(self, content: str) -> List[str]:
        """استخراج کلمات کلیدی بصری"""
        
        visual_words = [
            "رنگ", "نور", "تصویر", "طراحی", "شکل", "فرم", "خط", "نقطه",
            "دایره", "مربع", "مثلث", "منحنی", "زاویه", "سایه", "برجستگی"
        ]
        
        found_keywords = []
        content_lower = content.lower()
        
        for word in visual_words:
            if word in content_lower:
                found_keywords.append(word)
        
        return found_keywords[:5]  # حداکثر ۵ کلمه
    
    async def _generate_image_ideas(
        self,
        content_analysis: Dict,
        platform: PlatformType,
        content_type: ContentType,
        style_preferences: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """تولید ایده‌های تصویری"""
        
        ideas = []
        theme = content_analysis["theme"]
        mood = content_analysis["mood"]
        
        # انتخاب سبک بر اساس ترجیحات یا موضوع
        if style_preferences:
            styles = style_preferences
        else:
            styles = self._get_theme_appropriate_styles(theme, mood)
        
        # تولید ایده‌ها برای هر سبک
        for style in styles[:3]:  # حداکثر ۳ سبک
            idea = {
                "style": style,
                "description": self.visual_templates["image_styles"].get(
                    style, "سبک خاص"
                ),
                "elements": self._get_style_elements(style, theme),
                "layout": self._get_recommended_layout(platform, content_type),
                "focal_point": self._get_focal_point_suggestion(content_analysis),
                "color_mood": self._map_mood_to_colors(mood),
                "composition_tips": self._get_composition_tips(platform, style)
            }
            
            ideas.append(idea)
        
        return ideas
    
    def _get_theme_appropriate_styles(self, theme: str, mood: str) -> List[str]:
        """انتخاب سبک‌های مناسب برای موضوع"""
        
        theme_styles = {
            "technology": ["modern", "geometric", "gradient"],
            "business": ["professional", "minimalist", "modern"],
            "health": ["organic", "colorful", "minimalist"],
            "lifestyle": ["colorful", "vintage", "organic"],
            "education": ["professional", "modern", "colorful"],
            "travel": ["colorful", "vintage", "organic"],
            "food": ["colorful", "organic", "vintage"],
            "entertainment": ["colorful", "gradient", "modern"]
        }
        
        mood_styles = {
            "energetic": ["colorful", "gradient", "geometric"],
            "calm": ["minimalist", "organic", "professional"],
            "positive": ["colorful", "modern", "gradient"],
            "serious": ["professional", "minimalist", "modern"],
            "neutral": ["modern", "professional", "geometric"]
        }
        
        # ترکیب پیشنهادات
        suggested_styles = list(set(
            theme_styles.get(theme, ["modern"]) + 
            mood_styles.get(mood, ["professional"])
        ))
        
        return suggested_styles[:3]
    
    def _get_style_elements(self, style: str, theme: str) -> List[str]:
        """دریافت عناصر مناسب برای سبک"""
        
        style_elements = {
            "minimalist": ["فضای خالی زیاد", "رنگ‌های کم", "خطوط ساده"],
            "colorful": ["رنگ‌های پررنگ", "کنتراست بالا", "عناصر متنوع"],
            "professional": ["رنگ‌های خنثی", "فونت‌های ساده", "چیدمان منظم"],
            "modern": ["خطوط تمیز", "گرادیان‌ها", "فضای منفی"],
            "vintage": ["بافت قدیمی", "رنگ‌های کم‌اشباع", "فونت‌های کلاسیک"],
            "geometric": ["اشکال هندسی", "خطوط راست", "تقارن"],
            "organic": ["اشکال طبیعی", "منحنی‌ها", "رنگ‌های زمینی"],
            "gradient": ["تدریج رنگ", "انتقال نرم", "عمق بصری"]
        }
        
        return style_elements.get(style, ["عناصر استاندارد"])
    
    def _get_recommended_layout(self, platform: PlatformType, content_type: ContentType) -> str:
        """پیشنهاد چیدمان بر اساس پلتفرم"""
        
        platform_layouts = {
            PlatformType.INSTAGRAM: {
                ContentType.POST: "single_focus",
                ContentType.STORY: "layered",
                ContentType.CAROUSEL: "grid"
            },
            PlatformType.TELEGRAM: {
                ContentType.POST: "asymmetric",
                ContentType.NEWS: "frame"
            },
            PlatformType.WEBSITE: {
                ContentType.ARTICLE: "split_screen"
            }
        }
        
        return platform_layouts.get(platform, {}).get(content_type, "single_focus")
    
    def _get_focal_point_suggestion(self, content_analysis: Dict) -> str:
        """پیشنهاد نقطه کانونی"""
        
        if content_analysis["has_numbers"]:
            return "آمار و اعداد در مرکز"
        elif content_analysis["has_questions"]:
            return "سوال به عنوان عنصر اصلی"
        elif content_analysis["theme"] == "business":
            return "لوگو یا نماد کسب‌وکار"
        else:
            return "متن اصلی یا تصویر نماد"
    
    def _map_mood_to_colors(self, mood: str) -> str:
        """نگاشت حس‌وحال به رنگ‌ها"""
        
        mood_colors = {
            "energetic": "warm",
            "calm": "cool", 
            "positive": "vibrant",
            "serious": "professional",
            "neutral": "monochrome"
        }
        
        return mood_colors.get(mood, "natural")
    
    def _get_composition_tips(self, platform: PlatformType, style: str) -> List[str]:
        """نکات ترکیب‌بندی"""
        
        platform_tips = {
            PlatformType.INSTAGRAM: [
                "نسبت ۱:۱ برای فید",
                "متن خوانا روی تصویر",
                "رنگ‌های جذاب برای توجه"
            ],
            PlatformType.TELEGRAM: [
                "کیفیت بالا برای نمایش",
                "متن کمتر روی تصویر",
                "ابعاد مناسب برای موبایل"
            ]
        }
        
        return platform_tips.get(platform, ["کیفیت بالا", "خوانایی مناسب"])
    
    async def _generate_video_ideas(
        self,
        content_analysis: Dict,
        platform: PlatformType,
        content_type: ContentType
    ) -> List[Dict[str, Any]]:
        """تولید ایده‌های ویدئویی"""
        
        video_ideas = []
        theme = content_analysis["theme"]
        
        # انواع ویدئوهای مناسب
        video_types = self._get_video_types_for_theme(theme)
        
        for video_type in video_types[:3]:
            idea = {
                "type": video_type,
                "duration": self._get_optimal_duration(platform, video_type),
                "style": self._get_video_style(theme, video_type),
                "shots": self._generate_shot_list(video_type, content_analysis),
                "music_suggestion": self._suggest_music(theme, video_type),
                "text_overlay": self._suggest_text_overlay(platform, content_analysis),
                "transitions": self._suggest_transitions(video_type),
                "color_grading": self._suggest_color_grading(theme)
            }
            
            video_ideas.append(idea)
        
        return video_ideas
    
    def _get_video_types_for_theme(self, theme: str) -> List[str]:
        """انواع ویدئوی مناسب برای موضوع"""
        
        theme_videos = {
            "technology": ["demo", "animation", "timelapse"],
            "business": ["presentation", "interview", "infographic"],
            "health": ["tutorial", "transformation", "lifestyle"],
            "lifestyle": ["aesthetic", "day_in_life", "tutorial"],
            "education": ["tutorial", "animation", "presentation"],
            "travel": ["cinematic", "timelapse", "aesthetic"],
            "food": ["recipe", "aesthetic", "timelapse"],
            "entertainment": ["fun", "animation", "compilation"]
        }
        
        return theme_videos.get(theme, ["presentation", "tutorial", "aesthetic"])
    
    def _get_optimal_duration(self, platform: PlatformType, video_type: str) -> str:
        """مدت زمان بهینه ویدئو"""
        
        platform_durations = {
            PlatformType.INSTAGRAM: {
                "story": "15 ثانیه",
                "reel": "30 ثانیه", 
                "post": "60 ثانیه"
            },
            PlatformType.TELEGRAM: "2-5 دقیقه"
        }
        
        if platform == PlatformType.INSTAGRAM:
            if video_type in ["fun", "aesthetic"]:
                return "15-30 ثانیه"
            else:
                return "60-90 ثانیه"
        
        return "1-3 دقیقه"
    
    def _get_video_style(self, theme: str, video_type: str) -> str:
        """سبک ویدئو"""
        
        styles = {
            "technology": "مدرن و تمیز",
            "business": "حرفه‌ای و جدی",
            "health": "طبیعی و انرژی‌بخش",
            "lifestyle": "زیبا و جذاب",
            "education": "واضح و آموزشی"
        }
        
        return styles.get(theme, "متنوع و جذاب")
    
    def _generate_shot_list(self, video_type: str, content_analysis: Dict) -> List[str]:
        """لیست شات‌های پیشنهادی"""
        
        shot_types = {
            "tutorial": [
                "نمای کلی از موضوع",
                "نزدیک‌شدن به جزئیات",
                "مراحل گام‌به‌گام",
                "نتیجه نهایی"
            ],
            "aesthetic": [
                "نمای زیبا از موضوع اصلی",
                "جزئیات با فوکوس نرم",
                "حرکت آرام دوربین",
                "نمای نهایی جذاب"
            ],
            "presentation": [
                "معرفی موضوع",
                "نکات کلیدی با گرافیک",
                "مثال‌های عملی",
                "خلاصه و نتیجه‌گیری"
            ]
        }
        
        return shot_types.get(video_type, ["شات ابتدایی", "محتوای اصلی", "پایان"])
    
    def _suggest_music(self, theme: str, video_type: str) -> str:
        """پیشنهاد موسیقی"""
        
        music_suggestions = {
            "technology": "الکترونیک آرام یا آمبیانت",
            "business": "موسیقی انگیزشی یا کلاسیک",
            "health": "موسیقی آرام و طبیعی",
            "lifestyle": "موسیقی شاد و مدرن",
            "education": "موسیقی ملایم و تمرکزی"
        }
        
        return music_suggestions.get(theme, "موسیقی مناسب موضوع")
    
    def _suggest_text_overlay(self, platform: PlatformType, content_analysis: Dict) -> List[str]:
        """پیشنهاد متن روی ویدئو"""
        
        suggestions = ["عنوان اصلی در ابتدا"]
        
        if content_analysis["has_numbers"]:
            suggestions.append("نمایش آمار کلیدی")
        
        if content_analysis["has_questions"]:
            suggestions.append("نمایش سوال مهم")
        
        suggestions.append("فراخوان عمل در پایان")
        
        return suggestions
    
    def _suggest_transitions(self, video_type: str) -> List[str]:
        """پیشنهاد ترانزیشن‌ها"""
        
        transitions = {
            "tutorial": ["برش ساده", "فید کردن", "حرکت صاف"],
            "aesthetic": ["تدریج نرم", "حرکت آهسته", "انتقال روان"],
            "presentation": ["برش سریع", "اسلاید", "زوم"]
        }
        
        return transitions.get(video_type, ["برش ساده", "تدریج نرم"])
    
    def _suggest_color_grading(self, theme: str) -> str:
        """پیشنهاد رنگ‌بندی"""
        
        grading = {
            "technology": "رنگ‌های سرد و مدرن",
            "business": "رنگ‌های خنثی و حرفه‌ای",
            "health": "رنگ‌های گرم و طبیعی",
            "lifestyle": "رنگ‌های روشن و شاد",
            "education": "رنگ‌های متعادل و آرام"
        }
        
        return grading.get(theme, "رنگ‌بندی طبیعی")
    
    async def _suggest_graphic_elements(
        self, content_analysis: Dict, platform: PlatformType
    ) -> List[str]:
        """پیشنهاد عناصر گرافیکی"""
        
        elements = []
        theme = content_analysis["theme"]
        
        # عناصر اساسی بر اساس موضوع
        theme_elements = {
            "technology": ["آیکون‌های فنی", "خطوط دیجیتال", "نمودارها"],
            "business": ["گراف‌ها", "نمادهای پولی", "آیکون‌های کسب‌وکار"],
            "health": ["نمادهای پزشکی", "المان‌های طبیعی", "نمودار پیشرفت"],
            "lifestyle": ["آیکون‌های زیبایی", "نقوش تزیینی", "فریم‌های زیبا"],
            "education": ["آیکون‌های آموزشی", "نمودارها", "فلش‌های راهنما"]
        }
        
        elements.extend(theme_elements.get(theme, ["آیکون‌های عمومی"]))
        
        # عناصر بر اساس پلتفرم
        platform_elements = {
            PlatformType.INSTAGRAM: ["فریم استوری", "استیکرها", "GIF"],
            PlatformType.TELEGRAM: ["ایموجی", "مارک‌داون", "لینک پیش‌نمایش"]
        }
        
        elements.extend(platform_elements.get(platform, []))
        
        return elements
    
    async def _suggest_colors(
        self, content_analysis: Dict, style_preferences: Optional[List[str]] = None
    ) -> List[str]:
        """پیشنهاد رنگ‌ها"""
        
        mood = content_analysis["mood"]
        theme = content_analysis["theme"]
        
        # انتخاب پالت بر اساس حس‌وحال
        mood_palette = self._map_mood_to_colors(mood)
        suggested_colors = self.color_palettes[mood_palette]
        
        # اضافه کردن رنگ‌های موضوعی
        theme_colors = {
            "technology": ["#007ACC", "#FF6B35", "#36A2EB"],
            "business": ["#2C3E50", "#E74C3C", "#F39C12"],
            "health": ["#27AE60", "#E67E22", "#3498DB"],
            "lifestyle": ["#E91E63", "#9C27B0", "#FF9800"],
            "education": ["#3F51B5", "#009688", "#FF5722"]
        }
        
        if theme in theme_colors:
            suggested_colors.extend(theme_colors[theme])
        
        # حذف تکراری و محدود کردن
        unique_colors = list(dict.fromkeys(suggested_colors))
        
        return unique_colors[:6]  # حداکثر ۶ رنگ
    
    async def _suggest_typography(
        self, platform: PlatformType, content_type: ContentType
    ) -> List[str]:
        """پیشنهاد تایپوگرافی"""
        
        typography_rules = {
            PlatformType.INSTAGRAM: {
                ContentType.POST: ["فونت‌های ضخیم برای عنوان", "حداکثر ۳ سایز مختلف"],
                ContentType.STORY: ["فونت‌های بزرگ و خوانا", "کنتراست بالا"]
            },
            PlatformType.TELEGRAM: ["فونت‌های ساده", "اندازه متوسط", "خوانایی بالا"],
            PlatformType.WEBSITE: ["فونت‌های وب‌سیف", "هیرارشی واضح", "تناسب موبایل"]
        }
        
        suggestions = typography_rules.get(platform, {})
        if isinstance(suggestions, dict):
            suggestions = suggestions.get(content_type, ["فونت‌های استاندارد"])
        
        # اضافه کردن نکات عمومی
        general_tips = [
            "استفاده از فونت‌های فارسی مناسب",
            "رعایت فاصله خطوط",
            "تناسب اندازه با محتوا"
        ]
        
        if isinstance(suggestions, list):
            suggestions.extend(general_tips)
        else:
            suggestions = general_tips
        
        return suggestions[:5]
    
    async def _suggest_layouts(
        self, 
        platform: PlatformType, 
        content_type: ContentType,
        content_analysis: Dict
    ) -> List[str]:
        """پیشنهاد چیدمان"""
        
        suggestions = []
        
        # چیدمان بر اساس پلتفرم
        platform_layouts = {
            PlatformType.INSTAGRAM: {
                ContentType.POST: [
                    "متن بالا، تصویر پایین",
                    "تصویر پس‌زمینه با متن روی آن",
                    "تقسیم به سه بخش افقی"
                ],
                ContentType.STORY: [
                    "متن در وسط صفحه",
                    "تصویر پس‌زمینه با متن بالا",
                    "چیدمان عمودی"
                ]
            },
            PlatformType.TELEGRAM: [
                "متن بالا، تصویر پایین",
                "تصویر کوچک کنار متن",
                "گالری تصاویر"
            ]
        }
        
        platform_suggestion = platform_layouts.get(platform, {})
        if isinstance(platform_suggestion, dict):
            suggestions = platform_suggestion.get(content_type, [])
        else:
            suggestions = platform_suggestion
        
        # اضافه کردن پیشنهادات بر اساس محتوا
        if content_analysis["has_numbers"]:
            suggestions.append("نمایش برجسته آمار و اعداد")
        
        if content_analysis["has_questions"]:
            suggestions.append("قرار دادن سوال در مکان کانونی")
        
        return suggestions[:4]