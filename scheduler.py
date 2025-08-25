import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from models import Platform, ContentRequest
from content_generator import ContentGenerator
import json
import logging

# تنظیم لاگینگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentScheduler:
    def __init__(self):
        self.content_generator = ContentGenerator()
        self.scheduled_posts = {}
        self.is_running = False
        
    def schedule_post(self, 
                     platform: Platform, 
                     content_request: ContentRequest, 
                     publish_time: datetime,
                     post_id: Optional[str] = None) -> str:
        """زمان‌بندی انتشار پست"""
        
        if not post_id:
            post_id = f"post_{int(time.time())}"
        
        # تولید محتوا
        try:
            content_response = self.content_generator.generate_content(content_request)
            
            # ذخیره اطلاعات پست زمان‌بندی شده
            scheduled_post = {
                "post_id": post_id,
                "platform": platform,
                "content_request": content_request.dict(),
                "content_response": content_response.dict(),
                "publish_time": publish_time.isoformat(),
                "status": "scheduled",
                "created_at": datetime.now().isoformat()
            }
            
            self.scheduled_posts[post_id] = scheduled_post
            
            # زمان‌بندی انتشار
            schedule.every().day.at(publish_time.strftime("%H:%M")).do(
                self._publish_post, post_id
            ).tag(post_id)
            
            logger.info(f"پست {post_id} برای {platform} در ساعت {publish_time} زمان‌بندی شد")
            return post_id
            
        except Exception as e:
            logger.error(f"خطا در زمان‌بندی پست: {str(e)}")
            raise
    
    def schedule_recurring_posts(self, 
                                platform: Platform,
                                content_request: ContentRequest,
                                interval_hours: int,
                                start_time: datetime,
                                end_time: Optional[datetime] = None) -> List[str]:
        """زمان‌بندی پست‌های تکرارشونده"""
        
        post_ids = []
        current_time = start_time
        
        while True:
            if end_time and current_time > end_time:
                break
                
            post_id = f"recurring_{int(current_time.timestamp())}"
            self.schedule_post(platform, content_request, current_time, post_id)
            post_ids.append(post_id)
            
            current_time += timedelta(hours=interval_hours)
            
            # محدودیت تعداد پست‌ها
            if len(post_ids) >= 100:
                break
        
        return post_ids
    
    def schedule_platform_specific_posts(self, 
                                       content_request: ContentRequest,
                                       platform_schedule: Dict[Platform, List[datetime]]) -> Dict[Platform, List[str]]:
        """زمان‌بندی پست‌ها برای پلتفرم‌های مختلف"""
        
        platform_post_ids = {}
        
        for platform, publish_times in platform_schedule.items():
            post_ids = []
            for publish_time in publish_times:
                post_id = f"{platform}_{int(publish_time.timestamp())}"
                self.schedule_post(platform, content_request, publish_time, post_id)
                post_ids.append(post_id)
            
            platform_post_ids[platform] = post_ids
        
        return platform_post_ids
    
    def _publish_post(self, post_id: str):
        """انتشار پست زمان‌بندی شده"""
        
        if post_id not in self.scheduled_posts:
            logger.warning(f"پست {post_id} یافت نشد")
            return
        
        post_data = self.scheduled_posts[post_id]
        
        try:
            # اینجا می‌توانید کد انتشار واقعی را اضافه کنید
            # مثلاً ارسال به API پلتفرم‌ها
            
            logger.info(f"انتشار پست {post_id} برای {post_data['platform']}")
            
            # بروزرسانی وضعیت
            post_data["status"] = "published"
            post_data["published_at"] = datetime.now().isoformat()
            
            # حذف از زمان‌بندی
            schedule.clear(post_id)
            
        except Exception as e:
            logger.error(f"خطا در انتشار پست {post_id}: {str(e)}")
            post_data["status"] = "failed"
            post_data["error"] = str(e)
    
    def cancel_post(self, post_id: str) -> bool:
        """لغو پست زمان‌بندی شده"""
        
        if post_id not in self.scheduled_posts:
            return False
        
        try:
            # حذف از زمان‌بندی
            schedule.clear(post_id)
            
            # بروزرسانی وضعیت
            self.scheduled_posts[post_id]["status"] = "cancelled"
            self.scheduled_posts[post_id]["cancelled_at"] = datetime.now().isoformat()
            
            logger.info(f"پست {post_id} لغو شد")
            return True
            
        except Exception as e:
            logger.error(f"خطا در لغو پست {post_id}: {str(e)}")
            return False
    
    def get_scheduled_posts(self, 
                           platform: Optional[Platform] = None,
                           status: Optional[str] = None) -> List[Dict[str, Any]]:
        """دریافت لیست پست‌های زمان‌بندی شده"""
        
        posts = list(self.scheduled_posts.values())
        
        if platform:
            posts = [p for p in posts if p["platform"] == platform]
        
        if status:
            posts = [p for p in posts if p["status"] == status]
        
        return sorted(posts, key=lambda x: x["publish_time"])
    
    def get_post_status(self, post_id: str) -> Optional[Dict[str, Any]]:
        """دریافت وضعیت پست خاص"""
        return self.scheduled_posts.get(post_id)
    
    def start_scheduler(self):
        """شروع زمان‌بند"""
        if self.is_running:
            logger.warning("زمان‌بند در حال اجرا است")
            return
        
        self.is_running = True
        logger.info("زمان‌بند شروع شد")
        
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
        
        # اجرای زمان‌بند در thread جداگانه
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
    
    def stop_scheduler(self):
        """توقف زمان‌بند"""
        self.is_running = False
        schedule.clear()
        logger.info("زمان‌بند متوقف شد")
    
    def export_schedule(self, file_path: str):
        """صادرات زمان‌بندی به فایل JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.scheduled_posts, f, ensure_ascii=False, indent=2)
            logger.info(f"زمان‌بندی به {file_path} صادر شد")
        except Exception as e:
            logger.error(f"خطا در صادرات زمان‌بندی: {str(e)}")
    
    def import_schedule(self, file_path: str):
        """واردات زمان‌بندی از فایل JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_posts = json.load(f)
            
            # پاک کردن زمان‌بندی فعلی
            schedule.clear()
            self.scheduled_posts.clear()
            
            # واردات پست‌های جدید
            for post_id, post_data in imported_posts.items():
                if post_data["status"] == "scheduled":
                    publish_time = datetime.fromisoformat(post_data["publish_time"])
                    schedule.every().day.at(publish_time.strftime("%H:%M")).do(
                        self._publish_post, post_id
                    ).tag(post_id)
                
                self.scheduled_posts[post_id] = post_data
            
            logger.info(f"زمان‌بندی از {file_path} وارد شد")
            
        except Exception as e:
            logger.error(f"خطا در واردات زمان‌بندی: {str(e)}")

# نمونه استفاده
if __name__ == "__main__":
    scheduler = ContentScheduler()
    
    # شروع زمان‌بند
    scheduler.start_scheduler()
    
    try:
        # نگه داشتن برنامه در حال اجرا
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop_scheduler()
        print("زمان‌بند متوقف شد")