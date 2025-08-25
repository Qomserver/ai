from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class Platform(str, Enum):
    INSTAGRAM = "instagram"
    TELEGRAM = "telegram"
    WEBSITE = "website"
    EITAA = "eitaa"
    RUBIKA = "rubika"

class Tone(str, Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    CASUAL = "casual"
    FORMAL = "formal"
    CREATIVE = "creative"
    INSPIRATIONAL = "inspirational"

class ContentRequest(BaseModel):
    topic: str = Field(..., description="موضوع اصلی محتوا")
    keywords: List[str] = Field(..., description="کلمات کلیدی")
    target_audience: str = Field(..., description="مخاطب هدف")
    tone: Tone = Field(default=Tone.PROFESSIONAL, description="لحن محتوا")
    platforms: List[Platform] = Field(..., description="پلتفرم‌های هدف")
    language: str = Field(default="persian", description="زبان محتوا")
    include_visual_suggestions: bool = Field(default=True, description="شامل پیشنهادات بصری")
    include_seo: bool = Field(default=False, description="شامل بهینه‌سازی SEO")

class ContentResponse(BaseModel):
    topic_analysis: Dict[str, Any] = Field(..., description="تحلیل موضوع")
    instagram_content: Optional[Dict[str, str]] = Field(None, description="محتوای اینستاگرام")
    telegram_content: Optional[Dict[str, str]] = Field(None, description="محتوای تلگرام")
    website_content: Optional[Dict[str, str]] = Field(None, description="محتوای وب‌سایت")
    eitaa_content: Optional[Dict[str, str]] = Field(None, description="محتوای ایتا")
    rubika_content: Optional[Dict[str, str]] = Field(None, description="محتوای روبیکا")
    hashtags: List[str] = Field(..., description="هشتگ‌های پیشنهادی")
    visual_suggestions: Dict[str, Any] = Field(..., description="پیشنهادات بصری")
    cta_suggestions: List[str] = Field(..., description="پیشنهادات CTA")
    seo_optimization: Optional[Dict[str, str]] = Field(None, description="بهینه‌سازی SEO")

class PlatformContent(BaseModel):
    caption: str = Field(..., description="متن اصلی")
    hashtags: List[str] = Field(..., description="هشتگ‌ها")
    emojis: List[str] = Field(..., description="اموجی‌ها")
    cta: str = Field(..., description="فراخوان به عمل")

class WebsiteContent(BaseModel):
    title: str = Field(..., description="عنوان صفحه")
    meta_description: str = Field(..., description="توضیحات متا")
    content: str = Field(..., description="محتوای اصلی")
    headings: List[str] = Field(..., description="سرتیترها")
    keywords: List[str] = Field(..., description="کلمات کلیدی SEO")

class VisualSuggestion(BaseModel):
    image_style: str = Field(..., description="سبک تصویر")
    color_scheme: List[str] = Field(..., description="رنگ‌بندی")
    composition: str = Field(..., description="ترکیب‌بندی")
    video_duration: Optional[int] = Field(None, description="مدت ویدئو")
    video_style: Optional[str] = Field(None, description="سبک ویدئو")