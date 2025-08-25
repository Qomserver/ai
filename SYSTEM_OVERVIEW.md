# 🎯 مرور کلی سیستم تولید محتوای هوش مصنوعی

## 📁 ساختار پروژه

```
ai-content-generator/
├── 📄 main.py                 # اپلیکیشن اصلی FastAPI
├── 📄 models.py               # مدل‌های داده Pydantic
├── 📄 config.py               # تنظیمات سیستم
├── 📄 gemini_client.py        # کلاینت Gemini AI
├── 📄 content_generator.py    # موتور تولید محتوا
├── 📄 scheduler.py            # زمان‌بند انتشار
├── 📄 api_client.py           # کلاینت‌های API شبکه‌های اجتماعی
├── 📄 utils.py                # توابع کمکی
├── 📄 requirements.txt        # وابستگی‌های Python
├── 📄 .env.example           # نمونه فایل محیطی
├── 📄 Dockerfile             # فایل Docker
├── 📄 docker-compose.yml     # Docker Compose
├── 📄 test_system.py         # تست کامل سیستم
├── 📄 simple_test.py         # تست ساده
└── 📄 README.md              # مستندات کامل
```

## 🚀 ویژگی‌های اصلی

### 1. تولید محتوای چندپلتفرمی
- **اینستاگرام**: کپشن‌های جذاب با هشتگ و اموجی
- **تلگرام**: محتوای کامل و مفصل
- **وب‌سایت**: محتوای SEO-friendly
- **ایتا**: محتوای شبکه اجتماعی
- **روبیکا**: محتوای بهینه برای الگوریتم جدید

### 2. هوش مصنوعی پیشرفته
- استفاده از **Gemini 2.5 Flash**
- قابلیت **Function Calling**
- تولید محتوای خلاقانه و متناسب
- پشتیبانی از زبان فارسی

### 3. بهینه‌سازی خودکار
- SEO برای وب‌سایت
- هشتگ‌های مرتبط
- پیشنهادات بصری
- CTA موثر

## 🔧 نحوه کارکرد

### مرحله 1: دریافت درخواست
```python
request = ContentRequest(
    topic="بازاریابی دیجیتال",
    keywords=["بازاریابی", "دیجیتال"],
    target_audience="کارآفرینان",
    tone="professional",
    platforms=["instagram", "website"]
)
```

### مرحله 2: تحلیل موضوع
- تحلیل کلمات کلیدی
- شناسایی مخاطب هدف
- تعیین لحن مناسب

### مرحله 3: تولید محتوا
- تولید محتوای اختصاصی برای هر پلتفرم
- بهینه‌سازی SEO
- تولید هشتگ‌ها و پیشنهادات بصری

### مرحله 4: خروجی نهایی
```json
{
  "instagram_content": {...},
  "website_content": {...},
  "hashtags": [...],
  "visual_suggestions": {...},
  "seo_optimization": {...}
}
```

## 🌐 API Endpoints

| متد | مسیر | توضیحات |
|-----|------|----------|
| `GET` | `/` | صفحه اصلی |
| `POST` | `/generate-content` | تولید محتوا |
| `GET` | `/health` | بررسی وضعیت |
| `GET` | `/platforms` | لیست پلتفرم‌ها |
| `GET` | `/tones` | لیست لحن‌ها |

## 🎨 قالب‌های خروجی

### اینستاگرام
```json
{
  "caption": "متن کپشن...",
  "hashtags": ["#هشتگ1", "#هشتگ2"],
  "emojis": ["😊", "🚀"],
  "cta": "برای اطلاعات بیشتر کلیک کنید"
}
```

### وب‌سایت
```json
{
  "title": "عنوان SEO",
  "meta_description": "توضیحات متا",
  "content": "محتوای اصلی",
  "headings": ["H1", "H2", "H3"],
  "keywords": ["کلمه1", "کلمه2"]
}
```

## 🔍 Function Calling

سیستم از توابع تعریف شده استفاده می‌کند:

1. **`generate_content`**: تولید محتوای پلتفرم خاص
2. **`optimize_for_seo`**: بهینه‌سازی SEO
3. **`generate_visual_idea`**: تولید ایده بصری

## 📊 تست و توسعه

### تست پایه
```bash
python simple_test.py
```

### تست کامل
```bash
python test_system.py
```

### تست API
```bash
curl -X POST "http://localhost:8000/generate-content" \
  -H "Content-Type: application/json" \
  -d '{"topic": "تست", "platforms": ["instagram"]}'
```

## 🚀 استقرار

### محلی
```bash
pip install -r requirements.txt
python main.py
```

### Docker
```bash
docker build -t ai-content-generator .
docker run -p 8000:8000 ai-content-generator
```

### Docker Compose
```bash
docker-compose up -d
```

## 🔒 امنیت و تنظیمات

- API Keys در فایل `.env`
- اعتبارسنجی ورودی‌ها
- CORS تنظیم شده
- محدودیت نرخ درخواست

## 📈 عملکرد

- **سرعت**: تولید محتوا در کمتر از 10 ثانیه
- **مقیاس**: پشتیبانی از 5 پلتفرم همزمان
- **کیفیت**: محتوای بهینه و خلاقانه
- **قابلیت اطمینان**: سیستم پایدار و قابل اعتماد

## 🔮 توسعه‌های آینده

- پشتیبانی از پلتفرم‌های بیشتر
- قابلیت ترجمه چندزبانه
- تحلیل عملکرد محتوا
- یکپارچه‌سازی با CRM ها
- هوش مصنوعی پیشرفته‌تر

---

**🎯 هدف**: ایجاد یک سیستم جامع و حرفه‌ای برای تولید محتوای هوش مصنوعی که نیازهای کسب‌وکارهای مختلف را برآورده کند.