<header>

<!--
  <<< Author notes: Course header >>>
  Include a 1280×640 image, course title in sentence case, and a concise description in emphasis.
  In your repository settings: enable template repository, add your 1280×640 social image, auto delete head branches.
  Add your open source license, GitHub uses MIT license.
-->

# 🚀 سیستم تولید محتوای هوش مصنوعی چندپلتفرمی

یک سیستم پیشرفته تولید محتوا که با استفاده از **Gemini 2.5 Flash** و قابلیت **Function Calling**، محتوای بهینه و اختصاصی برای پلتفرم‌های مختلف تولید می‌کند.

## ✨ ویژگی‌های کلیدی

- 🎯 **تولید محتوای چندپلتفرمی**: اینستاگرام، تلگرام، وب‌سایت، ایتا، روبیکا
- 🤖 **هوش مصنوعی پیشرفته**: استفاده از Gemini 2.5 Flash با Function Calling
- 🔍 **بهینه‌سازی SEO**: محتوای وب‌سایت کاملاً SEO-friendly
- 🎨 **پیشنهادات بصری**: ایده‌های تصویر و ویدئو متناسب با محتوا
- ⏰ **زمان‌بندی خودکار**: انتشار خودکار محتوا در زمان‌های مشخص
- 🌍 **پشتیبانی چندزبانه**: تولید محتوا به زبان‌های مختلف
- 📊 **تحلیل موضوع**: تحلیل عمیق و ایده‌پردازی خلاقانه

## 🏗️ معماری سیستم

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │───▶│ Content Generator│───▶│  Gemini Client  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Scheduler     │    │   Models & API   │    │ Function Calls  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8+
- Gemini API Key

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

3. **تنظیم API Key**
```bash
cp .env.example .env
# فایل .env را ویرایش کرده و GEMINI_API_KEY خود را اضافه کنید
```

4. **اجرای سیستم**
```bash
python main.py
```

## 📖 نحوه استفاده

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
  "include_visual_suggestions": true,
  "include_seo": true
}
```

#### بررسی وضعیت
```http
GET /health
```

#### دریافت پلتفرم‌ها
```http
GET /platforms
```

### نمونه کد Python

```python
from models import ContentRequest, Platform, Tone
from content_generator import ContentGenerator

# ایجاد درخواست
request = ContentRequest(
    topic="نکات موفقیت در کسب‌وکار",
    keywords=["موفقیت", "کسب‌وکار"],
    target_audience="کارآفرینان",
    tone=Tone.PROFESSIONAL,
    platforms=[Platform.INSTAGRAM, Platform.TELEGRAM],
    include_visual_suggestions=True
)

# تولید محتوا
generator = ContentGenerator()
response = generator.generate_content(request)

# نمایش نتایج
print(f"کپشن اینستاگرام: {response.instagram_content['caption']}")
print(f"هشتگ‌ها: {response.hashtags}")
```

## 🎯 پلتفرم‌های پشتیبانی شده

### 📱 اینستاگرام
- کپشن‌های جذاب (حداکثر 2200 کاراکتر)
- هشتگ‌های بهینه
- اموجی‌های مناسب
- CTA موثر

### 💬 تلگرام
- محتوای کامل و مفصل
- هشتگ‌های مرتبط
- اموجی‌های مناسب
- CTA موثر

### 🌐 وب‌سایت
- محتوای SEO-friendly
- عنوان و متاتگ بهینه
- هدینگ‌های استاندارد
- کلمات کلیدی SEO

### 📢 ایتا
- محتوای مناسب شبکه اجتماعی
- هشتگ‌های مرتبط
- اموجی‌های مناسب

### 🎯 روبیکا
- محتوای بهینه برای الگوریتم جدید
- هشتگ‌های موثر
- CTA مناسب

## 🔧 Function Calling

سیستم از قابلیت Function Calling Gemini برای تولید محتوای ساختاریافته استفاده می‌کند:

### توابع تعریف شده

1. **`generate_content`**: تولید محتوای متناسب با پلتفرم
2. **`optimize_for_seo`**: بهینه‌سازی محتوای وب‌سایت
3. **`generate_visual_idea`**: تولید ایده‌های بصری

## ⏰ سیستم زمان‌بندی

```python
from scheduler import ContentScheduler
from datetime import datetime, timedelta

