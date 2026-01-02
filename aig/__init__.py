"""
Noesis Engine - محرك توليد الصور الذكي
======================================

نظام ثوري يدمج أفضل تقنيات Activation Engineering
"""

__version__ = "0.1.0"
__author__ = "Istiqlal Team"

from .core import NoesisEngine, NoesisConfig, create_engine
from .steering import SteeringController, ConceptVector, SteeringStrategy
from .thinking import ThinkingLayer
from .advanced_thinking import AdvancedThinkingLayer, quick_think

__all__ = [
    "NoesisEngine", "NoesisConfig", "create_engine",
    "SteeringController", "ConceptVector", "SteeringStrategy",
    "ThinkingLayer", "AdvancedThinkingLayer", "quick_think"
]
