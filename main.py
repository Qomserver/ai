"""
سیستم تولید محتوای هوش مصنوعی چندپلتفرمی
نویسنده: AI Content Generator System
ورژن: 1.0.0
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import asyncio
import logging
from enum import Enum

# وارد کردن ماژول‌های سیستم
from src.content_generator import ContentGenerator
from src.seo_optimizer import SEOOptimizer
from src.visual_idea_generator import VisualIdeaGenerator
from src.scheduler import ContentScheduler
from src.platforms import PlatformType, ContentType
from src.models import (
    ContentRequest, ContentResponse, 
    ScheduleRequest, VisualIdeaRequest,
    SEOOptimizationRequest
)

# تنظیمات لاگ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ایجاد اپلیکیشن FastAPI
app = FastAPI(
    title="سیستم تولید محتوای هوش مصنوعی",
    description="سیستم جامع تولید محتوا برای پلتفرم‌های مختلف با قابلیت Function Calling",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ایجاد نمونه‌های کلاس‌ها
content_generator = ContentGenerator()
seo_optimizer = SEOOptimizer()
visual_idea_generator = VisualIdeaGenerator()
scheduler = ContentScheduler()

# تنظیم فایل‌های استاتیک و قالب‌ها
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """صفحه اصلی سیستم"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate-content", response_model=ContentResponse)
async def generate_content_api(request: ContentRequest):
    """
    تولید محتوا برای پلتفرم‌های مختلف
    
    Function: generate_content(platform, topic, keywords, tone)
    """
    try:
        logger.info(f"تولید محتوا برای موضوع: {request.topic}")
        
        # تولید محتوا برای هر پلتفرم
        contents = {}
        
        for platform in request.platforms:
            platform_content = await content_generator.generate_for_platform(
                platform=platform,
                topic=request.topic,
                keywords=request.keywords,
                tone=request.tone,
                target_audience=request.target_audience,
                content_type=request.content_type
            )
            contents[platform.value] = platform_content
        
        # تولید هشتگ‌ها
        hashtags = await content_generator.generate_hashtags(
            topic=request.topic,
            keywords=request.keywords,
            platforms=request.platforms
        )
        
        # تولید ایده‌های CTA
        cta_suggestions = await content_generator.generate_cta_suggestions(
            topic=request.topic,
            platforms=request.platforms,
            content_type=request.content_type
        )
        
        response = ContentResponse(
            contents=contents,
            hashtags=hashtags,
            cta_suggestions=cta_suggestions,
            generated_at=datetime.now(),
            request_id=f"req_{int(datetime.now().timestamp())}"
        )
        
        logger.info("محتوا با موفقیت تولید شد")
        return response
        
    except Exception as e:
        logger.error(f"خطا در تولید محتوا: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطا در تولید محتوا: {str(e)}")

@app.post("/api/optimize-seo")
async def optimize_for_seo_api(request: SEOOptimizationRequest):
    """
    بهینه‌سازی محتوا برای SEO
    
    Function: optimize_for_seo(text, target_keywords)
    """
    try:
        logger.info("شروع بهینه‌سازی SEO")
        
        optimized_content = await seo_optimizer.optimize_content(
            text=request.text,
            target_keywords=request.target_keywords,
            meta_description=request.meta_description,
            focus_keyword=request.focus_keyword
        )
        
        logger.info("بهینه‌سازی SEO با موفقیت انجام شد")
        return optimized_content
        
    except Exception as e:
        logger.error(f"خطا در بهینه‌سازی SEO: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطا در بهینه‌سازی SEO: {str(e)}")

@app.post("/api/generate-visual-idea")
async def generate_visual_idea_api(request: VisualIdeaRequest):
    """
    تولید ایده‌های بصری برای محتوا
    
    Function: generate_visual_idea(content)
    """
    try:
        logger.info("تولید ایده‌های بصری")
        
        visual_ideas = await visual_idea_generator.generate_ideas(
            content=request.content,
            platform=request.platform,
            content_type=request.content_type,
            style_preferences=request.style_preferences
        )
        
        logger.info("ایده‌های بصری با موفقیت تولید شدند")
        return visual_ideas
        
    except Exception as e:
        logger.error(f"خطا در تولید ایده‌های بصری: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطا در تولید ایده‌های بصری: {str(e)}")

@app.post("/api/schedule-post")
async def schedule_post_api(request: ScheduleRequest, background_tasks: BackgroundTasks):
    """
    زمان‌بندی انتشار محتوا
    
    Function: schedule_post(platform, datetime)
    """
    try:
        logger.info(f"زمان‌بندی انتشار برای {request.platform.value}")
        
        schedule_id = await scheduler.schedule_content(
            platform=request.platform,
            content=request.content,
            schedule_time=request.schedule_time,
            auto_publish=request.auto_publish
        )
        
        # اضافه کردن به تسک‌های پس‌زمینه
        if request.auto_publish:
            background_tasks.add_task(
                scheduler.execute_scheduled_post,
                schedule_id
            )
        
        logger.info(f"محتوا با شناسه {schedule_id} زمان‌بندی شد")
        return {
            "message": "محتوا با موفقیت زمان‌بندی شد",
            "schedule_id": schedule_id,
            "scheduled_time": request.schedule_time
        }
        
    except Exception as e:
        logger.error(f"خطا در زمان‌بندی: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطا در زمان‌بندی: {str(e)}")

@app.get("/api/scheduled-posts")
async def get_scheduled_posts():
    """دریافت لیست پست‌های زمان‌بندی شده"""
    try:
        scheduled_posts = await scheduler.get_scheduled_posts()
        return scheduled_posts
    except Exception as e:
        logger.error(f"خطا در دریافت پست‌های زمان‌بندی شده: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/scheduled-posts/{schedule_id}")
async def cancel_scheduled_post(schedule_id: str):
    """لغو پست زمان‌بندی شده"""
    try:
        result = await scheduler.cancel_scheduled_post(schedule_id)
        return result
    except Exception as e:
        logger.error(f"خطا در لغو پست: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/platforms")
async def get_supported_platforms():
    """دریافت لیست پلتفرم‌های پشتیبانی شده"""
    return {
        "platforms": [platform.value for platform in PlatformType],
        "content_types": [content_type.value for content_type in ContentType]
    }

@app.get("/api/stats")
async def get_system_stats():
    """آمار سیستم"""
    try:
        stats = {
            "total_generated_contents": await content_generator.get_total_generated(),
            "scheduled_posts_count": await scheduler.get_scheduled_count(),
            "active_platforms": len(PlatformType),
            "system_uptime": datetime.now() - app.state.start_time if hasattr(app.state, 'start_time') else None
        }
        return stats
    except Exception as e:
        logger.error(f"خطا در دریافت آمار: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    """رویداد راه‌اندازی اپلیکیشن"""
    app.state.start_time = datetime.now()
    logger.info("🚀 سیستم تولید محتوای هوش مصنوعی راه‌اندازی شد")
    
    # راه‌اندازی scheduler
    await scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    """رویداد خاموش شدن اپلیکیشن"""
    logger.info("⛔ سیستم در حال خاموش شدن...")
    await scheduler.stop()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )