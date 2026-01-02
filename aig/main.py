"""
Main Entry Point - نقطة الدخول الرئيسية
=======================================

تشغيل Noesis Engine من سطر الأوامر
"""

import argparse
import sys
from .core import NoesisEngine, create_engine
from .advanced_thinking import quick_think, creative_think


def main():
    parser = argparse.ArgumentParser(
        description="Noesis Engine - محرك توليد الصور الذكي",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة:
  python -m noesis_engine.main --prompt "شعار لمقهى عربي"
  python -m noesis_engine.main --prompt "شعار" --think
  python -m noesis_engine.main --prompt "شعار" --explore arabic_style
  python -m noesis_engine.main demo
        """
    )
    
    parser.add_argument("command", nargs="?", default="generate",
                        help="الأمر: generate, think, demo")
    parser.add_argument("--prompt", "-p", type=str, help="الطلب")
    parser.add_argument("--think", "-t", action="store_true", help="تفعيل التفكير")
    parser.add_argument("--creative", "-c", action="store_true", help="تفكير إبداعي")
    parser.add_argument("--explore", "-e", type=str, help="استكشاف مفهوم")
    parser.add_argument("--analyze-only", "-a", action="store_true", help="تحليل فقط")
    parser.add_argument("--output", "-o", type=str, default="output.png", help="ملف الإخراج")
    
    args = parser.parse_args()
    
    if args.command == "demo":
        run_demo()
        return
    
    if not args.prompt:
        print("❌ يرجى تحديد الطلب باستخدام --prompt")
        sys.exit(1)
    
    # التفكير فقط
    if args.analyze_only:
        if args.creative:
            thought = creative_think(args.prompt)
        else:
            thought = quick_think(args.prompt)
        
        print("\n🧠 نتيجة التفكير:")
        print(f"   الفهم: {thought.understanding}")
        print(f"   Prompt المحسّن: {thought.enhanced_prompt}")
        print(f"   المفاهيم: {thought.selected_concepts}")
        print(f"   الاستراتيجية: {thought.steering_strategy}")
        if thought.reasoning:
            print(f"   التفسير: {thought.reasoning}")
        return
    
    # التوليد
    engine = create_engine(enable_thinking=args.think or args.creative)
    
    if args.explore:
        print(f"\n🔍 استكشاف مفهوم: {args.explore}")
        # توليد عدة صور بشدات مختلفة
        for strength in [0.3, 0.6, 0.9]:
            result = engine.generate(
                args.prompt,
                concepts=[args.explore],
                concept_strengths={args.explore: strength}
            )
            output_file = f"{args.output.rsplit('.', 1)[0]}_{args.explore}_{strength}.png"
            if result.image:
                result.image.save(output_file)
                print(f"   ✅ {output_file} (strength={strength})")
    else:
        result = engine.generate(args.prompt)
        if result.image:
            result.image.save(args.output)
            print(f"\n✅ تم حفظ الصورة: {args.output}")
        print(f"   Prompt المستخدم: {result.prompt_used}")
        print(f"   المفاهيم المطبقة: {result.concepts_applied}")


def run_demo():
    """تشغيل العرض التوضيحي"""
    print("\n" + "="*60)
    print("🎨 Noesis Engine - عرض توضيحي")
    print("="*60)
    
    # اختبار التفكير
    print("\n📝 اختبار التفكير...")
    thought = quick_think("شعار لمقهى عربي تقليدي")
    print(f"   ✅ الفهم: {thought.understanding}")
    print(f"   ✅ المفاهيم: {thought.selected_concepts}")
    
    # اختبار المحرك
    print("\n⚙️ اختبار المحرك...")
    engine = create_engine()
    print(f"   ✅ المفاهيم المتاحة: {engine.get_available_concepts()}")
    
    # اختبار التوليد
    print("\n🖼️ اختبار التوليد...")
    result = engine.generate("شعار")
    print(f"   ✅ Prompt المستخدم: {result.prompt_used[:50]}...")
    print(f"   ✅ المفاهيم المطبقة: {result.concepts_applied}")
    
    print("\n" + "="*60)
    print("✅ جميع الاختبارات نجحت!")
    print("="*60)


if __name__ == "__main__":
    main()
