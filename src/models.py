"""
مدل‌های داده‌ای سیستم
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

from .platforms import PlatformType, ContentType, ToneType

class ContentRequest(BaseModel):
    """درخواست تولید محتوا"""
    topic: str = Field(..., description="موضوع اصلی محتوا")
    keywords: List[str] = Field(..., description="کلمات کلیدی")
    platforms: List[PlatformType] = Field(..., description="پلتفرم‌های هدف")
    content_type: ContentType = Field(default=ContentType.POST, description="نوع محتوا")
    tone: ToneType = Field(default=ToneType.FRIENDLY, description="لحن محتوا")
    target_audience: Optional[str] = Field(None, description="مخاطب هدف")
    language: str = Field(default="fa", description="زبان محتوا")
    additional_instructions: Optional[str] = Field(None, description="دستورات اضافی")
    
    @validator('keywords')
    def validate_keywords(cls, v):
        if not v or len(v) == 0:
            raise ValueError("حداقل یک کلمه کلیدی باید وارد شود")
        return v
    
    @validator('topic')
    def validate_topic(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError("موضوع باید حداقل ۳ کاراکتر باشد")
        return v.strip()

class PlatformContent(BaseModel):
    """محتوای تولید شده برای یک پلتفرم"""
    platform: PlatformType
    content: str
    hashtags: List[str] = Field(default_factory=list)
    mentions: List[str] = Field(default_factory=list)
    character_count: int = 0
    estimated_reading_time: Optional[int] = None  # بر حسب ثانیه
    engagement_score: Optional[float] = None  # امتیاز جذابیت پیش‌بینی شده
    
    class Config:
        use_enum_values = True

class ContentResponse(BaseModel):
    """پاسخ تولید محتوا"""
    contents: Dict[str, PlatformContent]
    hashtags: Dict[str, List[str]]  # هشتگ‌های پیشنهادی برای هر پلتفرم
    cta_suggestions: List[str]  # پیشنهادات فراخوان عمل
    generated_at: datetime
    request_id: str
    total_platforms: int = 0
    processing_time: Optional[float] = None  # زمان پردازش به ثانیه
    
    def __init__(self, **data):
        super().__init__(**data)
        self.total_platforms = len(self.contents)

class SEOOptimizationRequest(BaseModel):
    """درخواست بهینه‌سازی SEO"""
    text: str = Field(..., description="متن برای بهینه‌سازی")
    target_keywords: List[str] = Field(..., description="کلمات کلیدی هدف")
    focus_keyword: str = Field(..., description="کلمه کلیدی اصلی")
    meta_description: Optional[str] = Field(None, description="توضیحات متا")
    title_tag: Optional[str] = Field(None, description="عنوان صفحه")
    
    @validator('target_keywords')
    def validate_target_keywords(cls, v):
        if not v or len(v) == 0:
            raise ValueError("حداقل یک کلمه کلیدی هدف باید وارد شود")
        return v

class SEOOptimizationResponse(BaseModel):
    """پاسخ بهینه‌سازی SEO"""
    optimized_content: str
    seo_title: str
    meta_description: str
    keywords_density: Dict[str, float]
    headings_structure: List[Dict[str, Any]]
    seo_score: float  # امتیاز SEO از ۰ تا ۱۰۰
    recommendations: List[str]
    readability_score: float
    word_count: int
    
class VisualIdeaRequest(BaseModel):
    """درخواست تولید ایده بصری"""
    content: str = Field(..., description="محتوای متنی")
    platform: PlatformType = Field(..., description="پلتفرم هدف")
    content_type: ContentType = Field(default=ContentType.POST, description="نوع محتوا")
    style_preferences: Optional[List[str]] = Field(None, description="ترجیحات سبک")
    color_scheme: Optional[str] = Field(None, description="طرح رنگی")
    brand_guidelines: Optional[Dict[str, Any]] = Field(None, description="راهنمای برند")

class VisualIdeaResponse(BaseModel):
    """پاسخ تولید ایده بصری"""
    image_ideas: List[Dict[str, Any]]
    video_ideas: List[Dict[str, Any]]
    graphic_elements: List[str]
    color_suggestions: List[str]
    typography_suggestions: List[str]
    layout_suggestions: List[str]
    
class ScheduleRequest(BaseModel):
    """درخواست زمان‌بندی انتشار"""
    platform: PlatformType = Field(..., description="پلتفرم انتشار")
    content: str = Field(..., description="محتوای قابل انتشار")
    schedule_time: datetime = Field(..., description="زمان انتشار")
    auto_publish: bool = Field(default=False, description="انتشار خودکار")
    repeat_schedule: Optional[str] = Field(None, description="تکرار زمان‌بندی")
    tags: List[str] = Field(default_factory=list, description="برچسب‌ها")
    
    @validator('schedule_time')
    def validate_schedule_time(cls, v):
        if v <= datetime.now():
            raise ValueError("زمان انتشار باید در آینده باشد")
        return v

class ScheduledPost(BaseModel):
    """پست زمان‌بندی شده"""
    id: str
    platform: PlatformType
    content: str
    schedule_time: datetime
    status: str = "scheduled"  # scheduled, published, failed, cancelled
    created_at: datetime
    published_at: Optional[datetime] = None
    error_message: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True

class ContentAnalytics(BaseModel):
    """آنالیتیک محتوا"""
    platform: PlatformType
    content_id: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    engagement_rate: float = 0.0
    reach: int = 0
    impressions: int = 0
    click_through_rate: float = 0.0
    analyzed_at: datetime
    
    class Config:
        use_enum_values = True

class UserProfile(BaseModel):
    """پروفایل کاربر"""
    user_id: str
    username: str
    email: str
    preferred_platforms: List[PlatformType] = Field(default_factory=list)
    default_tone: ToneType = ToneType.FRIENDLY
    brand_voice: Optional[str] = None
    target_audience: Optional[str] = None
    industry: Optional[str] = None
    created_at: datetime
    last_active: datetime
    subscription_type: str = "free"  # free, premium, enterprise
    
    class Config:
        use_enum_values = True

class SystemStats(BaseModel):
    """آمار سیستم"""
    total_content_generated: int
    total_users: int
    popular_platforms: Dict[str, int]
    popular_content_types: Dict[str, int]
    average_engagement_score: float
    uptime_percentage: float
    last_updated: datetime