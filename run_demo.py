#!/usr/bin/env python3
"""
اسکریپت نمایشی برای راه‌اندازی سریع سیستم تولید محتوای هوش مصنوعی
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_python_version():
    """بررسی نسخه پایتون"""
    if sys.version_info < (3, 8):
        print("❌ نسخه پایتون باید 3.8 یا بالاتر باشد")
        print(f"نسخه فعلی: {sys.version}")
        return False
    print(f"✅ نسخه پایتون: {sys.version.split()[0]}")
    return True

def install_requirements():
    """نصب وابستگی‌ها"""
    print("📦 در حال نصب وابستگی‌ها...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ وابستگی‌ها با موفقیت نصب شدند")
        return True
    except subprocess.CalledProcessError:
        print("❌ خطا در نصب وابستگی‌ها")
        return False

def setup_demo_data():
    """آماده‌سازی داده‌های نمونه"""
    print("🔧 آماده‌سازی داده‌های نمونه...")
    
    # ایجاد پوشه‌های مورد نیاز
    directories = ["logs", "data", "uploads"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ داده‌های نمونه آماده شدند")

def start_server():
    """راه‌اندازی سرور"""
    print("🚀 راه‌اندازی سرور...")
    
    try:
        # راه‌اندازی سرور در پس‌زمینه
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ])
        
        print("⏳ منتظر راه‌اندازی سرور...")
        time.sleep(5)  # منتظر راه‌اندازی سرور
        
        # بررسی وضعیت سرور
        if process.poll() is None:
            print("✅ سرور با موفقیت راه‌اندازی شد")
            print("🌐 آدرس سرور: http://localhost:8000")
            return process
        else:
            print("❌ خطا در راه‌اندازی سرور")
            return None
            
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی سرور: {e}")
        return None

def run_demo_examples():
    """اجرای نمونه‌های دمو"""
    print("\n🎯 اجرای نمونه‌های دمو...")
    
    try:
        # منتظر آماده شدن کامل سرور
        time.sleep(3)
        
        print("📝 تست تولید محتوا...")
        subprocess.run([
            sys.executable, "examples/sample_requests.py"
        ], timeout=30)
        
        print("✅ نمونه‌ها با موفقیت اجرا شدند")
        
    except subprocess.TimeoutExpired:
        print("⏰ زمان اجرای نمونه‌ها به پایان رسید")
    except Exception as e:
        print(f"❌ خطا در اجرای نمونه‌ها: {e}")

def open_browser():
    """باز کردن مرورگر"""
    print("🌐 باز کردن مرورگر...")
    try:
        webbrowser.open("http://localhost:8000")
        print("✅ مرورگر باز شد")
    except Exception as e:
        print(f"❌ خطا در باز کردن مرورگر: {e}")
        print("لطفاً خودتان آدرس http://localhost:8000 را در مرورگر باز کنید")

def print_banner():
    """نمایش بنر خوشامدگویی"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║          🤖 سیستم تولید محتوای هوش مصنوعی چندپلتفرمی           ║
    ║                                                                  ║
    ║                    🚀 نسخه نمایشی 1.0.0                         ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_help():
    """نمایش راهنما"""
    help_text = """
    🎯 ویژگی‌های سیستم:
    
    ✨ تولید محتوا برای 5 پلتفرم (Instagram, Telegram, Website, Eitaa, Rubika)
    🔍 بهینه‌سازی خودکار SEO
    🎨 تولید ایده‌های بصری
    ⏰ زمان‌بندی انتشار هوشمند
    📊 آنالیتیک و آمار پیشرفته
    
    🌐 آدرس‌های مهم:
    • رابط کاربری: http://localhost:8000
    • مستندات API: http://localhost:8000/docs
    • ReDoc: http://localhost:8000/redoc
    
    ⌨️ کلیدهای میانبر:
    • Ctrl+Enter: تولید محتوا
    • Ctrl+S: ذخیره محتوا
    • Ctrl+C: کپی محتوا
    
    🆘 در صورت مشکل:
    • بررسی کنید Python 3.8+ نصب باشد
    • از اجرای همزمان چند نمونه خودداری کنید
    • فایل‌های لاگ را در پوشه logs بررسی کنید
    """
    print(help_text)

def main():
    """تابع اصلی"""
    print_banner()
    
    # بررسی‌های اولیه
    if not check_python_version():
        return
    
    print("🔍 بررسی محیط...")
    
    # نصب وابستگی‌ها
    if not install_requirements():
        print("❌ نصب وابستگی‌ها ناموفق بود")
        return
    
    # آماده‌سازی
    setup_demo_data()
    
    # راه‌اندازی سرور
    server_process = start_server()
    if not server_process:
        return
    
    try:
        print("\n" + "="*70)
        print("🎉 سیستم آماده است!")
        print("="*70)
        
        # نمایش راهنما
        print_help()
        
        # باز کردن مرورگر
        open_browser()
        
        # اجرای نمونه‌ها (اختیاری)
        response = input("\n❓ آیا می‌خواهید نمونه‌های دمو را اجرا کنید؟ (y/n): ")
        if response.lower() in ['y', 'yes', 'آری', 'بله']:
            run_demo_examples()
        
        print("\n🔄 سرور در حال اجرا است...")
        print("💡 برای خروج Ctrl+C را فشار دهید")
        
        # نگه داشتن سرور
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 در حال بستن سرور...")
        server_process.terminate()
        server_process.wait()
        print("✅ سرور بسته شد")
        print("👋 خداحافظ!")

if __name__ == "__main__":
    main()