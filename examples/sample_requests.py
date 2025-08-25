"""
نمونه‌های استفاده از سیستم تولید محتوای هوش مصنوعی
"""

import requests
import json
from datetime import datetime, timedelta

# آدرس سرور (در صورت اجرا در محیط محلی)
BASE_URL = "http://localhost:8000/api"

def example_generate_content():
    """نمونه تولید محتوا برای چند پلتفرم"""
    
    payload = {
        "topic": "فواید یادگیری هوش مصنوعی",
        "keywords": ["هوش مصنوعی", "یادگیری ماشین", "فناوری", "آینده"],
        "platforms": ["instagram", "telegram", "website"],
        "content_type": "post",
        "tone": "educational",
        "target_audience": "دانشجویان و علاقه‌مندان فناوری"
    }
    
    response = requests.post(f"{BASE_URL}/generate-content", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        
        print("✅ محتوا با موفقیت تولید شد!")
        print(f"📊 تعداد پلتفرم‌ها: {result['total_platforms']}")
        print(f"🕐 زمان تولید: {result['generated_at']}")
        
        # نمایش محتوا برای هر پلتفرم
        for platform, content in result['contents'].items():
            print(f"\n📱 {platform.upper()}:")
            print("-" * 50)
            if isinstance(content, dict):
                print(content['content'])
                print(f"📏 تعداد کاراکتر: {content.get('character_count', 0)}")
                print(f"⭐ امتیاز جذابیت: {content.get('engagement_score', 0)}/10")
            else:
                print(content)
        
        # نمایش هشتگ‌ها
        print(f"\n🏷️ هشتگ‌های پیشنهادی:")
        for platform, hashtags in result['hashtags'].items():
            print(f"{platform}: {' '.join(hashtags[:5])}")
        
        # نمایش پیشنهادات CTA
        print(f"\n📢 پیشنهادات فراخوان عمل:")
        for cta in result['cta_suggestions'][:3]:
            print(f"• {cta}")
            
        return result
    else:
        print(f"❌ خطا: {response.status_code}")
        print(response.text)

def example_optimize_seo():
    """نمونه بهینه‌سازی SEO"""
    
    sample_text = """
    هوش مصنوعی یکی از مهم‌ترین فناوری‌های قرن حاضر است. 
    این فناوری در حال تغییر دادن دنیای ما است و کاربردهای فراوانی دارد.
    یادگیری ماشین بخش مهمی از هوش مصنوعی محسوب می‌شود.
    """
    
    payload = {
        "text": sample_text,
        "target_keywords": ["هوش مصنوعی", "یادگیری ماشین", "فناوری"],
        "focus_keyword": "هوش مصنوعی",
        "meta_description": "راهنمای جامع هوش مصنوعی و کاربردهای آن"
    }
    
    response = requests.post(f"{BASE_URL}/optimize-seo", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        
        print("✅ بهینه‌سازی SEO انجام شد!")
        print(f"🎯 امتیاز SEO: {result['seo_score']}/100")
        print(f"📖 امتیاز خوانایی: {result['readability_score']}/100")
        print(f"📝 تعداد کلمات: {result['word_count']}")
        
        print(f"\n📊 تراکم کلمات کلیدی:")
        for keyword, density in result['keywords_density'].items():
            print(f"• {keyword}: {density}%")
        
        print(f"\n💡 توصیه‌های بهبود:")
        for recommendation in result['recommendations'][:5]:
            print(f"• {recommendation}")
            
        return result
    else:
        print(f"❌ خطا: {response.status_code}")
        print(response.text)

def example_generate_visual_ideas():
    """نمونه تولید ایده‌های بصری"""
    
    sample_content = """
    ۵ نکته طلایی برای شروع یادگیری هوش مصنوعی:
    1. پایه‌های ریاضی را تقویت کنید
    2. زبان برنامه‌نویسی Python یاد بگیرید
    3. با کتابخانه‌های معروف آشنا شوید
    4. پروژه‌های عملی انجام دهید
    5. در جامعه فعال باشید
    """
    
    payload = {
        "content": sample_content,
        "platform": "instagram",
        "content_type": "post",
        "style_preferences": ["modern", "colorful"]
    }
    
    response = requests.post(f"{BASE_URL}/generate-visual-idea", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        
        print("✅ ایده‌های بصری تولید شدند!")
        
        print(f"\n🖼️ ایده‌های تصویری:")
        for i, idea in enumerate(result['image_ideas'], 1):
            print(f"{i}. سبک: {idea['style']}")
            print(f"   توضیح: {idea['description']}")
            print(f"   چیدمان: {idea['layout']}")
        
        print(f"\n🎬 ایده‌های ویدئویی:")
        for i, idea in enumerate(result['video_ideas'], 1):
            print(f"{i}. نوع: {idea['type']}")
            print(f"   مدت: {idea['duration']}")
            print(f"   سبک: {idea['style']}")
        
        print(f"\n🎨 رنگ‌های پیشنهادی:")
        print(" ".join(result['color_suggestions'][:5]))
        
        return result
    else:
        print(f"❌ خطا: {response.status_code}")
        print(response.text)

def example_schedule_content():
    """نمونه زمان‌بندی محتوا"""
    
    # زمان انتشار: یک ساعت بعد
    schedule_time = datetime.now() + timedelta(hours=1)
    
    payload = {
        "platform": "telegram",
        "content": "🚀 محتوای تست برای زمان‌بندی!\n\nاین پست به صورت خودکار منتشر می‌شود.",
        "schedule_time": schedule_time.isoformat(),
        "auto_publish": True
    }
    
    response = requests.post(f"{BASE_URL}/schedule-post", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        
        print("✅ محتوا زمان‌بندی شد!")
        print(f"🆔 شناسه: {result['schedule_id']}")
        print(f"⏰ زمان انتشار: {result['scheduled_time']}")
        
        return result
    else:
        print(f"❌ خطا: {response.status_code}")
        print(response.text)

def example_get_scheduled_posts():
    """نمونه دریافت پست‌های زمان‌بندی شده"""
    
    response = requests.get(f"{BASE_URL}/scheduled-posts")
    
    if response.status_code == 200:
        posts = response.json()
        
        print(f"📋 تعداد پست‌های زمان‌بندی شده: {len(posts)}")
        
        for post in posts[:5]:  # نمایش ۵ پست اول
            print(f"\n🆔 {post['id']}")
            print(f"📱 پلتفرم: {post['platform']}")
            print(f"📄 محتوا: {post['content'][:50]}...")
            print(f"📅 زمان: {post['schedule_time']}")
            print(f"🔘 وضعیت: {post['status']}")
        
        return posts
    else:
        print(f"❌ خطا: {response.status_code}")
        print(response.text)

def example_get_stats():
    """نمونه دریافت آمار سیستم"""
    
    response = requests.get(f"{BASE_URL}/stats")
    
    if response.status_code == 200:
        stats = response.json()
        
        print("📊 آمار سیستم:")
        print(f"📝 محتوای تولید شده: {stats.get('total_generated_contents', 0)}")
        print(f"⏰ زمان‌بندی شده: {stats.get('scheduled_posts_count', 0)}")
        print(f"📱 پلتفرم‌های فعال: {stats.get('active_platforms', 0)}")
        
        return stats
    else:
        print(f"❌ خطا: {response.status_code}")
        print(response.text)

def run_all_examples():
    """اجرای تمام نمونه‌ها"""
    
    print("🤖 شروع نمایش نمونه‌های سیستم تولید محتوای هوش مصنوعی")
    print("=" * 60)
    
    try:
        print("\n1️⃣ تولید محتوا:")
        example_generate_content()
        
        print("\n2️⃣ بهینه‌سازی SEO:")
        example_optimize_seo()
        
        print("\n3️⃣ تولید ایده‌های بصری:")
        example_generate_visual_ideas()
        
        print("\n4️⃣ زمان‌بندی محتوا:")
        example_schedule_content()
        
        print("\n5️⃣ دریافت پست‌های زمان‌بندی شده:")
        example_get_scheduled_posts()
        
        print("\n6️⃣ آمار سیستم:")
        example_get_stats()
        
    except requests.exceptions.ConnectionError:
        print("❌ خطا: نمی‌توان به سرور متصل شد.")
        print("🔧 لطفاً مطمئن شوید که سرور در حال اجرا است:")
        print("   python main.py")
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")

if __name__ == "__main__":
    run_all_examples()