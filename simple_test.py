#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تست ساده سیستم تولید محتوای هوش مصنوعی
"""

def test_basic():
    """تست پایه سیستم"""
    print("🧪 تست پایه سیستم...")
    
    try:
        # تست import مدل‌ها
        from models import Platform, Tone
        print("✅ مدل‌ها با موفقیت import شدند")
        
        # تست enum ها
        platforms = [p.value for p in Platform]
        tones = [t.value for t in Tone]
        print(f"✅ پلتفرم‌ها: {platforms}")
        print(f"✅ لحن‌ها: {tones}")
        
        print("🎉 تست پایه موفق بود!")
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست: {e}")
        return False

if __name__ == "__main__":
    print("🎯 تست ساده سیستم تولید محتوای هوش مصنوعی")
    print("="*50)
    
    success = test_basic()
    
    print("\n" + "="*50)
    if success:
        print("✅ سیستم آماده است!")
        print("\n📚 برای استفاده:")
        print("   1. فایل .env را با API Key خود ایجاد کنید")
        print("   2. سرور را با 'python main.py' اجرا کنید")
        print("   3. به http://localhost:8000 مراجعه کنید")
    else:
        print("❌ تست ناموفق بود")
        print("   لطفاً خطاها را بررسی کنید")