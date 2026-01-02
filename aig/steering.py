"""
Steering Module - وحدة التوجيه
==============================

تحكم في سلوك النموذج عبر Activation Steering
يدمج تقنيات: CASteer, H-Space, Representation Engineering
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pickle
import os


class SteeringStrategy(Enum):
    """استراتيجيات التوجيه المتاحة"""
    ADDITIVE = "additive"      # إضافة بسيطة
    PROJECTION = "projection"  # إسقاط ثم إضافة
    HSPACE = "hspace"          # تحرير في h-space


@dataclass
class ConceptVector:
    """متجه مفهوم للتوجيه"""
    name: str
    vector: np.ndarray
    strength: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class SteeringController:
    """
    متحكم التوجيه الرئيسي
    
    يدير المفاهيم ويطبق التوجيه على التفعيلات
    
    الاستخدام:
    ```python
    controller = SteeringController(alpha=10.0)
    controller.add_concept(ConceptVector("creativity", vector, 0.8))
    controller.activate_concept("creativity")
    steered = controller.steer(activations)
    ```
    """
    
    def __init__(self,
                 default_strategy: str = "additive",
                 alpha: float = 10.0,
                 beta: float = 2.0,
                 normalize: bool = True):
        
        self.strategy = SteeringStrategy(default_strategy)
        self.alpha = alpha  # شدة التوجيه الإيجابي
        self.beta = beta    # شدة التوجيه العكسي
        self.normalize = normalize
        self.concepts: Dict[str, ConceptVector] = {}
        self.active_concepts: List[str] = []
    
    def add_concept(self, concept: ConceptVector):
        """إضافة مفهوم جديد"""
        # تطبيع المتجه
        norm = np.linalg.norm(concept.vector)
        if norm > 0:
            concept.vector = concept.vector / norm
        self.concepts[concept.name] = concept
    
    def remove_concept(self, name: str):
        """إزالة مفهوم"""
        if name in self.concepts:
            del self.concepts[name]
        self.deactivate_concept(name)
    
    def activate_concept(self, name: str, strength: Optional[float] = None):
        """تفعيل مفهوم"""
        if name in self.concepts:
            if strength is not None:
                self.concepts[name].strength = strength
            if name not in self.active_concepts:
                self.active_concepts.append(name)
    
    def deactivate_concept(self, name: str):
        """إلغاء تفعيل مفهوم"""
        if name in self.active_concepts:
            self.active_concepts.remove(name)
    
    def deactivate_all(self):
        """إلغاء تفعيل جميع المفاهيم"""
        self.active_concepts = []
    
    def steer(self, 
              activations: np.ndarray,
              layer_name: str = "mid",
              timestep: int = 0) -> np.ndarray:
        """
        تطبيق التوجيه على التفعيلات
        
        Args:
            activations: التفعيلات الأصلية [batch, ..., hidden_dim]
            layer_name: اسم الطبقة
            timestep: الخطوة الزمنية
        
        Returns:
            التفعيلات المُوجَّهة
        """
        if not self.active_concepts:
            return activations
        
        # حفظ النورم الأصلي
        original_norm = np.linalg.norm(activations, axis=-1, keepdims=True)
        steered = activations.copy()
        
        for name in self.active_concepts:
            if name not in self.concepts:
                continue
            
            concept = self.concepts[name]
            vector = concept.vector
            strength = concept.strength
            
            # تعديل حجم المتجه ليتناسب مع التفعيلات
            if vector.shape[-1] != activations.shape[-1]:
                # محاولة التوسيع أو التقليص
                if len(vector.shape) == 1:
                    vector = np.broadcast_to(vector, activations.shape)
                else:
                    continue
            
            # تطبيق الاستراتيجية المختارة
            if self.strategy == SteeringStrategy.ADDITIVE:
                # steered = activations + α * strength * vector
                alpha = self.alpha * strength if strength >= 0 else -self.beta * abs(strength)
                steered = steered + alpha * vector
            
            elif self.strategy == SteeringStrategy.PROJECTION:
                # إزالة المكون الحالي ثم الإضافة
                # steered = activations - (activations · v)v + α * v
                proj = np.sum(steered * vector, axis=-1, keepdims=True) * vector
                steered = steered - proj + self.alpha * strength * vector
            
            elif self.strategy == SteeringStrategy.HSPACE:
                # تحرير في h-space (للطبقة الوسطى فقط)
                if layer_name == "mid":
                    steered = steered + self.alpha * strength * vector
        
        # إعادة التطبيع للحفاظ على النورم الأصلي
        if self.normalize:
            new_norm = np.linalg.norm(steered, axis=-1, keepdims=True)
            steered = steered / (new_norm + 1e-8) * original_norm
        
        return steered
    
    def compute_combined_vector(self) -> Optional[np.ndarray]:
        """حساب المتجه المدمج من جميع المفاهيم النشطة"""
        if not self.active_concepts:
            return None
        
        combined = None
        for name in self.active_concepts:
            if name in self.concepts:
                concept = self.concepts[name]
                weighted = concept.vector * concept.strength
                if combined is None:
                    combined = weighted
                else:
                    combined = combined + weighted
        
        return combined
    
    def save_concepts(self, path: str):
        """حفظ المفاهيم إلى ملف"""
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self.concepts, f)
    
    def load_concepts(self, path: str):
        """تحميل المفاهيم من ملف"""
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.concepts = pickle.load(f)


class ConceptLibrary:
    """
    مكتبة المفاهيم المحفوظة
    
    تخزن وتدير مجموعة من متجهات المفاهيم
    """
    
    def __init__(self, path: Optional[str] = None):
        self.path = path
        self.concepts: Dict[str, ConceptVector] = {}
        if path and os.path.exists(path):
            self.load()
    
    def add_concept(self, concept: ConceptVector):
        """إضافة مفهوم للمكتبة"""
        self.concepts[concept.name] = concept
    
    def get_concept(self, name: str) -> Optional[ConceptVector]:
        """الحصول على مفهوم"""
        return self.concepts.get(name)
    
    def list_concepts(self) -> List[str]:
        """قائمة المفاهيم المتاحة"""
        return list(self.concepts.keys())
    
    def save(self):
        """حفظ المكتبة"""
        if self.path:
            os.makedirs(os.path.dirname(self.path) if os.path.dirname(self.path) else '.', exist_ok=True)
            with open(self.path, 'wb') as f:
                pickle.dump(self.concepts, f)
    
    def load(self):
        """تحميل المكتبة"""
        if self.path and os.path.exists(self.path):
            with open(self.path, 'rb') as f:
                self.concepts = pickle.load(f)


# === مفاهيم افتراضية ===

DEFAULT_CONCEPTS = {
    "creativity": {
        "positive": ["highly creative", "innovative", "unique"],
        "negative": ["generic", "boring", "common"]
    },
    "professional": {
        "positive": ["professional", "polished", "high-quality"],
        "negative": ["amateur", "rough", "low-quality"]
    },
    "arabic_style": {
        "positive": ["Arabic geometric patterns", "Islamic art", "Middle Eastern"],
        "negative": ["Western modern", "European", "minimalist"]
    }
}
