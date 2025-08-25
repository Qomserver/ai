#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نمونه استفاده از سیستم تولید محتوای هوش مصنوعی چندپلتفرمی
"""

import os
import sys
from datetime import datetime, timedelta
from models import ContentRequest, Platform, Tone
from content_generator import ContentGenerator
from scheduler import ContentScheduler

def main():
    """نمونه استفاده اصلی"""
    
    print("🚀 سیستم تولید محتوای هوش مصنوعی چندپلتفرمی")
    print("=" * 60)
    
    # بررسی وجود API Key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY تنظیم نشده است!")
        print("لطفاً فایل .env را ایجاد کرده و API Key را اضافه کنید:")
        print("GEMINI_API_KEY=your_api_key_here")
        return
    
    try:
        # ایجاد نمونه از تولیدکننده محتوا
        content_generator = ContentGenerator()
        
        # نمونه درخواست محتوا
        request = ContentRequest(
            topic="بازاریابی دیجیتال در سال 2024",
            keywords=["بازاریابی دیجیتال", "شبکه‌های اجتماعی", "محتوا", "SEO"],
            target_audience="کارآفرینان و مدیران کسب‌وکار",
            tone=Tone.PROFESSIONAL,
            platforms=[Platform.INSTAGRAM, Platform.TELEGRAM, Platform.WEBSITE],
            include_visual_suggestions=True,
            include_seo=True
        )
        
        print("\n📝 درخواست محتوا:")
        print(f"موضوع: {request.topic}")
        print(f"کلمات کلیدی: {', '.join(request.keywords)}")
        print(f"مخاطب: {request.target_audience}")
        print(f"لحن: {request.tone.value}")
        print(f"پلتفرم‌ها: {[p.value for p in request.platforms]}")
        
        print("\n🔄 در حال تولید محتوا...")
        
        # تولید محتوا
        response = content_generator.generate_content(request)
        
        print("\n✅ محتوا با موفقیت تولید شد!")
        print("\n" + "=" * 60)
        
        # نمایش تحلیل موضوع
        print("📊 تحلیل موضوع:")
        print(f"تحلیل: {response.topic_analysis.get('analysis', '')[:200]}...")
        
        # نمایش محتوای اینستاگرام
        if response.instagram_content:
            print("\n📱 محتوای اینستاگرام:")
            print(f"کپشن: {response.instagram_content.get('caption', '')[:100]}...")
            print(f"هشتگ‌ها: {', '.join(response.instagram_content.get('hashtags', [])[:5])}")
            print(f"اموجی‌ها: {', '.join(response.instagram_content.get('emojis', [])[:3])}")
            print(f"CTA: {response.instagram_content.get('cta', '')}")
        
        # نمایش محتوای تلگرام
        if response.telegram_content:
            print("\n💬 محتوای تلگرام:")
            print(f"محتوا: {response.telegram_content.get('content', '')[:150]}...")
            print(f"هشتگ‌ها: {', '.join(response.telegram_content.get('hashtags', [])[:5])}")
        
        # نمایش محتوای وب‌سایت
        if response.website_content:
            print("\n🌐 محتوای وب‌سایت:")
            print(f"عنوان: {response.website_content.get('title', '')}")
            print(f"توضیحات متا: {response.website_content.get('meta_description', '')}")
            print(f"هدینگ‌ها: {', '.join(response.website_content.get('headings', [])[:3])}")
        
        # نمایش هشتگ‌های کلی
        print(f"\n🏷️ هشتگ‌های پیشنهادی:")
        print(f"{', '.join(response.hashtags[:10])}")
        
        # نمایش پیشنهادات بصری
        print(f"\n🎨 پیشنهادات بصری:")
        visual = response.visual_suggestions
        print(f"سبک تصویر: {visual.get('image_style', '')}")
        print(f"رنگ‌بندی: {', '.join(visual.get('color_scheme', [])[:3])}")
        print(f"ترکیب‌بندی: {visual.get('composition', '')}")
        if visual.get('video_duration'):
            print(f"مدت ویدئو: {visual.get('video_duration')} ثانیه")
        
        # نمایش پیشنهادات CTA
        print(f"\n🎯 پیشنهادات CTA:")
        for i, cta in enumerate(response.cta_suggestions[:3], 1):
            print(f"{i}. {cta}")
        
        # نمایش بهینه‌سازی SEO
        if response.seo_optimization:
            print(f"\n🔍 بهینه‌سازی SEO:")
            seo = response.seo_optimization
            print(f"عنوان SEO: {seo.get('title', '')}")
            print(f"توضیحات متا: {seo.get('meta_description', '')}")
            print(f"هدینگ‌های SEO: {', '.join(seo.get('headings', [])[:3])}")
        
        # نمایش نمونه زمان‌بندی
        print("\n" + "=" * 60)
        print("⏰ نمونه زمان‌بندی انتشار:")
        
        scheduler = ContentScheduler()
        
        # زمان‌بندی پست برای اینستاگرام
        instagram_time = datetime.now() + timedelta(hours=2)
        post_id = scheduler.schedule_post(
            Platform.INSTAGRAM,
            request,
            instagram_time
        )
        print(f"پست اینستاگرام در ساعت {instagram_time.strftime('%H:%M')} زمان‌بندی شد (ID: {post_id})")
        
        # زمان‌بندی پست برای تلگرام
        telegram_time = datetime.now() + timedelta(hours=4)
        post_id = scheduler.schedule_post(
            Platform.TELEGRAM,
            request,
            telegram_time
        )
        print(f"پست تلگرام در ساعت {telegram_time.strftime('%H:%M')} زمان‌بندی شد (ID: {post_id})")
        
        # نمایش پست‌های زمان‌بندی شده
        scheduled_posts = scheduler.get_scheduled_posts()
        print(f"\n📅 تعداد پست‌های زمان‌بندی شده: {len(scheduled_posts)}")
        
        for post in scheduled_posts:
            print(f"- {post['platform']}: {post['publish_time']} (وضعیت: {post['status']})")
        
        print("\n🎉 نمونه استفاده با موفقیت اجرا شد!")
        
    except Exception as e:
        print(f"\n❌ خطا: {str(e)}")
        print("\nبرای رفع مشکل:")
        print("1. مطمئن شوید GEMINI_API_KEY تنظیم شده است")
        print("2. اتصال اینترنت خود را بررسی کنید")
        print("3. نسخه‌های پکیج‌ها را بررسی کنید")

def demo_simple_content():
    """نمونه ساده تولید محتوا"""
    
    print("\n🔧 نمونه ساده تولید محتوا:")
    
    try:
        content_generator = ContentGenerator()
        
        # درخواست ساده
        simple_request = ContentRequest(
            topic="نکات موفقیت در کسب‌وکار",
            keywords=["موفقیت", "کسب‌وکار", "نکات"],
            target_audience="کارآفرینان",
            tone=Tone.INSPIRATIONAL,
            platforms=[Platform.INSTAGRAM],
            include_visual_suggestions=False,
            include_seo=False
        )
        
        print("درخواست: تولید محتوای الهام‌بخش برای اینستاگرام")
        
        response = content_generator.generate_content(simple_request)
        
        if response.instagram_content:
            print(f"✅ کپشن تولید شد: {response.instagram_content.get('caption', '')[:100]}...")
            print(f"🏷️ هشتگ‌ها: {', '.join(response.hashtags[:5])}")
        
    except Exception as e:
        print(f"❌ خطا در نمونه ساده: {str(e)}")

def demo_bulk_generation():
    """نمونه تولید انبوه محتوا"""
    
    print("\n📚 نمونه تولید انبوه محتوا:")
    
    topics = [
        "تکنیک‌های مدیریت زمان",
        "راه‌های افزایش بهره‌وری",
        "استراتژی‌های بازاریابی محتوا",
        "نکات موفقیت در شبکه‌های اجتماعی"
    ]
    
    try:
        content_generator = ContentGenerator()
        
        for i, topic in enumerate(topics, 1):
            print(f"\n{i}. تولید محتوا برای: {topic}")
            
            request = ContentRequest(
                topic=topic,
                keywords=[topic.split()[0], "موفقیت", "نکات"],
                target_audience="کارآفرینان",
                tone=Tone.PROFESSIONAL,
                platforms=[Platform.INSTAGRAM, Platform.TELEGRAM],
                include_visual_suggestions=False,
                include_seo=False
            )
            
            response = content_generator.generate_content(request)
            
            if response.instagram_content:
                caption = response.instagram_content.get('caption', '')
                print(f"   ✅ کپشن: {caption[:80]}...")
            
            if response.telegram_content:
                content = response.telegram_content.get('content', '')
                print(f"   💬 محتوا: {content[:80]}...")
        
        print(f"\n🎯 {len(topics)} محتوا با موفقیت تولید شد!")
        
    except Exception as e:
        print(f"❌ خطا در تولید انبوه: {str(e)}")

if __name__ == "__main__":
    print("انتخاب کنید:")
    print("1. اجرای کامل نمونه")
    print("2. نمونه ساده")
    print("3. تولید انبوه")
    
    try:
        choice = input("انتخاب شما (1-3): ").strip()
        
        if choice == "1":
            main()
        elif choice == "2":
            demo_simple_content()
        elif choice == "3":
            demo_bulk_generation()
        else:
            print("انتخاب نامعتبر. اجرای نمونه کامل...")
            main()
            
    except KeyboardInterrupt:
        print("\n\n👋 برنامه متوقف شد")
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {str(e)}")