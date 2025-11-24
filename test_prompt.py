import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'DevCareer_Project')))

try:
    from core_engine.prompts import get_linkedin_profile_kit_prompt
    
    prompt = get_linkedin_profile_kit_prompt("Software Engineer", "Dubai", "Resume content here")
    print("Prompt generated successfully.")
    # print(prompt) # Optional: print to check output
    
except Exception as e:
    print(f"Verification failed: {e}")
