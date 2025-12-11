import sys
import os

sys.path.append(os.path.abspath("d:/geme-resume"))

try:
    import DevCareer_Project.core_engine.visual_factory
    print("✅ visual_factory.py imported successfully")
    
    # Test template access
    from DevCareer_Project.core_engine.visual_factory import VisualFactory
    vf = VisualFactory()
    print(f"✅ Found {len(vf.BANNER_TEMPLATES)} banner templates")
    for key in vf.BANNER_TEMPLATES:
        print(f"   - {key}")
    
except Exception as e:
    print(f"❌ Error: {e}")
