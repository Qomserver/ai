import google.generativeai as genai
from typing import Dict, Any, List
import json
from config import Config

class GeminiClient:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        
        # تعریف توابع برای Function Calling
        self.functions = self._define_functions()
    
    def _define_functions(self) -> List[Dict[str, Any]]:
        """تعریف توابع قابل فراخوانی برای Gemini"""
        return [
            {
                "name": "generate_content",
                "description": "تولید محتوای متناسب با پلتفرم خاص",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "enum": ["instagram", "telegram", "website", "eitaa", "rubika"],
                            "description": "پلتفرم هدف"
                        },
                        "content_type": {
                            "type": "string",
                            "enum": ["caption", "article", "post", "story"],
                            "description": "نوع محتوا"
                        },
                        "main_text": {
                            "type": "string",
                            "description": "متن اصلی محتوا"
                        },
                        "hashtags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "هشتگ‌های مرتبط"
                        },
                        "emojis": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "اموجی‌های مناسب"
                        },
                        "cta": {
                            "type": "string",
                            "description": "فراخوان به عمل"
                        }
                    },
                    "required": ["platform", "content_type", "main_text"]
                }
            },
            {
                "name": "optimize_for_seo",
                "description": "بهینه‌سازی محتوای وب‌سایت برای SEO",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "عنوان بهینه شده"
                        },
                        "meta_description": {
                            "type": "string",
                            "description": "توضیحات متا"
                        },
                        "headings": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "سرتیترهای H1, H2, H3"
                        },
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "کلمات کلیدی SEO"
                        }
                    },
                    "required": ["title", "meta_description", "headings", "keywords"]
                }
            },
            {
                "name": "generate_visual_idea",
                "description": "تولید ایده بصری برای محتوا",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "image_style": {
                            "type": "string",
                            "description": "سبک تصویر"
                        },
                        "color_scheme": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "رنگ‌بندی پیشنهادی"
                        },
                        "composition": {
                            "type": "string",
                            "description": "ترکیب‌بندی تصویر"
                        },
                        "video_duration": {
                            "type": "integer",
                            "description": "مدت ویدئو (ثانیه)"
                        },
                        "video_style": {
                            "type": "string",
                            "description": "سبک ویدئو"
                        }
                    },
                    "required": ["image_style", "color_scheme", "composition"]
                }
            }
        ]
    
    def generate_content(self, prompt: str) -> Dict[str, Any]:
        """تولید محتوا با استفاده از Gemini"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                },
                tools=self.functions
            )
            
            # پردازش پاسخ و استخراج فراخوانی توابع
            if response.candidates and response.candidates[0].content:
                content = response.candidates[0].content
                
                # بررسی فراخوانی توابع
                if hasattr(content, 'parts') and content.parts:
                    for part in content.parts:
                        if hasattr(part, 'function_call'):
                            return self._process_function_call(part.function_call)
                
                # اگر تابعی فراخوانی نشده، متن معمولی برگردان
                return {"text": content.text}
            
            return {"error": "پاسخ نامعتبر از Gemini"}
            
        except Exception as e:
            return {"error": f"خطا در تولید محتوا: {str(e)}"}
    
    def _process_function_call(self, function_call) -> Dict[str, Any]:
        """پردازش فراخوانی تابع"""
        try:
            function_name = function_call.name
            arguments = json.loads(function_call.args)
            
            return {
                "function_name": function_name,
                "arguments": arguments,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": f"خطا در پردازش فراخوانی تابع: {str(e)}",
                "status": "error"
            }
    
    def generate_multi_platform_content(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """تولید محتوای چندپلتفرمی"""
        prompt = self._create_content_prompt(request_data)
        return self.generate_content(prompt)
    
    def _create_content_prompt(self, request_data: Dict[str, Any]) -> str:
        """ایجاد پرومپت برای تولید محتوا"""
        platforms = ", ".join(request_data.get("platforms", []))
        
        prompt = f"""
        شما یک سیستم هوش مصنوعی تولید محتوا هستید که باید برای پلتفرم‌های {platforms} محتوای بهینه تولید کنید.
        
        موضوع: {request_data.get('topic', '')}
        کلمات کلیدی: {', '.join(request_data.get('keywords', []))}
        مخاطب هدف: {request_data.get('target_audience', '')}
        لحن: {request_data.get('tone', 'professional')}
        زبان: {request_data.get('language', 'persian')}
        
        لطفاً برای هر پلتفرم محتوای مناسب تولید کنید و از توابع تعریف شده استفاده کنید:
        1. برای تولید محتوا از تابع generate_content استفاده کنید
        2. برای بهینه‌سازی SEO از تابع optimize_for_seo استفاده کنید  
        3. برای ایده‌های بصری از تابع generate_visual_idea استفاده کنید
        
        خروجی باید شامل موارد زیر باشد:
        - تحلیل موضوع و ایده‌پردازی
        - محتوای اختصاصی برای هر پلتفرم
        - هشتگ‌های پیشنهادی
        - ایده‌های بصری
        - پیشنهادات CTA
        """
        
        return prompt