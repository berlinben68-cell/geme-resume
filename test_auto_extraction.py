import sys
import os

sys.path.append(os.path.abspath("d:/geme-resume"))

try:
    # Test prompts
    from DevCareer_Project.core_engine.prompts import get_linkedin_banner_content_extraction_prompt
    print("✅ get_linkedin_banner_content_extraction_prompt imported successfully")
    
    # Test ai_logic
    from DevCareer_Project.core_engine.ai_logic import IntelligenceEngine
    print("✅ IntelligenceEngine imported successfully")
    
    # Test dashboard compilation
    with open("d:/geme-resume/DevCareer_Project/admin_panel/dashboard.py", "r", encoding="utf-8") as f:
        compile(f.read(), "dashboard.py", "exec")
    print("✅ dashboard.py compiled successfully")
    
    print("\n✅ All files verified successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
