# 🧠 AIG - التفعيل التمثيلي
## Representational Activation for Artificial General Intelligence

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-AIG--Custom-green)
![Python](https://img.shields.io/badge/python-3.8+-yellow)

**نظام ثوري لتوليد الصور يدمج أفضل تقنيات Activation Engineering**

[العربية](#العربية) | [English](#english)

</div>

---

## العربية

### 🌟 ما هو AIG؟

**AIG (التفعيل التمثيلي)** هو إطار عمل مفتوح المصدر يهدف لبناء نظام ذكاء اصطناعي متقدم لتوليد الصور من خلال:

- **التفكير الذكي**: فهم عميق للطلبات وتحسينها تلقائياً
- **التوجيه التمثيلي**: التحكم في سلوك النموذج بدون تدريب
- **الدمج الذكي**: جمع أفضل التقنيات من مشاريع مفتوحة المصدر متعددة

### 🎯 الرؤية

> "التفوق على أفضل أدوات توليد الصور من خلال الذكاء في الطريقة، لا القوة الغاشمة"

### ✨ الميزات الرئيسية

#### 🧠 طبقة التفكير (Thinking Layer)
- فهم الطلبات باللغة العربية والإنجليزية
- تحسين تلقائي للـ prompts
- اقتراح مفاهيم إبداعية ذكية
- تفكير متعدد المستويات (سريع، قياسي، عميق، إبداعي)

#### 🎯 التوجيه التمثيلي (Activation Steering)
- **CASteer**: توجيه عبر Cross-Attention بدون تدريب
- **H-Space**: تحرير دلالي في فضاء bottleneck
- **Concept Vectors**: متجهات مفاهيم قابلة للتخصيص

#### 🔧 التقنيات المدمجة

| التقنية | المصدر | الوصف |
|---------|--------|-------|
| CASteer | Cross-Attention Steering | توجيه بدون تدريب |
| H-Space | Asyrp (ICLR 2023) | تحرير دلالي |
| RepE | Representation Engineering | هندسة التمثيلات |

### 🚀 البدء السريع

```python
from aig import create_engine, quick_think

# تفكير سريع
thought = quick_think("شعار لمقهى عربي تقليدي")
print(thought.enhanced_prompt)
print(thought.selected_concepts)

# إنشاء المحرك
engine = create_engine()

# عرض المفاهيم المتاحة
print(engine.get_available_concepts())
# ['creativity', 'professional', 'arabic_style', 'minimalist', ...]

# توليد (يحتاج GPU)
# result = engine.generate("شعار لمقهى عربي")
# result.image.save("output.png")
```

### 📁 هيكل المشروع

```
aig/
├── __init__.py              # التصدير الرئيسي
├── core.py                  # المحرك الأساسي
├── steering.py              # التحكم بالتوجيه
├── thinking.py              # طبقة التفكير
├── advanced_thinking.py     # التفكير المتقدم
├── main.py                  # نقطة الدخول
└── integrations/
    ├── casteer_integration.py   # تكامل CASteer
    └── hspace_integration.py    # تكامل H-Space
```

### 🎛️ المفاهيم المتاحة

| المفهوم | الوصف |
|---------|-------|
| `creativity` | الإبداع والابتكار |
| `professional` | الاحترافية والجودة |
| `arabic_style` | النمط العربي والإسلامي |
| `minimalist` | البساطة والنظافة |
| `detailed` | التفاصيل الدقيقة |
| `traditional` | الطابع التقليدي |
| `modern` | الطابع العصري |

---

## English

### 🌟 What is AIG?

**AIG (Representational Activation)** is an open-source framework for building advanced AI image generation systems through:

- **Intelligent Thinking**: Deep understanding and automatic prompt enhancement
- **Representational Steering**: Control model behavior without training
- **Smart Integration**: Combining best techniques from multiple open-source projects

### 🎯 Vision

> "Surpass the best image generation tools through intelligent methods, not brute force"

### 🚀 Quick Start

```python
from aig import create_engine, quick_think

# Quick thinking
thought = quick_think("logo for Arabic coffee shop")
print(thought.enhanced_prompt)

# Create engine
engine = create_engine()

# Generate (requires GPU)
# result = engine.generate("professional logo design")
# result.image.save("output.png")
```

---

## 📚 المراجع / References

1. **CASteer**: Cross-Attention Steering for Diffusion Models
2. **Asyrp**: Diffusion Models already have a Semantic Latent Space (ICLR 2023)
3. **Representation Engineering**: Activation Engineering for Neural Networks
4. **Concept Sliders**: LoRA-based Concept Control

---

## 👤 المؤلف / Author

**الرؤية والتوجيه**: صاحب المشروع
**التنفيذ**: بمساعدة الذكاء الاصطناعي

---

## 📄 الرخصة / License

هذا المشروع مرخص تحت **رخصة AIG المخصصة** - انظر ملف [LICENSE](LICENSE) للتفاصيل.

This project is licensed under the **AIG Custom License** - see [LICENSE](LICENSE) for details.

---

<div align="center">

**صُنع بـ ❤️ لدعم الإبداع العربي**

**Made with ❤️ to support Arabic creativity**

</div>
