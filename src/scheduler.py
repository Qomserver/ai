"""
سیستم زمان‌بندی انتشار محتوا
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import schedule
import time
from threading import Thread

from .platforms import PlatformType
from .models import ScheduledPost

logger = logging.getLogger(__name__)

class ContentScheduler:
    """کلاس زمان‌بندی انتشار محتوا"""
    
    def __init__(self):
        self.scheduled_posts: Dict[str, ScheduledPost] = {}
        self.is_running = False
        self.scheduler_thread = None
        self.api_connections = self._initialize_api_connections()
    
    def _initialize_api_connections(self) -> Dict[PlatformType, Any]:
        """مقداردهی اولیه اتصالات API"""
        # در اینجا می‌توانید API کلاینت‌های واقعی را تعریف کنید
        return {
            PlatformType.INSTAGRAM: None,  # Instagram Basic Display API
            PlatformType.TELEGRAM: None,   # Telegram Bot API
            PlatformType.EITAA: None,      # Eitaa API
            PlatformType.RUBIKA: None,     # Rubika API
            PlatformType.WEBSITE: None     # Custom CMS API
        }
    
    async def start(self):
        """شروع سیستم زمان‌بندی"""
        if not self.is_running:
            self.is_running = True
            self.scheduler_thread = Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            logger.info("🚀 سیستم زمان‌بندی راه‌اندازی شد")
    
    async def stop(self):
        """توقف سیستم زمان‌بندی"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        logger.info("⛔ سیستم زمان‌بندی متوقف شد")
    
    def _run_scheduler(self):
        """اجرای scheduler در thread جداگانه"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
    
    async def schedule_content(
        self,
        platform: PlatformType,
        content: str,
        schedule_time: datetime,
        auto_publish: bool = False,
        repeat_schedule: Optional[str] = None,
        tags: List[str] = None
    ) -> str:
        """زمان‌بندی محتوا برای انتشار"""
        
        # ایجاد شناسه یکتا
        schedule_id = str(uuid.uuid4())
        
        # ایجاد پست زمان‌بندی شده
        scheduled_post = ScheduledPost(
            id=schedule_id,
            platform=platform,
            content=content,
            schedule_time=schedule_time,
            status="scheduled",
            created_at=datetime.now(),
            tags=tags or []
        )
        
        # ذخیره در حافظه (در پروداکشن از دیتابیس استفاده کنید)
        self.scheduled_posts[schedule_id] = scheduled_post
        
        # تنظیم زمان‌بندی
        if auto_publish:
            await self._set_schedule_task(schedule_id, schedule_time)
        
        # تنظیم زمان‌بندی تکراری در صورت نیاز
        if repeat_schedule:
            await self._set_recurring_schedule(schedule_id, repeat_schedule)
        
        logger.info(f"محتوا برای {platform.value} در {schedule_time} زمان‌بندی شد")
        
        return schedule_id
    
    async def _set_schedule_task(self, schedule_id: str, schedule_time: datetime):
        """تنظیم تسک زمان‌بندی"""
        
        def publish_job():
            asyncio.create_task(self.execute_scheduled_post(schedule_id))
        
        # محاسبه تاخیر تا زمان انتشار
        delay = (schedule_time - datetime.now()).total_seconds()
        
        if delay > 0:
            # برنامه‌ریزی برای اجرا در زمان مشخص
            schedule.every().day.at(schedule_time.strftime("%H:%M")).do(publish_job)
            
            # برای زمان‌بندی یکباره، پس از اجرا حذف شود
            def one_time_job():
                publish_job()
                schedule.cancel_job(one_time_job)
            
            schedule.every().day.at(schedule_time.strftime("%H:%M")).do(one_time_job)
    
    async def _set_recurring_schedule(self, schedule_id: str, repeat_pattern: str):
        """تنظیم زمان‌بندی تکراری"""
        
        def recurring_job():
            asyncio.create_task(self.execute_scheduled_post(schedule_id))
        
        # تفسیر الگوی تکرار
        if repeat_pattern == "daily":
            schedule.every().day.do(recurring_job)
        elif repeat_pattern == "weekly":
            schedule.every().week.do(recurring_job)
        elif repeat_pattern == "monthly":
            schedule.every(30).days.do(recurring_job)
        elif repeat_pattern.startswith("every_"):
            # مثال: every_2_hours
            parts = repeat_pattern.split("_")
            if len(parts) == 3:
                interval = int(parts[1])
                unit = parts[2]
                
                if unit == "hours":
                    schedule.every(interval).hours.do(recurring_job)
                elif unit == "days":
                    schedule.every(interval).days.do(recurring_job)
    
    async def execute_scheduled_post(self, schedule_id: str):
        """اجرای انتشار محتوای زمان‌بندی شده"""
        
        if schedule_id not in self.scheduled_posts:
            logger.error(f"پست با شناسه {schedule_id} یافت نشد")
            return
        
        scheduled_post = self.scheduled_posts[schedule_id]
        
        try:
            logger.info(f"شروع انتشار محتوا: {schedule_id}")
            
            # انتشار محتوا بر اساس پلتفرم
            success = await self._publish_to_platform(
                platform=scheduled_post.platform,
                content=scheduled_post.content,
                schedule_id=schedule_id
            )
            
            if success:
                # بروزرسانی وضعیت
                scheduled_post.status = "published"
                scheduled_post.published_at = datetime.now()
                logger.info(f"محتوا با موفقیت منتشر شد: {schedule_id}")
            else:
                scheduled_post.status = "failed"
                scheduled_post.error_message = "خطا در انتشار محتوا"
                logger.error(f"خطا در انتشار محتوا: {schedule_id}")
        
        except Exception as e:
            scheduled_post.status = "failed"
            scheduled_post.error_message = str(e)
            logger.error(f"خطای غیرمنتظره در انتشار: {e}")
    
    async def _publish_to_platform(
        self, platform: PlatformType, content: str, schedule_id: str
    ) -> bool:
        """انتشار محتوا در پلتفرم مشخص"""
        
        try:
            if platform == PlatformType.INSTAGRAM:
                return await self._publish_to_instagram(content)
            elif platform == PlatformType.TELEGRAM:
                return await self._publish_to_telegram(content)
            elif platform == PlatformType.EITAA:
                return await self._publish_to_eitaa(content)
            elif platform == PlatformType.RUBIKA:
                return await self._publish_to_rubika(content)
            elif platform == PlatformType.WEBSITE:
                return await self._publish_to_website(content)
            else:
                logger.warning(f"پلتفرم {platform.value} پشتیبانی نمی‌شود")
                return False
        
        except Exception as e:
            logger.error(f"خطا در انتشار به {platform.value}: {e}")
            return False
    
    async def _publish_to_instagram(self, content: str) -> bool:
        """انتشار در اینستاگرام"""
        
        # در اینجا کد اتصال به Instagram API
        # مثال ساده:
        logger.info("انتشار در اینستاگرام: محتوا آماده انتشار")
        
        # شبیه‌سازی انتشار
        await asyncio.sleep(1)
        
        # در حالت واقعی:
        # instagram_api = self.api_connections[PlatformType.INSTAGRAM]
        # result = await instagram_api.create_post(content)
        # return result.success
        
        return True  # شبیه‌سازی موفقیت
    
    async def _publish_to_telegram(self, content: str) -> bool:
        """انتشار در تلگرام"""
        
        logger.info("انتشار در تلگرام: محتوا آماده انتشار")
        
        # شبیه‌سازی انتشار
        await asyncio.sleep(1)
        
        # در حالت واقعی:
        # telegram_bot = self.api_connections[PlatformType.TELEGRAM]
        # result = await telegram_bot.send_message(chat_id=CHANNEL_ID, text=content)
        # return result.message_id is not None
        
        return True
    
    async def _publish_to_eitaa(self, content: str) -> bool:
        """انتشار در ایتا"""
        
        logger.info("انتشار در ایتا: محتوا آماده انتشار")
        await asyncio.sleep(1)
        return True
    
    async def _publish_to_rubika(self, content: str) -> bool:
        """انتشار در روبیکا"""
        
        logger.info("انتشار در روبیکا: محتوا آماده انتشار")
        await asyncio.sleep(1)
        return True
    
    async def _publish_to_website(self, content: str) -> bool:
        """انتشار در وب‌سایت"""
        
        logger.info("انتشار در وب‌سایت: محتوا آماده انتشار")
        await asyncio.sleep(1)
        return True
    
    async def get_scheduled_posts(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """دریافت لیست پست‌های زمان‌بندی شده"""
        
        posts = list(self.scheduled_posts.values())
        
        # فیلتر بر اساس وضعیت
        if status:
            posts = [post for post in posts if post.status == status]
        
        # مرتب‌سازی بر اساس زمان زمان‌بندی
        posts.sort(key=lambda x: x.schedule_time, reverse=True)
        
        # تبدیل به دیکشنری برای پاسخ API
        result = []
        for post in posts:
            result.append({
                "id": post.id,
                "platform": post.platform.value,
                "content": post.content[:100] + "..." if len(post.content) > 100 else post.content,
                "schedule_time": post.schedule_time.isoformat(),
                "status": post.status,
                "created_at": post.created_at.isoformat(),
                "published_at": post.published_at.isoformat() if post.published_at else None,
                "error_message": post.error_message,
                "tags": post.tags
            })
        
        return result
    
    async def cancel_scheduled_post(self, schedule_id: str) -> Dict[str, Any]:
        """لغو پست زمان‌بندی شده"""
        
        if schedule_id not in self.scheduled_posts:
            return {
                "success": False,
                "message": "پست یافت نشد"
            }
        
        scheduled_post = self.scheduled_posts[schedule_id]
        
        if scheduled_post.status == "published":
            return {
                "success": False,
                "message": "پست قبلاً منتشر شده است"
            }
        
        # تغییر وضعیت به لغو شده
        scheduled_post.status = "cancelled"
        
        # حذف از scheduler (در صورت وجود)
        # schedule.cancel_job() برای job های مربوطه
        
        logger.info(f"پست {schedule_id} لغو شد")
        
        return {
            "success": True,
            "message": "پست با موفقیت لغو شد"
        }
    
    async def get_scheduled_count(self) -> int:
        """تعداد پست‌های زمان‌بندی شده"""
        return len([post for post in self.scheduled_posts.values() if post.status == "scheduled"])
    
    async def get_publishing_stats(self) -> Dict[str, Any]:
        """آمار انتشار"""
        
        total_posts = len(self.scheduled_posts)
        published_posts = len([post for post in self.scheduled_posts.values() if post.status == "published"])
        failed_posts = len([post for post in self.scheduled_posts.values() if post.status == "failed"])
        scheduled_posts = len([post for post in self.scheduled_posts.values() if post.status == "scheduled"])
        
        # آمار بر اساس پلتفرم
        platform_stats = {}
        for platform in PlatformType:
            platform_posts = [post for post in self.scheduled_posts.values() if post.platform == platform]
            platform_stats[platform.value] = {
                "total": len(platform_posts),
                "published": len([post for post in platform_posts if post.status == "published"]),
                "failed": len([post for post in platform_posts if post.status == "failed"]),
                "scheduled": len([post for post in platform_posts if post.status == "scheduled"])
            }
        
        return {
            "total_posts": total_posts,
            "published_posts": published_posts,
            "failed_posts": failed_posts,
            "scheduled_posts": scheduled_posts,
            "success_rate": (published_posts / total_posts * 100) if total_posts > 0 else 0,
            "platform_stats": platform_stats
        }
    
    async def reschedule_post(self, schedule_id: str, new_schedule_time: datetime) -> Dict[str, Any]:
        """تغییر زمان انتشار پست"""
        
        if schedule_id not in self.scheduled_posts:
            return {
                "success": False,
                "message": "پست یافت نشد"
            }
        
        scheduled_post = self.scheduled_posts[schedule_id]
        
        if scheduled_post.status != "scheduled":
            return {
                "success": False,
                "message": "فقط پست‌های زمان‌بندی شده قابل تغییر هستند"
            }
        
        # بروزرسانی زمان
        old_time = scheduled_post.schedule_time
        scheduled_post.schedule_time = new_schedule_time
        
        # بروزرسانی scheduler
        await self._set_schedule_task(schedule_id, new_schedule_time)
        
        logger.info(f"زمان پست {schedule_id} از {old_time} به {new_schedule_time} تغییر کرد")
        
        return {
            "success": True,
            "message": "زمان انتشار با موفقیت تغییر کرد",
            "old_time": old_time.isoformat(),
            "new_time": new_schedule_time.isoformat()
        }
    
    async def bulk_schedule(self, posts_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """زمان‌بندی انبوه محتوا"""
        
        results = {
            "successful": [],
            "failed": [],
            "total": len(posts_data)
        }
        
        for post_data in posts_data:
            try:
                schedule_id = await self.schedule_content(
                    platform=PlatformType(post_data["platform"]),
                    content=post_data["content"],
                    schedule_time=datetime.fromisoformat(post_data["schedule_time"]),
                    auto_publish=post_data.get("auto_publish", False),
                    tags=post_data.get("tags", [])
                )
                
                results["successful"].append({
                    "schedule_id": schedule_id,
                    "platform": post_data["platform"]
                })
                
            except Exception as e:
                results["failed"].append({
                    "platform": post_data.get("platform", "unknown"),
                    "error": str(e)
                })
        
        return results
    
    async def get_optimal_posting_times(self, platform: PlatformType) -> List[str]:
        """دریافت بهترین زمان‌های انتشار برای پلتفرم"""
        
        optimal_times = {
            PlatformType.INSTAGRAM: ["09:00", "12:00", "17:00", "20:00"],
            PlatformType.TELEGRAM: ["08:00", "13:00", "18:00", "21:00"],
            PlatformType.EITAA: ["10:00", "14:00", "19:00", "22:00"],
            PlatformType.RUBIKA: ["11:00", "15:00", "20:00", "23:00"],
            PlatformType.WEBSITE: ["09:00", "14:00", "16:00", "19:00"]
        }
        
        return optimal_times.get(platform, ["12:00", "18:00"])
    
    async def analyze_best_posting_time(self, platform: PlatformType) -> Dict[str, Any]:
        """تحلیل بهترین زمان انتشار بر اساس عملکرد گذشته"""
        
        # در اینجا می‌توانید از دیتای واقعی استفاده کنید
        # فعلاً داده‌های نمونه ارائه می‌دهیم
        
        analysis = {
            "platform": platform.value,
            "recommended_times": await self.get_optimal_posting_times(platform),
            "peak_engagement_hours": {
                "weekday": ["12:00-13:00", "19:00-21:00"],
                "weekend": ["10:00-12:00", "20:00-22:00"]
            },
            "avoid_times": ["02:00-06:00", "23:00-01:00"],
            "best_days": ["دوشنبه", "سه‌شنبه", "پنج‌شنبه"],
            "engagement_rate_by_hour": {
                "08:00": 65,
                "12:00": 85,
                "18:00": 92,
                "21:00": 78
            }
        }
        
        return analysis