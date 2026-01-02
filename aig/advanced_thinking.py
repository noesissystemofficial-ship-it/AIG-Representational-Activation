"""
Advanced Thinking Module - وحدة التفكير المتقدم
===============================================

تفكير متعدد المستويات مع دعم LLM
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from .thinking import ThinkingLayer, AnalysisResult


@dataclass
class ThoughtResult:
    """نتيجة عملية التفكير"""
    original_input: str
    understanding: str
    enhanced_prompt: str
    selected_concepts: List[Tuple[str, float]]
    steering_strategy: str
    reasoning: Optional[str] = None
    creative_variations: Optional[List[str]] = None


class AdvancedThinkingLayer:
    """
    طبقة التفكير المتقدم
    
    تدمج التفكير الأساسي مع LLM للحصول على نتائج أفضل
    """
    
    def __init__(self, 
                 enable_llm: bool = False,
                 enable_creative: bool = True,
                 llm_client: Optional[Any] = None):
        
        self.basic_thinking = ThinkingLayer()
        self.enable_llm = enable_llm
        self.enable_creative = enable_creative
        self.llm_client = llm_client
    
    def think(self, prompt: str, depth: str = "standard") -> ThoughtResult:
        """
        عملية التفكير المتقدم
        
        Args:
            prompt: الطلب الأصلي
            depth: عمق التفكير (quick, standard, deep)
        
        Returns:
            نتيجة التفكير
        """
        # التحليل الأساسي
        analysis = self.basic_thinking.analyze(prompt)
        basic_result = self.basic_thinking.think(prompt)
        
        # بناء الفهم
        understanding = self._build_understanding(prompt, analysis)
        
        # تحسين الـ prompt
        enhanced = basic_result["enhanced_prompt"]
        
        # اختيار المفاهيم
        concepts = self._select_concepts(analysis, basic_result["concepts_to_activate"])
        
        # اختيار استراتيجية التوجيه
        strategy = self._select_strategy(analysis)
        
        # التفكير الإبداعي
        creative_variations = None
        reasoning = None
        
        if self.enable_creative and depth in ["standard", "deep"]:
            creative_variations = self._generate_variations(prompt, analysis)
            reasoning = self._generate_reasoning(prompt, analysis, concepts)
        
        return ThoughtResult(
            original_input=prompt,
            understanding=understanding,
            enhanced_prompt=enhanced,
            selected_concepts=concepts,
            steering_strategy=strategy,
            reasoning=reasoning,
            creative_variations=creative_variations
        )
    
    def _build_understanding(self, prompt: str, analysis: AnalysisResult) -> str:
        """بناء وصف الفهم"""
        parts = []
        
        # النمط
        style_names = {
            "logo": "تصميم شعار",
            "illustration": "رسم توضيحي",
            "photo": "صورة فوتوغرافية",
            "poster": "ملصق إعلاني",
            "icon": "أيقونة",
            "pattern": "نقش زخرفي"
        }
        parts.append(f"النمط: {style_names.get(analysis.style, analysis.style)}")
        
        # المزاج
        mood_names = {
            "professional": "احترافي",
            "playful": "مرح",
            "elegant": "أنيق",
            "modern": "عصري",
            "traditional": "تقليدي",
            "minimalist": "بسيط"
        }
        parts.append(f"المزاج: {mood_names.get(analysis.mood, analysis.mood)}")
        
        # اللغة
        lang_names = {"ar": "عربي", "en": "إنجليزي", "mixed": "مختلط"}
        parts.append(f"اللغة: {lang_names.get(analysis.language, analysis.language)}")
        
        return " | ".join(parts)
    
    def _select_concepts(self, 
                         analysis: AnalysisResult,
                         basic_concepts: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """اختيار وتحسين المفاهيم"""
        concepts = list(basic_concepts)
        
        # إضافة مفاهيم إضافية حسب التحليل
        if analysis.language == "ar":
            # تعزيز النمط العربي
            existing = [c[0] for c in concepts]
            if "arabic_style" not in existing:
                concepts.append(("arabic_style", 0.7))
        
        # تعديل الشدة حسب التعقيد
        if analysis.complexity == "complex":
            concepts = [(name, min(strength * 1.2, 1.0)) for name, strength in concepts]
        
        # ترتيب حسب الأهمية
        concepts.sort(key=lambda x: x[1], reverse=True)
        
        return concepts[:5]  # أقصى 5 مفاهيم
    
    def _select_strategy(self, analysis: AnalysisResult) -> str:
        """اختيار استراتيجية التوجيه"""
        if analysis.style in ["logo", "icon"]:
            return "additive"  # أبسط وأسرع
        elif analysis.style in ["photo"]:
            return "projection"  # أكثر دقة
        elif analysis.mood == "traditional":
            return "hspace"  # للتحرير الدلالي
        
        return "additive"
    
    def _generate_variations(self, prompt: str, analysis: AnalysisResult) -> List[str]:
        """توليد تنويعات إبداعية"""
        variations = []
        
        # تنويع 1: أكثر تفصيلاً
        detailed = f"{prompt} with intricate details and rich textures"
        variations.append(detailed)
        
        # تنويع 2: أكثر بساطة
        simple = f"minimalist {prompt}, clean and simple"
        variations.append(simple)
        
        # تنويع 3: نمط مختلف
        if analysis.mood != "modern":
            modern = f"modern contemporary {prompt}"
            variations.append(modern)
        else:
            classic = f"classic traditional {prompt}"
            variations.append(classic)
        
        return variations
    
    def _generate_reasoning(self, 
                            prompt: str, 
                            analysis: AnalysisResult,
                            concepts: List[Tuple[str, float]]) -> str:
        """توليد تفسير للقرارات"""
        reasoning = []
        
        reasoning.append(f"تم تحليل الطلب: '{prompt}'")
        reasoning.append(f"تم تحديد النمط كـ '{analysis.style}' والمزاج كـ '{analysis.mood}'")
        
        if concepts:
            concept_names = [c[0] for c in concepts]
            reasoning.append(f"تم اختيار المفاهيم: {', '.join(concept_names)}")
        
        if analysis.language == "ar":
            reasoning.append("تم تفعيل دعم اللغة العربية والنمط العربي")
        
        return " → ".join(reasoning)


def quick_think(prompt: str) -> ThoughtResult:
    """تفكير سريع - دالة مساعدة"""
    layer = AdvancedThinkingLayer(enable_creative=False)
    return layer.think(prompt, depth="quick")


def creative_think(prompt: str) -> ThoughtResult:
    """تفكير إبداعي - دالة مساعدة"""
    layer = AdvancedThinkingLayer(enable_creative=True)
    return layer.think(prompt, depth="deep")
