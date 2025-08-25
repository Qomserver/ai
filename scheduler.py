# زمان‌بند محتوا

import time
import json
from datetime import datetime, timedelta

class ContentScheduler:
    def __init__(self):
        self.scheduled_posts = {}
    
    def schedule_post(self, platform, content, scheduled_time):
        """زمان‌بندی انتشار محتوا"""
        post_id = f"{platform}_{int(time.time())}"
        self.scheduled_posts[post_id] = {
            "platform": platform,
            "content": content,
            "scheduled_time": scheduled_time.isoformat() if hasattr(scheduled_time, 'isoformat') else str(scheduled_time),
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        return post_id
    
    def get_scheduled_posts(self):
        """دریافت لیست انتشارات زمان‌بندی شده"""
        return list(self.scheduled_posts.values())
    
    def cancel_post(self, post_id):
        """لغو انتشار"""
        if post_id in self.scheduled_posts:
            self.scheduled_posts[post_id]["status"] = "cancelled"
            return True
        return False
