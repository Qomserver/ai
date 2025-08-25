# 🤖 سیستم تولید محتوای هوش مصنوعی چندپلتفرمی

یک سیستم جامع و حرفه‌ای برای تولید محتوای بهینه شده برای پلتفرم‌های مختلف با استفاده از هوش مصنوعی و قابلیت‌های پیشرفته Function Calling.

## ✨ ویژگی‌های کلیدی

### 🎯 تولید محتوای چندپلتفرمی
- **اینستاگرام**: پست‌ها، استوری‌ها، کروسل‌ها و اسکریپت Reel
- **تلگرام**: پست‌ها، اخبار و مقالات با پشتیبانی HTML/Markdown
- **وب‌سایت**: مقالات SEO-friendly با ساختار استاندارد
- **ایتا**: محتوای بهینه شده برای پیام‌رسان داخلی
- **روبیکا**: محتوا متناسب با الگوریتم پلتفرم

### 🧠 قابلیت‌های هوشمند
- **تحلیل موضوع**: شناسایی خودکار تم و حس‌وحال محتوا
- **بهینه‌سازی SEO**: تحلیل و بهبود خودکار برای موتورهای جستجو
- **تولید ایده‌های بصری**: پیشنهاد طراحی، رنگ‌بندی و چیدمان
- **زمان‌بندی هوشمند**: انتشار خودکار در بهترین زمان‌ها
- **آنالیتیک پیشرفته**: ردیابی عملکرد و آمار تفصیلی

### 🔧 Function Calling
- `generate_content(platform, topic, keywords, tone)`: تولید محتوا
- `optimize_for_seo(text, target_keywords)`: بهینه‌سازی SEO
- `generate_visual_idea(content)`: تولید ایده‌های بصری
- `schedule_post(platform, datetime)`: زمان‌بندی انتشار

## 🚀 راه‌اندازی سریع

### نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### اجرای سرور
```bash
python main.py
```

سرور روی `http://localhost:8000` راه‌اندازی می‌شود.

### دسترسی به رابط کاربری
مرورگر خود را باز کرده و به آدرس بالا بروید.

### مشاهده مستندات API
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📝 نحوه استفاده

### 1. تولید محتوا از طریق API

```python
import requests

payload = {
    "topic": "فواید یادگیری هوش مصنوعی",
    "keywords": ["هوش مصنوعی", "یادگیری ماشین", "فناوری"],
    "platforms": ["instagram", "telegram", "website"],
    "content_type": "post",
    "tone": "educational",
    "target_audience": "دانشجویان"
}

response = requests.post("http://localhost:8000/api/generate-content", json=payload)
result = response.json()
```

### 2. بهینه‌سازی SEO

```python
seo_payload = {
    "text": "متن مقاله شما...",
    "target_keywords": ["کلمه کلیدی 1", "کلمه کلیدی 2"],
    "focus_keyword": "کلمه کلیدی اصلی"
}

response = requests.post("http://localhost:8000/api/optimize-seo", json=seo_payload)
```

### 3. زمان‌بندی انتشار

```python
from datetime import datetime, timedelta

schedule_payload = {
    "platform": "instagram",
    "content": "محتوای شما...",
    "schedule_time": (datetime.now() + timedelta(hours=2)).isoformat(),
    "auto_publish": True
}

response = requests.post("http://localhost:8000/api/schedule-post", json=schedule_payload)
```

## 🏗️ معماری سیستم

```
📁 workspace/
├── 📄 main.py                 # سرور اصلی FastAPI
├── 📁 src/                    # ماژول‌های اصلی
│   ├── 📄 __init__.py
│   ├── 📄 platforms.py        # تعاریف پلتفرم‌ها
│   ├── 📄 models.py          # مدل‌های داده
│   ├── 📄 content_generator.py # تولیدکننده محتوا
│   ├── 📄 seo_optimizer.py   # بهینه‌ساز SEO
│   ├── 📄 visual_idea_generator.py # تولید ایده‌های بصری
│   └── 📄 scheduler.py       # زمان‌بندی انتشار
├── 📁 templates/             # قالب‌های HTML
│   └── 📄 index.html
├── 📁 static/               # فایل‌های استاتیک
│   ├── 📁 css/
│   ├── 📁 js/
│   └── 📁 images/
├── 📁 examples/             # نمونه‌های کاربرد
│   └── 📄 sample_requests.py
└── 📄 requirements.txt      # وابستگی‌ها
```

## 🎨 ویژگی‌های رابط کاربری

### طراحی مدرن و ریسپانسیو
- **ظاهر زیبا**: طراحی مدرن با گرادیان‌ها و انیمیشن‌ها
- **فونت فارسی**: استفاده از فونت Vazir برای نمایش بهتر
- **داکمود**: پشتیبانی از حالت تاریک
- **موبایل**: بهینه‌سازی کامل برای دستگاه‌های همراه

### تجربه کاربری بهینه
- **لودینگ هوشمند**: نمایش وضعیت پردازش
- **کپی آسان**: کپی محتوا با یک کلیک
- **ذخیره‌سازی**: دانلود نتایج به فرمت JSON
- **کیبورد شورتکات**: میانبرهای کلیدی برای سرعت بیشتر

