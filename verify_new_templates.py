import sys
import os

sys.path.append(os.path.abspath("d:/geme-resume"))

try:
    from DevCareer_Project.core_engine.visual_factory import VisualFactory
    vf = VisualFactory()
    
    expected_templates = ['modern_gradient', 'success_green', 'elegant_rose']
    missing = [t for t in expected_templates if t not in vf.BANNER_TEMPLATES]
    
    if missing:
        print(f"❌ Missing templates: {missing}")
    else:
        print("✅ All new templates found in VisualFactory")
        for t in expected_templates:
            print(f"   - {vf.BANNER_TEMPLATES[t]['name']}")

    # Check dashboard compilation
    with open("d:/geme-resume/DevCareer_Project/admin_panel/dashboard.py", "r", encoding="utf-8") as f:
        compile(f.read(), "dashboard.py", "exec")
    print("✅ dashboard.py compiled successfully")

except Exception as e:
    print(f"❌ Error: {e}")