scheduler = ContentScheduler()

# زمان‌بندی پست
publish_time = datetime.now() + timedelta(hours=2)
post_id = scheduler.schedule_post(
    Platform.INSTAGRAM,
    content_request,
    publish_time
)

# پست‌های تکرارشونده
post_ids = scheduler.schedule_recurring_posts(
    Platform.TELEGRAM,
    content_request,
    interval_hours=24,
    start_time=datetime.now()
)
```

## 🎨 پیشنهادات بصری

سیستم برای هر محتوا پیشنهادات بصری ارائه می‌دهد:

- **سبک تصویر**: modern, minimalist, vibrant, professional
- **رنگ‌بندی**: پالت‌های رنگی متناسب با سبک
- **ترکیب‌بندی**: راهنمایی برای طراحی
- **ویدئو**: مدت و سبک مناسب

## 🔍 بهینه‌سازی SEO

برای محتوای وب‌سایت:

- عنوان بهینه (حداکثر 60 کاراکتر)
- توضیحات متا (حداکثر 160 کاراکتر)
- هدینگ‌های H1, H2, H3
- کلمات کلیدی هدفمند

## 📊 نمونه خروجی

```json
{
  "topic_analysis": {
    "analysis": "تحلیل کامل موضوع...",
    "key_points": ["نکته 1", "نکته 2"],
    "creative_angles": ["زاویه 1", "زاویه 2"]
  },
  "instagram_content": {
    "caption": "کپشن جذاب...",
    "hashtags": ["#هشتگ1", "#هشتگ2"],
    "emojis": ["🚀", "💡"],
    "cta": "شروع کنید"
  },
  "hashtags": ["#موضوع", "#کلمه_کلیدی"],
  "visual_suggestions": {
    "image_style": "modern",
    "color_scheme": ["#2C3E50", "#3498DB"],
    "composition": "ترکیب‌بندی متقارن"
  }
}
```

## 🛠️ توسعه و سفارشی‌سازی

### اضافه کردن پلتفرم جدید

```python
# در models.py
class Platform(str, Enum):
    NEW_PLATFORM = "new_platform"

# در content_generator.py
def _generate_new_platform_content(self, request: ContentRequest):
    # منطق تولید محتوا
    pass
```

### تنظیمات جدید

```python
# در config.py
class Config:
    NEW_PLATFORM_MAX_LENGTH = 1000
    NEW_PLATFORM_FEATURES = ["feature1", "feature2"]
```

## 📝 نمونه‌های استفاده

### تولید انبوه محتوا

```python
topics = ["موضوع 1", "موضوع 2", "موضوع 3"]
for topic in topics:
    request = ContentRequest(topic=topic, ...)
    response = generator.generate_content(request)
    # ذخیره یا انتشار محتوا
```

### زمان‌بندی هوشمند

```python
# انتشار در بهترین زمان‌ها
best_times = {
    Platform.INSTAGRAM: ["09:00", "18:00"],
    Platform.TELEGRAM: ["08:00", "12:00", "20:00"]
}

scheduler.schedule_platform_specific_posts(request, best_times)
```

## 🔒 امنیت

- API Key ها در فایل `.env` ذخیره می‌شوند
- اعتبارسنجی ورودی‌ها با Pydantic
- محدودیت‌های مناسب برای API calls

## 📈 عملکرد

- تولید محتوا در کمتر از 10 ثانیه
- پشتیبانی از 100+ درخواست همزمان
- کش کردن نتایج برای بهبود سرعت

## 🤝 مشارکت

1. Fork کنید
2. Branch جدید ایجاد کنید (`git checkout -b feature/amazing-feature`)
3. تغییرات را commit کنید (`git commit -m 'Add amazing feature'`)
4. Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request ایجاد کنید

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

## 📞 پشتیبانی

- 📧 ایمیل: support@example.com
- 💬 تلگرام: @support_channel
- 🐛 Issues: GitHub Issues

## 🙏 تشکر

از تمامی مشارکت‌کنندگان و کاربران این سیستم تشکر می‌کنیم.

---

**نکته**: برای استفاده از این سیستم، حتماً API Key معتبر Gemini داشته باشید.
