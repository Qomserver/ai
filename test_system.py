#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست ساده سیستم تولید محتوای هوش مصنوعی
"""

import os
import sys
from models import ContentRequest, Platform, Tone

def test_models():
    """تست مدل‌های داده"""
    print("🧪 تست مدل‌های داده...")
    
    try:
        # تست ایجاد درخواست
        request = ContentRequest(
            topic="تست سیستم",
            keywords=["تست", "سیستم"],
            target_audience="توسعه‌دهندگان",
            tone=Tone.PROFESSIONAL,
            platforms=[Platform.INSTAGRAM, Platform.TELEGRAM],
            include_visual_suggestions=True,
            include_seo=False
        )
        
        print("✅ ContentRequest ایجاد شد")
        print(f"   موضوع: {request.topic}")
        print(f"   پلتفرم‌ها: {[p.value for p in request.platforms]}")
        print(f"   لحن: {request.tone.value}")
        
        # تست تبدیل به دیکشنری
        request_dict = request.dict()
        print("✅ تبدیل به دیکشنری موفق")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست مدل‌ها: {str(e)}")
        return False

def test_config():
    """تست تنظیمات"""
    print("\n⚙️ تست تنظیمات...")
    
    try:
        from config import Config
        
        print("✅ فایل تنظیمات بارگذاری شد")
        print(f"   مدل Gemini: {Config.GEMINI_MODEL}")
        print(f"   حداکثر طول کپشن اینستاگرام: {Config.INSTAGRAM_MAX_CAPTION_LENGTH}")
        print(f"   حداکثر هشتگ: {Config.MAX_HASHTAGS}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست تنظیمات: {str(e)}")
        return False

def test_imports():
    """تست import کردن ماژول‌ها"""
    print("\n📦 تست import کردن ماژول‌ها...")
    
    try:
        # تست import کردن ماژول‌های اصلی
        from content_generator import ContentGenerator
        print("✅ ContentGenerator import شد")
        
        from gemini_client import GeminiClient
        print("✅ GeminiClient import شد")
        
        from scheduler import ContentScheduler
        print("✅ ContentScheduler import شد")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در import: {str(e)}")
        return False

def test_environment():
    """تست محیط اجرا"""
    print("\n🌍 تست محیط اجرا...")
    
    try:
        # بررسی Python version
        python_version = sys.version_info
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # بررسی وجود فایل‌های اصلی
        required_files = [
            "main.py",
            "models.py",
            "content_generator.py",
            "gemini_client.py",
            "scheduler.py",
            "config.py"
        ]
        
        for file in required_files:
            if os.path.exists(file):
                print(f"✅ {file} موجود است")
            else:
                print(f"❌ {file} یافت نشد")
                return False
        
        # بررسی وجود فایل requirements.txt
        if os.path.exists("requirements.txt"):
            print("✅ requirements.txt موجود است")
        else:
            print("❌ requirements.txt یافت نشد")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست محیط: {str(e)}")
        return False

def main():
    """تابع اصلی تست"""
    print("🚀 شروع تست سیستم تولید محتوای هوش مصنوعی")
    print("=" * 60)
    
    tests = [
        test_environment,
        test_imports,
        test_config,
        test_models
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 نتایج تست: {passed}/{total} تست موفق")
    
    if passed == total:
        print("🎉 تمام تست‌ها با موفقیت انجام شد!")
        print("\n✅ سیستم آماده استفاده است")
        print("\nبرای اجرای سیستم:")
        print("1. فایل .env را ایجاد کرده و GEMINI_API_KEY را اضافه کنید")
        print("2. دستور 'python main.py' را اجرا کنید")
        print("3. یا از 'python example_usage.py' برای نمونه استفاده کنید")
    else:
        print("❌ برخی تست‌ها ناموفق بودند")
        print("\nبرای رفع مشکل:")
        print("1. مطمئن شوید تمام فایل‌ها موجود هستند")
        print("2. وابستگی‌ها را با 'pip install -r requirements.txt' نصب کنید")
        print("3. خطاهای Python را بررسی کنید")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 تست متوقف شد")
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {str(e)}")
        print("لطفاً مشکل را بررسی کرده و دوباره تلاش کنید")