"""
Thinking Module - وحدة التفكير
==============================

طبقة التفكير الأساسية لتحليل وتحسين الطلبات
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import re


@dataclass
class AnalysisResult:
    """نتيجة التحليل"""
    style: str
    mood: str
    elements: List[str]
    colors: List[str]
    language: str
    complexity: str


class ThinkingLayer:
    """
    طبقة التفكير الأساسية
    
    تحلل الطلبات وتحسّنها للحصول على نتائج أفضل
    """
    
    # خريطة الأنماط
    STYLE_KEYWORDS = {
        "logo": ["شعار", "لوجو", "logo", "brand", "علامة"],
        "illustration": ["رسم", "توضيح", "illustration", "drawing"],
        "photo": ["صورة", "فوتو", "photo", "realistic", "واقعي"],
        "poster": ["بوستر", "ملصق", "poster", "banner", "إعلان"],
        "icon": ["أيقونة", "icon", "رمز"],
        "pattern": ["نقش", "زخرفة", "pattern", "نمط"]
    }
    
    # خريطة المزاج
    MOOD_KEYWORDS = {
        "professional": ["احترافي", "professional", "رسمي", "formal"],
        "playful": ["مرح", "playful", "fun", "ممتع"],
        "elegant": ["أنيق", "elegant", "راقي", "فاخر"],
        "modern": ["عصري", "modern", "حديث"],
        "traditional": ["تقليدي", "traditional", "كلاسيكي", "تراثي"],
        "minimalist": ["بسيط", "minimalist", "minimal"]
    }
    
    # قوالب التحسين
    ENHANCEMENT_TEMPLATES = {
        "logo": "Professional logo design, {elements}, clean vector style, {mood} aesthetic, {colors}",
        "illustration": "Detailed illustration of {elements}, {mood} style, {colors}, high quality artwork",
        "photo": "Professional photograph of {elements}, {mood} lighting, {colors} color palette",
        "poster": "Eye-catching poster design featuring {elements}, {mood} design, {colors}",
        "default": "High quality {style} of {elements}, {mood} style, {colors}"
    }
    
    def __init__(self):
        self.analysis_cache = {}
    
    def analyze(self, prompt: str) -> AnalysisResult:
        """تحليل الطلب"""
        # اكتشاف اللغة
        language = self._detect_language(prompt)
        
        # اكتشاف النمط
        style = self._detect_style(prompt)
        
        # اكتشاف المزاج
        mood = self._detect_mood(prompt)
        
        # استخراج العناصر
        elements = self._extract_elements(prompt)
        
        # استخراج الألوان
        colors = self._extract_colors(prompt)
        
        # تقدير التعقيد
        complexity = self._estimate_complexity(prompt)
        
        return AnalysisResult(
            style=style,
            mood=mood,
            elements=elements,
            colors=colors,
            language=language,
            complexity=complexity
        )
    
    def enhance_prompt(self, prompt: str) -> str:
        """تحسين الطلب"""
        analysis = self.analyze(prompt)
        
        # اختيار القالب
        template = self.ENHANCEMENT_TEMPLATES.get(
            analysis.style, 
            self.ENHANCEMENT_TEMPLATES["default"]
        )
        
        # بناء الوصف المحسّن
        elements_str = ", ".join(analysis.elements) if analysis.elements else prompt
        colors_str = ", ".join(analysis.colors) if analysis.colors else "harmonious colors"
        
        enhanced = template.format(
            style=analysis.style,
            elements=elements_str,
            mood=analysis.mood,
            colors=colors_str
        )
        
        # إضافة جودة
        enhanced += ". High resolution, detailed, professional quality."
        
        return enhanced
    
    def think(self, prompt: str) -> Dict[str, Any]:
        """عملية التفكير الكاملة"""
        analysis = self.analyze(prompt)
        enhanced = self.enhance_prompt(prompt)
        
        # اقتراح المفاهيم
        concepts = self._suggest_concepts(analysis)
        
        # إعدادات التوليد
        gen_config = self._suggest_generation_config(analysis)
        
        return {
            "analysis": analysis,
            "enhanced_prompt": enhanced,
            "concepts_to_activate": concepts,
            "generation_config": gen_config
        }
    
    def _detect_language(self, text: str) -> str:
        """اكتشاف لغة النص"""
        arabic_pattern = re.compile(r'[\u0600-\u06FF]')
        arabic_chars = len(arabic_pattern.findall(text))
        total_chars = len(text.replace(" ", ""))
        
        if total_chars == 0:
            return "en"
        
        arabic_ratio = arabic_chars / total_chars
        
        if arabic_ratio > 0.5:
            return "ar"
        elif arabic_ratio > 0.1:
            return "mixed"
        return "en"
    
    def _detect_style(self, prompt: str) -> str:
        """اكتشاف النمط"""
        prompt_lower = prompt.lower()
        
        for style, keywords in self.STYLE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    return style
        
        return "illustration"
    
    def _detect_mood(self, prompt: str) -> str:
        """اكتشاف المزاج"""
        prompt_lower = prompt.lower()
        
        for mood, keywords in self.MOOD_KEYWORDS.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    return mood
        
        return "professional"
    
    def _extract_elements(self, prompt: str) -> List[str]:
        """استخراج العناصر"""
        # إزالة الكلمات الشائعة
        stop_words = ["أريد", "اريد", "صمم", "اصنع", "i want", "create", "make", "design"]
        
        elements = prompt
        for word in stop_words:
            elements = elements.replace(word, "")
        
        # تنظيف
        elements = elements.strip()
        
        if elements:
            return [elements]
        return [prompt]
    
    def _extract_colors(self, prompt: str) -> List[str]:
        """استخراج الألوان"""
        color_keywords = {
            "أحمر": "red", "أزرق": "blue", "أخضر": "green",
            "أصفر": "yellow", "برتقالي": "orange", "بنفسجي": "purple",
            "أسود": "black", "أبيض": "white", "ذهبي": "gold",
            "فضي": "silver", "بني": "brown"
        }
        
        colors = []
        prompt_lower = prompt.lower()
        
        for ar, en in color_keywords.items():
            if ar in prompt or en in prompt_lower:
                colors.append(en)
        
        return colors if colors else ["harmonious"]
    
    def _estimate_complexity(self, prompt: str) -> str:
        """تقدير تعقيد الطلب"""
        word_count = len(prompt.split())
        
        if word_count < 5:
            return "simple"
        elif word_count < 15:
            return "medium"
        return "complex"
    
    def _suggest_concepts(self, analysis: AnalysisResult) -> List[Tuple[str, float]]:
        """اقتراح المفاهيم للتفعيل"""
        concepts = []
        
        # حسب النمط
        if analysis.style == "logo":
            concepts.append(("professional", 0.8))
            concepts.append(("minimalist", 0.5))
        elif analysis.style == "illustration":
            concepts.append(("artistic", 0.7))
            concepts.append(("detailed", 0.6))
        
        # حسب اللغة
        if analysis.language in ["ar", "mixed"]:
            concepts.append(("arabic_style", 0.6))
        
        # حسب المزاج
        if analysis.mood == "traditional":
            concepts.append(("traditional", 0.7))
        elif analysis.mood == "modern":
            concepts.append(("modern", 0.7))
        
        return concepts
    
    def _suggest_generation_config(self, analysis: AnalysisResult) -> Dict[str, Any]:
        """اقتراح إعدادات التوليد"""
        config = {
            "num_inference_steps": 50,
            "guidance_scale": 7.5,
            "width": 512,
            "height": 512
        }
        
        # تعديل حسب النمط
        if analysis.style == "logo":
            config["guidance_scale"] = 8.0
        elif analysis.style == "photo":
            config["num_inference_steps"] = 75
        elif analysis.style == "poster":
            config["width"] = 768
            config["height"] = 1024
        
        # تعديل حسب التعقيد
        if analysis.complexity == "complex":
            config["num_inference_steps"] = 75
        
        return config
