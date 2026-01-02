"""
H-Space Integration - تكامل H-Space
====================================

Semantic Latent Space Manipulation
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class HSpaceConfig:
    """إعدادات H-Space"""
    edit_strength: float = 1.0
    use_asyrp: bool = True
    timestep_range: Tuple[int, int] = (200, 800)


class HSpaceEditor:
    """محرر H-Space للتحرير الدلالي"""
    
    def __init__(self, config: Optional[HSpaceConfig] = None):
        self.config = config or HSpaceConfig()
        self.edit_directions: Dict[str, Tuple[np.ndarray, float]] = {}
        self.active_edits: List[str] = []
    
    def add_edit_direction(self, name: str, direction: np.ndarray, strength: float = 1.0):
        norm = np.linalg.norm(direction)
        if norm > 0:
            direction = direction / norm
        self.edit_directions[name] = (direction, strength)
    
    def activate_edit(self, name: str, strength: Optional[float] = None):
        if name in self.edit_directions:
            if strength is not None:
                direction, _ = self.edit_directions[name]
                self.edit_directions[name] = (direction, strength)
            if name not in self.active_edits:
                self.active_edits.append(name)
    
    def deactivate_edit(self, name: str):
        if name in self.active_edits:
            self.active_edits.remove(name)
    
    def apply_edit(self, h: np.ndarray, timestep: int) -> np.ndarray:
        if not self.active_edits:
            return h
        
        t_min, t_max = self.config.timestep_range
        if not (t_min <= timestep <= t_max):
            return h
        
        h_edited = h.copy()
        for name in self.active_edits:
            if name in self.edit_directions:
                direction, strength = self.edit_directions[name]
                if direction.shape[-1] != h.shape[-1]:
                    continue
                h_edited = h_edited + self.config.edit_strength * strength * direction
        
        return h_edited
