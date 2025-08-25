"""
بهینه‌ساز SEO برای محتوای وب‌سایت
"""

import re
import asyncio
from typing import Dict, List, Any, Tuple
from datetime import datetime
import logging

from .models import SEOOptimizationResponse

logger = logging.getLogger(__name__)

class SEOOptimizer:
    """کلاس بهینه‌سازی SEO"""
    
    def __init__(self):
        self.seo_rules = self._load_seo_rules()
        self.stopwords = self._load_persian_stopwords()
    
    def _load_seo_rules(self) -> Dict[str, Any]:
        """بارگذاری قوانین SEO"""
        return {
            "title_length": {"min": 30, "max": 60},
            "meta_description_length": {"min": 120, "max": 160},
            "keyword_density": {"min": 0.5, "max": 3.0},  # درصد
            "heading_structure": {
                "h1_count": 1,
                "h2_min": 2,
                "h3_max": 6
            },
            "content_length": {"min": 300, "max": 3000},
            "internal_links": {"min": 2, "max": 10},
            "image_alt_required": True,
            "readability_score": {"min": 60}  # از ۱۰۰
        }
    
    def _load_persian_stopwords(self) -> List[str]:
        """بارگذاری کلمات پر تکرار فارسی"""
        return [
            "در", "از", "به", "با", "که", "این", "آن", "را", "تا", "و", "یا",
            "است", "بود", "باشد", "شده", "می", "خود", "همه", "یک", "دو",
            "سه", "برای", "روی", "زیر", "بالا", "پایین", "کنار", "وسط"
        ]
    
    async def optimize_content(
        self,
        text: str,
        target_keywords: List[str],
        focus_keyword: str,
        meta_description: str = None,
        title_tag: str = None
    ) -> SEOOptimizationResponse:
        """بهینه‌سازی محتوا برای SEO"""
        
        logger.info(f"شروع بهینه‌سازی SEO برای کلمه کلیدی: {focus_keyword}")
        
        # تجزیه محتوای موجود
        analysis = await self._analyze_content(text, target_keywords, focus_keyword)
        
        # بهینه‌سازی محتوا
        optimized_content = await self._optimize_text_content(
            text, target_keywords, focus_keyword, analysis
        )
        
        # تولید عنوان SEO
        seo_title = await self._generate_seo_title(
            title_tag or focus_keyword, focus_keyword
        )
        
        # تولید متای توضیحات
        optimized_meta = await self._generate_meta_description(
            meta_description or text, focus_keyword, target_keywords
        )
        
        # محاسبه تراکم کلمات کلیدی
        keyword_density = self._calculate_keyword_density(
            optimized_content, target_keywords
        )
        
        # تجزیه ساختار هدینگ‌ها
        headings_structure = self._analyze_headings_structure(optimized_content)
        
        # محاسبه امتیاز SEO
        seo_score = await self._calculate_seo_score(
            optimized_content, seo_title, optimized_meta, 
            keyword_density, headings_structure, focus_keyword
        )
        
        # تولید توصیه‌ها
        recommendations = await self._generate_recommendations(
            analysis, seo_score, keyword_density, headings_structure
        )
        
        # محاسبه امتیاز خوانایی
        readability_score = self._calculate_readability_score(optimized_content)
        
        # شمارش کلمات
        word_count = len(optimized_content.split())
        
        logger.info(f"بهینه‌سازی SEO کامل شد - امتیاز: {seo_score}")
        
        return SEOOptimizationResponse(
            optimized_content=optimized_content,
            seo_title=seo_title,
            meta_description=optimized_meta,
            keywords_density=keyword_density,
            headings_structure=headings_structure,
            seo_score=seo_score,
            recommendations=recommendations,
            readability_score=readability_score,
            word_count=word_count
        )
    
    async def _analyze_content(
        self, text: str, target_keywords: List[str], focus_keyword: str
    ) -> Dict[str, Any]:
        """تجزیه و تحلیل محتوای موجود"""
        
        analysis = {
            "original_length": len(text),
            "word_count": len(text.split()),
            "paragraph_count": len(text.split('\n\n')),
            "sentence_count": len(re.findall(r'[.!؟]+', text)),
            "has_headings": bool(re.search(r'#+\s+', text)),
            "current_keyword_density": {},
            "issues": []
        }
        
        # تحلیل تراکم کلمات کلیدی فعلی
        for keyword in target_keywords + [focus_keyword]:
            density = self._calculate_single_keyword_density(text, keyword)
            analysis["current_keyword_density"][keyword] = density
            
            if density < self.seo_rules["keyword_density"]["min"]:
                analysis["issues"].append(f"تراکم کم کلمه '{keyword}': {density:.1f}%")
            elif density > self.seo_rules["keyword_density"]["max"]:
                analysis["issues"].append(f"تراکم زیاد کلمه '{keyword}': {density:.1f}%")
        
        # بررسی طول محتوا
        if analysis["word_count"] < self.seo_rules["content_length"]["min"]:
            analysis["issues"].append("محتوا کوتاه‌تر از حد استاندارد است")
        elif analysis["word_count"] > self.seo_rules["content_length"]["max"]:
            analysis["issues"].append("محتوا طولانی‌تر از حد توصیه شده است")
        
        return analysis
    
    async def _optimize_text_content(
        self, text: str, target_keywords: List[str], focus_keyword: str, analysis: Dict
    ) -> str:
        """بهینه‌سازی محتوای متنی"""
        
        optimized_text = text
        
        # اضافه کردن ساختار هدینگ در صورت عدم وجود
        if not analysis["has_headings"]:
            optimized_text = self._add_heading_structure(optimized_text, focus_keyword)
        
        # بهینه‌سازی تراکم کلمات کلیدی
        optimized_text = await self._optimize_keyword_density(
            optimized_text, target_keywords, focus_keyword
        )
        
        # اضافه کردن کلمه کلیدی در نقاط مهم
        optimized_text = self._place_keywords_strategically(
            optimized_text, focus_keyword
        )
        
        # بهبود ساختار پاراگراف‌ها
        optimized_text = self._improve_paragraph_structure(optimized_text)
        
        return optimized_text
    
    def _add_heading_structure(self, text: str, focus_keyword: str) -> str:
        """اضافه کردن ساختار هدینگ به محتوا"""
        
        paragraphs = text.split('\n\n')
        
        if len(paragraphs) < 2:
            return text
        
        # افزودن H1 در ابتدا
        structured_text = f"# {focus_keyword} - راهنمای جامع\n\n"
        
        # تبدیل پاراگراف‌ها به بخش‌های مختلف
        for i, paragraph in enumerate(paragraphs):
            if i == 0:
                structured_text += f"## مقدمه\n{paragraph}\n\n"
            elif i == len(paragraphs) - 1:
                structured_text += f"## نتیجه‌گیری\n{paragraph}\n\n"
            else:
                structured_text += f"## بخش {i}\n{paragraph}\n\n"
        
        return structured_text
    
    async def _optimize_keyword_density(
        self, text: str, target_keywords: List[str], focus_keyword: str
    ) -> str:
        """بهینه‌سازی تراکم کلمات کلیدی"""
        
        optimized_text = text
        word_count = len(text.split())
        
        for keyword in target_keywords + [focus_keyword]:
            current_density = self._calculate_single_keyword_density(text, keyword)
            target_density = 2.0 if keyword == focus_keyword else 1.0
            
            if current_density < target_density:
                # اضافه کردن کلمه کلیدی
                additions_needed = int((target_density * word_count / 100) - 
                                     text.lower().count(keyword.lower()))
                
                if additions_needed > 0:
                    optimized_text = self._add_keyword_naturally(
                        optimized_text, keyword, additions_needed
                    )
        
        return optimized_text
    
    def _add_keyword_naturally(self, text: str, keyword: str, count: int) -> str:
        """اضافه کردن طبیعی کلمه کلیدی به متن"""
        
        sentences = text.split('.')
        keyword_variations = self._generate_keyword_variations(keyword)
        
        added = 0
        for i, sentence in enumerate(sentences):
            if added >= count:
                break
            
            # اضافه کردن در جملات مناسب
            if len(sentence.split()) > 5 and keyword.lower() not in sentence.lower():
                variation = keyword_variations[added % len(keyword_variations)]
                sentences[i] = sentence + f" {variation}"
                added += 1
        
        return '.'.join(sentences)
    
    def _generate_keyword_variations(self, keyword: str) -> List[str]:
        """تولید تنوعات کلمه کلیدی"""
        return [
            keyword,
            f"در مورد {keyword}",
            f"برای {keyword}",
            f"راجع به {keyword}",
            f"{keyword} مهم"
        ]
    
    def _place_keywords_strategically(self, text: str, focus_keyword: str) -> str:
        """قرار دادن استراتژیک کلمه کلیدی"""
        
        # در پاراگراف اول
        paragraphs = text.split('\n\n')
        if paragraphs and focus_keyword.lower() not in paragraphs[0].lower():
            paragraphs[0] = f"{focus_keyword} {paragraphs[0]}"
        
        # در پاراگراف آخر
        if len(paragraphs) > 1 and focus_keyword.lower() not in paragraphs[-1].lower():
            paragraphs[-1] = paragraphs[-1] + f" در نهایت، {focus_keyword} بسیار مهم است."
        
        return '\n\n'.join(paragraphs)
    
    def _improve_paragraph_structure(self, text: str) -> str:
        """بهبود ساختار پاراگراف‌ها"""
        
        paragraphs = text.split('\n\n')
        improved_paragraphs = []
        
        for paragraph in paragraphs:
            # تقسیم پاراگراف‌های طولانی
            if len(paragraph.split()) > 100:
                sentences = paragraph.split('.')
                mid_point = len(sentences) // 2
                
                part1 = '.'.join(sentences[:mid_point]) + '.'
                part2 = '.'.join(sentences[mid_point:])
                
                improved_paragraphs.extend([part1.strip(), part2.strip()])
            else:
                improved_paragraphs.append(paragraph.strip())
        
        return '\n\n'.join(improved_paragraphs)
    
    async def _generate_seo_title(self, title: str, focus_keyword: str) -> str:
        """تولید عنوان SEO بهینه"""
        
        rules = self.seo_rules["title_length"]
        
        # اگر عنوان شامل کلمه کلیدی نیست، اضافه کن
        if focus_keyword.lower() not in title.lower():
            title = f"{focus_keyword} - {title}"
        
        # بررسی طول
        if len(title) > rules["max"]:
            # کوتاه کردن با حفظ کلمه کلیدی
            title = title[:rules["max"]-3] + "..."
        elif len(title) < rules["min"]:
            # طولانی کردن
            title += f" | راهنمای کامل {focus_keyword}"
        
        return title.strip()
    
    async def _generate_meta_description(
        self, description: str, focus_keyword: str, target_keywords: List[str]
    ) -> str:
        """تولید متای توضیحات بهینه"""
        
        rules = self.seo_rules["meta_description_length"]
        
        # استخراج جمله اول به عنوان متای توضیحات
        if not description or len(description) > 500:
            first_paragraph = description.split('\n\n')[0] if description else ""
            description = first_paragraph[:200] + "..."
        
        # اطمینان از وجود کلمه کلیدی اصلی
        if focus_keyword.lower() not in description.lower():
            description = f"{focus_keyword}: {description}"
        
        # اضافه کردن کلمات کلیدی دیگر در صورت امکان
        for keyword in target_keywords[:2]:
            if keyword.lower() not in description.lower() and len(description) < rules["max"] - 20:
                description += f" {keyword}"
        
        # تنظیم طول
        if len(description) > rules["max"]:
            description = description[:rules["max"]-3] + "..."
        elif len(description) < rules["min"]:
            description += f" اطلاعات کامل درباره {focus_keyword} و {', '.join(target_keywords[:2])}"
        
        return description.strip()
    
    def _calculate_keyword_density(
        self, text: str, keywords: List[str]
    ) -> Dict[str, float]:
        """محاسبه تراکم کلمات کلیدی"""
        
        density = {}
        
        for keyword in keywords:
            density[keyword] = self._calculate_single_keyword_density(text, keyword)
        
        return density
    
    def _calculate_single_keyword_density(self, text: str, keyword: str) -> float:
        """محاسبه تراکم یک کلمه کلیدی"""
        
        total_words = len(text.split())
        keyword_count = text.lower().count(keyword.lower())
        
        if total_words == 0:
            return 0.0
        
        return round((keyword_count / total_words) * 100, 2)
    
    def _analyze_headings_structure(self, text: str) -> List[Dict[str, Any]]:
        """تجزیه ساختار هدینگ‌ها"""
        
        headings = []
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # شناسایی هدینگ‌های Markdown
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                
                headings.append({
                    "level": level,
                    "title": title,
                    "line_number": line_num,
                    "character_count": len(title)
                })
        
        return headings
    
    async def _calculate_seo_score(
        self, 
        content: str, 
        title: str, 
        meta_description: str,
        keyword_density: Dict[str, float],
        headings_structure: List[Dict],
        focus_keyword: str
    ) -> float:
        """محاسبه امتیاز SEO کلی"""
        
        score = 0.0
        max_score = 100.0
        
        # امتیاز طول محتوا (20 امتیاز)
        word_count = len(content.split())
        if self.seo_rules["content_length"]["min"] <= word_count <= self.seo_rules["content_length"]["max"]:
            score += 20
        elif word_count < self.seo_rules["content_length"]["min"]:
            score += 10
        
        # امتیاز عنوان (15 امتیاز)
        title_len = len(title)
        if self.seo_rules["title_length"]["min"] <= title_len <= self.seo_rules["title_length"]["max"]:
            score += 15
        elif title_len < self.seo_rules["title_length"]["max"]:
            score += 10
        
        # امتیاز متای توضیحات (15 امتیاز)
        meta_len = len(meta_description)
        if self.seo_rules["meta_description_length"]["min"] <= meta_len <= self.seo_rules["meta_description_length"]["max"]:
            score += 15
        elif meta_len < self.seo_rules["meta_description_length"]["max"]:
            score += 10
        
        # امتیاز تراکم کلمات کلیدی (25 امتیاز)
        focus_density = keyword_density.get(focus_keyword, 0)
        if self.seo_rules["keyword_density"]["min"] <= focus_density <= self.seo_rules["keyword_density"]["max"]:
            score += 25
        elif focus_density > 0:
            score += 15
        
        # امتیاز ساختار هدینگ‌ها (15 امتیاز)
        h1_count = len([h for h in headings_structure if h["level"] == 1])
        h2_count = len([h for h in headings_structure if h["level"] == 2])
        
        if h1_count == 1 and h2_count >= 2:
            score += 15
        elif h1_count == 1:
            score += 10
        elif headings_structure:
            score += 5
        
        # امتیاز وجود کلمه کلیدی در عنوان (10 امتیاز)
        if focus_keyword.lower() in title.lower():
            score += 10
        
        return round(min(score, max_score), 1)
    
    async def _generate_recommendations(
        self, 
        analysis: Dict, 
        seo_score: float, 
        keyword_density: Dict,
        headings_structure: List[Dict]
    ) -> List[str]:
        """تولید توصیه‌های بهبود"""
        
        recommendations = []
        
        # توصیه‌های مبتنی بر امتیاز
        if seo_score < 70:
            recommendations.append("امتیاز SEO قابل بهبود است")
        
        # توصیه‌های مبتنی بر مسائل شناسایی شده
        recommendations.extend(analysis["issues"])
        
        # توصیه‌های ساختار هدینگ
        h1_count = len([h for h in headings_structure if h["level"] == 1])
        if h1_count == 0:
            recommendations.append("حداقل یک هدینگ H1 اضافه کنید")
        elif h1_count > 1:
            recommendations.append("فقط یک هدینگ H1 استفاده کنید")
        
        h2_count = len([h for h in headings_structure if h["level"] == 2])
        if h2_count < 2:
            recommendations.append("حداقل ۲ هدینگ H2 برای بهتر سازماندهی محتوا اضافه کنید")
        
        # توصیه‌های تراکم کلمات کلیدی
        for keyword, density in keyword_density.items():
            if density < 0.5:
                recommendations.append(f"تراکم کلمه '{keyword}' را افزایش دهید")
            elif density > 3.0:
                recommendations.append(f"تراکم کلمه '{keyword}' زیاد است، کاهش دهید")
        
        # توصیه‌های عمومی
        if not recommendations:
            recommendations.append("محتوای شما از نظر SEO بهینه است!")
        
        return recommendations[:10]  # حداکثر ۱۰ توصیه
    
    def _calculate_readability_score(self, text: str) -> float:
        """محاسبه امتیاز خوانایی (ساده‌شده برای فارسی)"""
        
        sentences = len(re.findall(r'[.!؟]+', text))
        words = len(text.split())
        
        if sentences == 0:
            return 0.0
        
        avg_sentence_length = words / sentences
        
        # فرمول ساده‌شده برای فارسی
        if avg_sentence_length <= 15:
            score = 90
        elif avg_sentence_length <= 20:
            score = 75
        elif avg_sentence_length <= 25:
            score = 60
        else:
            score = 40
        
        # کاهش امتیاز برای کلمات پیچیده (بیش از ۸ حرف)
        long_words = len([word for word in text.split() if len(word) > 8])
        complexity_penalty = (long_words / words) * 20 if words > 0 else 0
        
        final_score = max(score - complexity_penalty, 0)
        
        return round(final_score, 1)