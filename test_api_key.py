import streamlit as st
import os
import sys
import toml

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "DevCareer_Project")))

def test_api_key_loading():
    print("Testing API Key Loading...")
    
    # 1. Check if secrets.toml exists in the expected location
    secrets_path = os.path.join("DevCareer_Project", ".streamlit", "secrets.toml")
    if os.path.exists(secrets_path):
        print(f"✅ Found secrets.toml at {secrets_path}")
    else:
        print(f"❌ secrets.toml NOT found at {secrets_path}")
        return

    # 2. Try to load it via Streamlit secrets (simulated)
    try:
        with open(secrets_path, "r") as f:
            content = f.read()
            if "GEMINI_API_KEY" in content:
                print("✅ GEMINI_API_KEY found in secrets.toml")
            else:
                print("❌ GEMINI_API_KEY NOT found in secrets.toml")
    except Exception as e:
        print(f"❌ Error reading secrets.toml: {e}")

    # 3. Check if we can initialize IntelligenceEngine with the key
    try:
        secrets = toml.load(secrets_path)
        api_key = secrets.get("GEMINI_API_KEY")
        if api_key:
            print(f"✅ Successfully loaded API Key: {api_key[:5]}...{api_key[-5:]}")
            
            # Try init engine
            from core_engine.ai_logic import IntelligenceEngine
            engine = IntelligenceEngine(api_key)
            if engine.api_key == api_key:
                 print("✅ IntelligenceEngine initialized with correct key")
            else:
                 print("❌ IntelligenceEngine key mismatch")

        else:
            print("❌ GEMINI_API_KEY is empty or missing in parsed TOML")
    except Exception as e:
        print(f"❌ Error parsing TOML or initializing engine: {e}")

if __name__ == "__main__":
    test_api_key_loading()