## 📊 ماژول‌های تخصصی

### ContentGenerator
تولید محتوای هوشمند با ویژگی‌های:
- تحلیل موضوع و مخاطب
- انتخاب لحن مناسب
- تولید هشتگ‌های بهینه
- پیشنهاد CTA مؤثر

### SEOOptimizer
بهینه‌سازی پیشرفته شامل:
- تحلیل تراکم کلمات کلیدی
- بررسی ساختار هدینگ‌ها
- محاسبه امتیاز خوانایی
- پیشنهادات بهبود

### VisualIdeaGenerator
تولید ایده‌های خلاقانه:
- پیشنهاد پالت رنگی
- ایده‌های طراحی
- چیدمان بصری
- اسکریپت ویدئو

### ContentScheduler
زمان‌بندی پیشرفته:
- انتشار خودکار
- زمان‌بندی تکراری
- مدیریت صف انتشار
- آمار عملکرد

## 🔌 API Endpoints

| Endpoint | Method | توضیح |
|----------|--------|-------|
| `/api/generate-content` | POST | تولید محتوا |
| `/api/optimize-seo` | POST | بهینه‌سازی SEO |
| `/api/generate-visual-idea` | POST | تولید ایده بصری |
| `/api/schedule-post` | POST | زمان‌بندی انتشار |
| `/api/scheduled-posts` | GET | لیست زمان‌بندی شده |
| `/api/scheduled-posts/{id}` | DELETE | لغو زمان‌بندی |
| `/api/platforms` | GET | پلتفرم‌های پشتیبانی شده |
| `/api/stats` | GET | آمار سیستم |

## 🧪 تست و نمونه‌ها

### اجرای نمونه‌ها
```bash
cd examples
python sample_requests.py
```

### تست‌های خودکار
```bash
# نصب pytest
pip install pytest

# اجرای تست‌ها
pytest tests/
```

## ⚙️ تنظیمات پیشرفته

### متغیرهای محیطی
```bash
export API_KEY="your-ai-api-key"
export INSTAGRAM_TOKEN="your-instagram-token"
export TELEGRAM_BOT_TOKEN="your-telegram-token"
```

### تنظیمات پایگاه داده
```python
# در فایل config.py
DATABASE_URL = "postgresql://user:password@localhost/dbname"
REDIS_URL = "redis://localhost:6379"
```

## 🔧 توسعه و سفارشی‌سازی

### اضافه کردن پلتفرم جدید
1. پلتفرم را به `PlatformType` اضافه کنید
2. تنظیمات را در `PLATFORM_CONFIGS` تعریف کنید
3. متد انتشار را در `ContentScheduler` پیاده‌سازی کنید

### ایجاد تولیدکننده محتوای سفارشی
```python
class CustomContentGenerator:
    async def generate_custom_content(self, params):
        # منطق تولید محتوای سفارشی
        pass
```

## 📈 مانیتورینگ و لاگ

### لاگ‌های سیستم
- تمام عملیات در فایل `app.log` ثبت می‌شوند
- سطوح مختلف لاگ: INFO, WARNING, ERROR
- ردیابی زمان پاسخ و عملکرد

### آمار عملکرد
- تعداد محتوای تولید شده
- آمار پلتفرم‌ها
- زمان پاسخ‌دهی
- نرخ موفقیت انتشار

## 🚀 استقرار در پروداکشن

### Docker
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
  redis:
    image: redis:alpine
  postgres:
    image: postgres:13
```

## 🤝 مشارکت

### راهنمای مشارکت
1. Fork کنید
2. برنچ جدید بسازید (`git checkout -b feature/AmazingFeature`)
3. تغییرات را commit کنید (`git commit -m 'Add some AmazingFeature'`)
4. به برنچ push کنید (`git push origin feature/AmazingFeature`)
5. Pull Request باز کنید

### استانداردهای کد
- استفاده از Black برای فرمت کردن
- Docstring برای تمام توابع
- Type hints برای پارامترها
- تست‌نویسی برای ویژگی‌های جدید

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات بیشتر فایل `LICENSE` را ببینید.

## 🆘 پشتیبانی

### مسائل رایج
- **خطای اتصال**: بررسی کنید سرور در حال اجرا باشد
- **خطای API**: کلیدهای API را بررسی کنید
- **مشکل انتشار**: تنظیمات پلتفرم را چک کنید

### تماس با ما
- 📧 Email: support@contentgenerator.ai
- 💬 Telegram: @ContentGeneratorSupport
- 🐛 Issues: GitHub Issues

## 🎉 تشکر ویژه

از تمامی توسعه‌دهندگان، طراحان و کاربرانی که در بهبود این سیستم مشارکت داشته‌اند، صمیمانه تشکر می‌کنیم.

---

<div align="center">

**🚀 ساخته شده با ❤️ برای جامعه محتواسازان ایرانی**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Persian](https://img.shields.io/badge/Language-Persian-red.svg)](README.md)

</div>