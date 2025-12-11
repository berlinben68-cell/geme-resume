import sys
import os

# Add project root to path
sys.path.append(os.path.abspath("d:/geme-resume"))

try:
    import DevCareer_Project.file_factory.doc_builder
    print("doc_builder.py imported successfully")
except Exception as e:
    print(f"Error importing doc_builder.py: {e}")

try:
    import DevCareer_Project.core_engine.ai_logic
    print("ai_logic.py imported successfully")
except Exception as e:
    print(f"Error importing ai_logic.py: {e}")

try:
    # dashboard.py is a script
    with open("d:/geme-resume/DevCareer_Project/admin_panel/dashboard.py", "r", encoding="utf-8") as f:
        compile(f.read(), "dashboard.py", "exec")
    print("dashboard.py compiled successfully")
except Exception as e:
    print(f"Error compiling dashboard.py: {e}")
