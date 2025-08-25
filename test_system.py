#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تست ساده سیستم تولید محتوای هوش مصنوعی
"""

def test_basic_functionality():
    """تست عملکرد پایه"""
    print("🧪 شروع تست عملکرد پایه...")
    
    try:
        # تست import مدل‌ها
        from models import Platform, Tone
        print("✅ مدل‌ها با موفقیت import شدند")
        
        # تست enum ها
        platforms = [p.value for p in Platform]
        tones = [t.value for t in Tone]
        print(f"✅ پلتفرم‌ها: {platforms}")
        print(f"✅ لحن‌ها: {tones}")
        
        # تست تنظیمات
        from config import Config
        print(f"✅ تنظیمات بارگذاری شد: {Config.GEMINI_MODEL}")
        
        print("🎉 تمام تست‌های پایه موفق بودند!")
        return True
        
    except ImportError as e:
        print(f"❌ خطا در import: {e}")
        return False
    except Exception as e:
        print(f"❌ خطای نامشخص: {e}")
        return False

def test_content_generation():
    """تست تولید محتوا (بدون API)"""
    print("\n🔄 تست تولید محتوا...")
    
    try:
        # تست ایجاد درخواست
        from models import ContentRequest, Platform, Tone
        
        request = ContentRequest(
            topic="تست سیستم",
            keywords=["تست", "سیستم"],
            target_audience="توسعه‌دهندگان",
            tone=Tone.PROFESSIONAL,
            platforms=[Platform.INSTAGRAM, Platform.TELEGRAM],
            language="persian"
        )
        
        print("✅ درخواست محتوا ایجاد شد")
        print(f"   موضوع: {request.topic}")
        print(f"   پلتفرم‌ها: {[p.value for p in request.platforms]}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست تولید محتوا: {e}")
        return False

def main():
    """تابع اصلی"""
    print("🎯 تست سیستم تولید محتوای هوش مصنوعی")
    print("="*50)
    
    # تست عملکرد پایه
    basic_success = test_basic_functionality()
    
    # تست تولید محتوا
    content_success = test_content_generation()
    
    print("\n" + "="*50)
    if basic_success and content_success:
        print("🎉 تمام تست‌ها موفق بودند!")
        print("\n📚 برای استفاده کامل:")
        print("   1. فایل .env را با API Key خود ایجاد کنید")
        print("   2. سرور را با 'python main.py' اجرا کنید")
        print("   3. به http://localhost:8000 مراجعه کنید")
    else:
        print("❌ برخی تست‌ها ناموفق بودند")
        print("   لطفاً خطاها را بررسی کنید")

if __name__ == "__main__":
    main()