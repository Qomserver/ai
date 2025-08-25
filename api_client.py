# کلاینت API شبکه‌های اجتماعی

import time

class SocialMediaAPIClient:
    """کلاس پایه برای API های شبکه‌های اجتماعی"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def publish_content(self, content):
        """انتشار محتوا (متد پایه)"""
        print(f"انتشار محتوا: {content}")
        return {"status": "success", "message": "محتوا با موفقیت منتشر شد"}

class InstagramAPIClient(SocialMediaAPIClient):
    """کلاینت API اینستاگرام"""
    
    def publish_content(self, content):
        """انتشار محتوا در اینستاگرام"""
        print(f"انتشار در اینستاگرام: {content}")
        return {
            "status": "success",
            "platform": "instagram",
            "post_id": f"ig_{int(time.time())}",
            "message": "محتوا با موفقیت منتشر شد"
        }

class TelegramAPIClient(SocialMediaAPIClient):
    """کلاینت API تلگرام"""
    
    def publish_content(self, content):
        """انتشار محتوا در تلگرام"""
        print(f"انتشار در تلگرام: {content}")
        return {
            "status": "success",
            "platform": "telegram",
            "message_id": f"tg_{int(time.time())}",
            "message": "محتوا با موفقیت ارسال شد"
        }
