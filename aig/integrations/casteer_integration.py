"""
CASteer Integration - تكامل CASteer
====================================

Cross-Attention Steering for Diffusion Models
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class CASteerConfig:
    """إعدادات CASteer"""
    alpha: float = 10.0
    beta: float = 2.0
    normalize: bool = True
    apply_to_layers: List[str] = None
    timestep_range: Tuple[int, int] = (0, 1000)
    
    def __post_init__(self):
        if self.apply_to_layers is None:
            self.apply_to_layers = ["down", "mid", "up"]


class CASteerApplier:
    """مُطبّق CASteer"""
    
    def __init__(self, config: Optional[CASteerConfig] = None):
        self.config = config or CASteerConfig()
        self.steering_vectors: Dict[str, Tuple[np.ndarray, float]] = {}
        self.active = False
    
    def add_steering_vector(self, name: str, vector: np.ndarray, strength: float = 1.0):
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        self.steering_vectors[name] = (vector, strength)
    
    def activate(self):
        self.active = True
    
    def deactivate(self):
        self.active = False
    
    def apply_steering(self, activations: np.ndarray, layer_name: str, timestep: int) -> np.ndarray:
        if not self.active or layer_name not in self.config.apply_to_layers:
            return activations
        
        t_min, t_max = self.config.timestep_range
        if not (t_min <= timestep <= t_max):
            return activations
        
        original_norm = np.linalg.norm(activations, axis=-1, keepdims=True)
        steered = activations.copy()
        
        for name, (vector, strength) in self.steering_vectors.items():
            if vector.shape[-1] != activations.shape[-1]:
                continue
            alpha = self.config.alpha * strength if strength >= 0 else -self.config.beta * abs(strength)
            steered = steered + alpha * vector
        
        if self.config.normalize:
            new_norm = np.linalg.norm(steered, axis=-1, keepdims=True)
            steered = steered / (new_norm + 1e-8) * original_norm
        
        return steered


def get_concept_prompts(concept: str) -> Tuple[List[str], List[str]]:
    """الحصول على أمثلة لمفهوم"""
    concepts = {
        "creativity": {
            "positive": ["highly creative design", "unique artwork", "innovative composition"],
            "negative": ["generic design", "boring artwork", "common composition"]
        },
        "professional": {
            "positive": ["professional design", "polished artwork", "expert composition"],
            "negative": ["amateur design", "rough artwork", "beginner composition"]
        },
        "arabic_style": {
            "positive": ["Arabic geometric patterns", "Islamic art", "Arabian calligraphy"],
            "negative": ["Western modern design", "European style", "minimalist plain"]
        }
    }
    if concept in concepts:
        return concepts[concept]["positive"], concepts[concept]["negative"]
    return [f"high {concept}"], [f"low {concept}"]
