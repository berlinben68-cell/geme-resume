
# demo_engine.py
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core_engine.ai_logic import IntelligenceEngine

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = input("Enter your Gemini API Key: ")
    
    engine = IntelligenceEngine(api_key)
    
    print("\n--- Testing Resume Rewrite (India) ---")
    dummy_resume = "Software Engineer with 2 years experience in Java."
    print("Original:", dummy_resume)
    rewritten = engine.rewrite_resume(dummy_resume, market="India")
    print("\nRewritten:\n", rewritten)
    
    print("\n--- Testing Architect ---")
    desc = "A To-Do list app with Python and Streamlit"
    arch = engine.architect_project(desc)
    print("\nArchitecture:\n", arch)

if __name__ == "__main__":
    main()
