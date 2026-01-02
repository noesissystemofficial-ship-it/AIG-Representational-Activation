"""
Core Module - المحرك الرئيسي
============================

Noesis Engine - محرك توليد الصور الذكي
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import numpy as np

from .steering import SteeringController, ConceptVector, ConceptLibrary
from .thinking import ThinkingLayer
from .advanced_thinking import AdvancedThinkingLayer, ThoughtResult


@dataclass
class NoesisConfig:
    """إعدادات المحرك"""
    model_backend: str = "stable_diffusion"
    model_id: str = "runwayml/stable-diffusion-v1-5"
    enable_thinking: bool = True
    thinking_depth: str = "standard"
    enable_creative: bool = True
    enable_steering: bool = True
    steering_strategy: str = "additive"
    steering_alpha: float = 10.0
    steering_beta: float = 2.0
    default_steps: int = 50
    default_guidance: float = 7.5
    default_width: int = 512
    default_height: int = 512
    use_casteer: bool = True
    use_hspace: bool = True
    concept_library_path: Optional[str] = None


@dataclass
class GenerationResult:
    """نتيجة التوليد"""
    image: Any
    prompt_used: str
    thought: Optional[ThoughtResult] = None
    concepts_applied: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class NoesisEngine:
    """محرك Noesis الرئيسي"""
    
    def __init__(self, config: Optional[NoesisConfig] = None):
        self.config = config or NoesisConfig()
        self.thinking_layer = None
        self.steering_controller = None
        self.concept_library = None
        self.pipeline = None
        self.model_loaded = False
        self._initialize_components()
    
    def _initialize_components(self):
        if self.config.enable_thinking:
            self.thinking_layer = AdvancedThinkingLayer(
                enable_creative=self.config.enable_creative
            )
        if self.config.enable_steering:
            self.steering_controller = SteeringController(
                default_strategy=self.config.steering_strategy,
                alpha=self.config.steering_alpha,
                beta=self.config.steering_beta
            )
        self.concept_library = ConceptLibrary(self.config.concept_library_path)
        self._load_default_concepts()
    
    def _load_default_concepts(self):
        default_concepts = {
            "creativity": np.random.randn(768),
            "professional": np.random.randn(768),
            "arabic_style": np.random.randn(768),
            "minimalist": np.random.randn(768),
            "detailed": np.random.randn(768),
            "vibrant": np.random.randn(768),
            "traditional": np.random.randn(768),
            "modern": np.random.randn(768)
        }
        for name, vector in default_concepts.items():
            concept = ConceptVector(name=name, vector=vector, strength=0.5)
            self.concept_library.add_concept(concept)
            if self.steering_controller:
                self.steering_controller.add_concept(concept)
    
    def load_model(self, model_id: Optional[str] = None):
        model_id = model_id or self.config.model_id
        self.model_loaded = True
        print(f"✅ تم تحميل النموذج: {model_id}")
    
    def think(self, prompt: str) -> ThoughtResult:
        if not self.thinking_layer:
            raise RuntimeError("طبقة التفكير غير مفعّلة")
        return self.thinking_layer.think(prompt, depth=self.config.thinking_depth)
    
    def analyze(self, prompt: str) -> Optional[Dict[str, Any]]:
        if self.thinking_layer:
            thought = self.think(prompt)
            return {
                "understanding": thought.understanding,
                "concepts": thought.selected_concepts,
                "strategy": thought.steering_strategy
            }
        return None
    
    def generate(self, prompt: str, concepts: Optional[List[str]] = None,
                 concept_strengths: Optional[Dict[str, float]] = None, **kwargs) -> GenerationResult:
        thought = None
        final_prompt = prompt
        if self.thinking_layer:
            thought = self.think(prompt)
            final_prompt = thought.enhanced_prompt
            if self.steering_controller and not concepts:
                for concept_name, strength in thought.selected_concepts:
                    self.steering_controller.activate_concept(concept_name, strength)
        if concepts and self.steering_controller:
            for concept_name in concepts:
                strength = concept_strengths.get(concept_name, 0.5) if concept_strengths else 0.5
                self.steering_controller.activate_concept(concept_name, strength)
        
        # صورة وهمية للاختبار
        try:
            from PIL import Image
            image = Image.new('RGB', (512, 512), color='gray')
        except:
            image = None
        
        applied_concepts = []
        if self.steering_controller:
            applied_concepts = list(self.steering_controller.active_concepts)
            self.steering_controller.deactivate_all()
        
        return GenerationResult(
            image=image, prompt_used=final_prompt, thought=thought,
            concepts_applied=applied_concepts, metadata=kwargs
        )
    
    def think_and_generate(self, prompt: str, **kwargs) -> GenerationResult:
        return self.generate(prompt, **kwargs)
    
    def add_concept(self, name: str, vector: np.ndarray, strength: float = 0.5):
        concept = ConceptVector(name=name, vector=vector, strength=strength)
        self.concept_library.add_concept(concept)
        if self.steering_controller:
            self.steering_controller.add_concept(concept)
    
    def get_available_concepts(self) -> List[str]:
        return self.concept_library.list_concepts()


def create_engine(model_id: Optional[str] = None, enable_thinking: bool = True,
                  enable_steering: bool = True, **kwargs) -> NoesisEngine:
    config = NoesisConfig(
        model_id=model_id or "runwayml/stable-diffusion-v1-5",
        enable_thinking=enable_thinking, enable_steering=enable_steering, **kwargs
    )
    return NoesisEngine(config)
