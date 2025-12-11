import sys
import os

# Add project root to path
sys.path.append(os.path.abspath("d:/geme-resume"))

try:
    import DevCareer_Project.core_engine.prompts
    print("prompts.py imported successfully")
except Exception as e:
    print(f"Error importing prompts.py: {e}")

try:
    # dashboard.py is a script, not a module usually imported, but we can try compiling it
    with open("d:/geme-resume/DevCareer_Project/admin_panel/dashboard.py", "r", encoding="utf-8") as f:
        compile(f.read(), "dashboard.py", "exec")
    print("dashboard.py compiled successfully")
except Exception as e:
    print(f"Error compiling dashboard.py: {e}")
