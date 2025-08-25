from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Dict, Any

from models import ContentRequest, ContentResponse
from content_generator import ContentGenerator
from config import Config

app = FastAPI(
    title="سیستم تولید محتوای هوش مصنوعی چندپلتفرمی",
    description="تولید محتوای بهینه برای اینستاگرام، تلگرام، وب‌سایت، ایتا و روبیکا",
    version="1.0.0"
)

# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ایجاد نمونه از تولیدکننده محتوا
content_generator = ContentGenerator()

@app.get("/", response_class=HTMLResponse)
async def root():
    """صفحه اصلی"""
    return """
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>سیستم تولید محتوای هوش مصنوعی</title>
        <style>
            body {
                font-family: 'Tahoma', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                color: #333;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 {
                text-align: center;
                color: #4a5568;
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            .platforms {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .platform {
                background: #f7fafc;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                border: 2px solid #e2e8f0;
                transition: all 0.3s ease;
            }
            .platform:hover {
                transform: translateY(-5px);
                border-color: #667eea;
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            }
            .platform h3 {
                color: #4a5568;
                margin: 0 0 10px 0;
            }
            .api-info {
                background: #edf2f7;
                padding: 20px;
                border-radius: 10px;
                margin: 30px 0;
            }
            .api-info h2 {
                color: #2d3748;
                margin-top: 0;
            }
            .endpoint {
                background: #2d3748;
                color: white;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                font-family: monospace;
            }
            .features {
                background: #f0fff4;
                padding: 20px;
                border-radius: 10px;
                margin: 30px 0;
            }
            .features h2 {
                color: #22543d;
                margin-top: 0;
            }
            .feature-list {
                list-style: none;
                padding: 0;
            }
            .feature-list li {
                padding: 8px 0;
                border-bottom: 1px solid #c6f6d5;
            }
            .feature-list li:before {
                content: "✅ ";
                margin-left: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 سیستم تولید محتوای هوش مصنوعی چندپلتفرمی</h1>
            
            <div class="platforms">
                <div class="platform">
                    <h3>📱 اینستاگرام</h3>
                    <p>کپشن‌های جذاب و هشتگ‌های بهینه</p>
                </div>
                <div class="platform">
                    <h3>💬 تلگرام</h3>
                    <p>محتویات کامل و مفصل</p>
                </div>
                <div class="platform">
                    <h3>🌐 وب‌سایت</h3>
                    <p>محتوای SEO-friendly</p>
                </div>
                <div class="platform">
                    <h3>📢 ایتا</h3>
                    <p>محتویات مناسب شبکه اجتماعی</p>
                </div>
                <div class="platform">
                    <h3>🎯 روبیکا</h3>
                    <p>محتوای بهینه برای الگوریتم جدید</p>
                </div>
            </div>
            
            <div class="api-info">
                <h2>🔌 API Endpoints</h2>
                <div class="endpoint">POST /generate-content</div>
                <p>تولید محتوای چندپلتفرمی</p>
                <div class="endpoint">GET /health</div>
                <p>بررسی وضعیت سیستم</p>
            </div>
            
            <div class="features">
                <h2>✨ ویژگی‌های کلیدی</h2>
                <ul class="feature-list">
                    <li>تولید محتوای اختصاصی برای هر پلتفرم</li>
                    <li>بهینه‌سازی SEO برای وب‌سایت</li>
                    <li>تولید هشتگ‌های مرتبط و موثر</li>
                    <li>پیشنهادات بصری (تصویر و ویدئو)</li>
                    <li>پشتیبانی از Function Calling Gemini</li>
                    <li>زمان‌بندی انتشار خودکار</li>
                    <li>ترجمه چندزبانه</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/generate-content", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """تولید محتوای چندپلتفرمی"""
    try:
        # بررسی وجود API Key
        if not Config.GEMINI_API_KEY:
            raise HTTPException(
                status_code=500, 
                detail="GEMINI_API_KEY تنظیم نشده است"
            )
        
        # تولید محتوا
        response = content_generator.generate_content(request)
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"خطا در تولید محتوا: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """بررسی وضعیت سیستم"""
    return {
        "status": "healthy",
        "service": "AI Content Generation System",
        "version": "1.0.0",
        "gemini_api_configured": bool(Config.GEMINI_API_KEY)
    }

@app.get("/platforms")
async def get_platforms():
    """دریافت لیست پلتفرم‌های پشتیبانی شده"""
    return {
        "platforms": [
            {
                "name": "instagram",
                "display_name": "اینستاگرام",
                "max_caption_length": Config.INSTAGRAM_MAX_CAPTION_LENGTH,
                "features": ["کپشن", "هشتگ", "اموجی", "CTA"]
            },
            {
                "name": "telegram",
                "display_name": "تلگرام",
                "max_message_length": Config.TELEGRAM_MAX_MESSAGE_LENGTH,
                "features": ["متن کامل", "هشتگ", "اموجی", "CTA"]
            },
            {
                "name": "website",
                "display_name": "وب‌سایت",
                "max_title_length": Config.WEBSITE_MAX_TITLE_LENGTH,
                "features": ["SEO", "هدینگ", "متاتگ", "کلمات کلیدی"]
            },
            {
                "name": "eitaa",
                "display_name": "ایتا",
                "features": ["متن کامل", "هشتگ", "اموجی", "CTA"]
            },
            {
                "name": "rubika",
                "display_name": "روبیکا",
                "features": ["متن کوتاه", "هشتگ", "اموجی", "CTA"]
            }
        ]
    }

@app.get("/tones")
async def get_tones():
    """دریافت لیست لحن‌های پشتیبانی شده"""
    return {
        "tones": [
            {"name": "professional", "display_name": "حرفه‌ای"},
            {"name": "friendly", "display_name": "دوستانه"},
            {"name": "casual", "display_name": "غیررسمی"},
            {"name": "formal", "display_name": "رسمی"},
            {"name": "creative", "display_name": "خلاقانه"},
            {"name": "inspirational", "display_name": "الهام‌بخش"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )