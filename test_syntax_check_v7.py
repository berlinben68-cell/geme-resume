import sys
import os

# Add project root to path
sys.path.append(os.path.abspath("d:/geme-resume"))

try:
    # dashboard.py is a script
    with open("d:/geme-resume/DevCareer_Project/admin_panel/dashboard.py", "r", encoding="utf-8") as f:
        compile(f.read(), "dashboard.py", "exec")
    print("dashboard.py compiled successfully")
except Exception as e:
    print(f"Error compiling dashboard.py: {e}")
