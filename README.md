# 🚀 سیستم تولید محتوای هوش مصنوعی چندپلتفرمی

یک سیستم پیشرفته تولید محتوا که با استفاده از **Gemini 2.5 Flash** و قابلیت **Function Calling**، محتوای بهینه برای چندین پلتفرم تولید می‌کند.

## ✨ ویژگی‌های کلیدی

- 🎯 **تولید محتوای چندپلتفرمی**: اینستاگرام، تلگرام، وب‌سایت، ایتا، روبیکا
- 🤖 **هوش مصنوعی پیشرفته**: استفاده از Gemini 2.5 Flash
- 🔧 **Function Calling**: پشتیبانی از فراخوانی توابع
- 📱 **بهینه‌سازی پلتفرم**: محتوای اختصاصی برای هر شبکه اجتماعی
- 🔍 **SEO بهینه**: بهینه‌سازی محتوای وب‌سایت
- 🎨 **پیشنهادات بصری**: ایده‌های تصویر و ویدئو
- ⏰ **زمان‌بندی خودکار**: انتشار خودکار محتوا
- 🌐 **API کامل**: RESTful API برای یکپارچه‌سازی

## 🏗️ معماری سیستم

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │───▶│ Content Generator│───▶│ Gemini Client   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  API Manager   │    │   Scheduler      │    │  Function Call  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│ Social Media    │    │   Content DB     │
│    APIs        │    │                  │
└─────────────────┘    └──────────────────┘
```

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8+
- Gemini API Key
- pip

### نصب

1. **کلون کردن مخزن**
```bash
git clone <repository-url>
cd ai-content-generator
```

2. **نصب وابستگی‌ها**
```bash
pip install -r requirements.txt
```

3. **تنظیم متغیرهای محیطی**
```bash
cp .env.example .env
# فایل .env را ویرایش کرده و API Key خود را اضافه کنید
```

4. **اجرای سیستم**
```bash
python main.py
```

5. **دسترسی به سیستم**
```
http://localhost:8000
```

## 📚 راهنمای استفاده

### API Endpoints

#### تولید محتوا
```http
POST /generate-content
Content-Type: application/json

{
  "topic": "بازاریابی دیجیتال در سال 2024",
  "keywords": ["بازاریابی دیجیتال", "شبکه‌های اجتماعی"],
  "target_audience": "کارآفرینان",
  "tone": "professional",
  "platforms": ["instagram", "telegram", "website"],
  "language": "persian",
  "include_visual_suggestions": true,
  "include_seo": true
}
```

#### بررسی وضعیت سیستم
```http
GET /health
```

#### دریافت پلتفرم‌های پشتیبانی شده
```http
GET /platforms
```

### مثال استفاده با Python

```python
import requests

# تولید محتوا
response = requests.post("http://localhost:8000/generate-content", json={
    "topic": "هوش مصنوعی در کسب‌وکار",
    "keywords": ["هوش مصنوعی", "کسب‌وکار", "دیجیتال"],
    "target_audience": "مدیران ارشد",
    "tone": "professional",
    "platforms": ["instagram", "website"],
    "language": "persian"
})

content = response.json()
print(f"محتوای اینستاگرام: {content['instagram_content']['caption']}")
```

### مثال استفاده با cURL

```bash
curl -X POST "http://localhost:8000/generate-content" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "تست سیستم",
    "keywords": ["تست", "سیستم"],
    "target_audience": "توسعه‌دهندگان",
    "tone": "friendly",
    "platforms": ["telegram"],
    "language": "persian"
  }'
```

## 🔧 تنظیمات پیشرفته

### تنظیم API Keys

```bash
# فایل .env
GEMINI_API_KEY=your_gemini_api_key
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
TELEGRAM_BOT_TOKEN=your_telegram_token
```

### تنظیمات پلتفرم‌ها

هر پلتفرم تنظیمات خاص خود را دارد:

- **اینستاگرام**: حداکثر 2200 کاراکتر در کپشن
- **تلگرام**: متن کامل بدون محدودیت
- **وب‌سایت**: بهینه‌سازی SEO
- **ایتا**: محتوای شبکه اجتماعی
- **روبیکا**: محتوای بهینه برای الگوریتم جدید

## 🎨 قالب‌های محتوا

### اینستاگرام
- کپشن جذاب و کوتاه
- هشتگ‌های مرتبط
- اموجی‌های مناسب
- CTA موثر

### تلگرام
- متن کامل و مفصل
- هشتگ‌های مرتبط
- اموجی‌های مناسب
- CTA موثر

### وب‌سایت
- عنوان SEO بهینه
- توضیحات متا
- محتوای اصلی با هدینگ‌ها
- کلمات کلیدی

## 🔍 Function Calling

سیستم از قابلیت Function Calling Gemini استفاده می‌کند:

```python
# تعریف توابع
functions = [
    {
        "name": "generate_content",
        "description": "تولید محتوای متناسب با پلتفرم",
        "parameters": {...}
    },
    {
        "name": "optimize_for_seo",
        "description": "بهینه‌سازی SEO",
        "parameters": {...}
    }
]
```

## 📊 تست سیستم

```bash
# اجرای تست‌های کامل
python test_system.py

# تست ساده
python simple_test.py

# تست تولید محتوا
python -c "
from content_generator import ContentGenerator
generator = ContentGenerator()
# تست کد...
"
```

## 🚀 استقرار

### Docker

```bash
# ساخت و اجرای کانتینر
docker build -t ai-content-generator .
docker run -p 8000:8000 ai-content-generator
```

### Docker Compose

```bash
# اجرا با Docker Compose
docker-compose up -d
```

## 🔒 امنیت

- استفاده از متغیرهای محیطی برای API Keys
- اعتبارسنجی ورودی‌ها
- محدودیت نرخ درخواست
- CORS تنظیم شده

## 📈 عملکرد

- تولید محتوا در کمتر از 10 ثانیه
- پشتیبانی از 5 پلتفرم همزمان
- قابلیت تولید انبوه محتوا
- بهینه‌سازی خودکار

## 🤝 مشارکت

1. Fork کنید
2. Branch جدید ایجاد کنید (`git checkout -b feature/amazing-feature`)
3. تغییرات را commit کنید (`git commit -m 'Add amazing feature'`)
4. Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request ایجاد کنید

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات بیشتر فایل `LICENSE` را مطالعه کنید.

## 📞 پشتیبانی

- 📧 ایمیل: support@example.com
- 💬 تلگرام: @support_channel
- 🐛 Issues: GitHub Issues
- 📚 مستندات: Wiki

## 🙏 تشکر

از تمامی افرادی که در توسعه این پروژه مشارکت داشته‌اند تشکر می‌کنیم.

---

**نکته**: این سیستم برای استفاده تجاری و شخصی طراحی شده است. لطفاً قوانین و محدودیت‌های پلتفرم‌های مختلف را رعایت کنید.
