
# test_module1.py
import sys
import os

# Add the project root to path so we can import modules
sys.path.append(os.path.abspath("DevCareer_Project"))

from core_engine.prompts import get_resume_prompt, get_github_architect_prompt

def test_prompts():
    print("Testing Prompts...")
    
    # Test India Prompt
    india_prompt = get_resume_prompt("India", "Experienced Java Developer...")
    if "Scale" in india_prompt and "Naukri Keywords" in india_prompt:
        print("✅ India Prompt: PASS")
    else:
        print("❌ India Prompt: FAIL")

    # Test UAE Prompt
    uae_prompt = get_resume_prompt("UAE", "Experienced Java Developer...")
    if "ROI" in uae_prompt and "Visa Status" in uae_prompt:
        print("✅ UAE Prompt: PASS")
    else:
        print("❌ UAE Prompt: FAIL")
        
    # Test Architect Prompt
    arch_prompt = get_github_architect_prompt("E-commerce app")
    if "Mermaid.js Diagram" in arch_prompt:
        print("✅ Architect Prompt: PASS")
    else:
        print("❌ Architect Prompt: FAIL")

if __name__ == "__main__":
    test_prompts()
    print("\nTo test actual generation, you need a Gemini API Key.")
