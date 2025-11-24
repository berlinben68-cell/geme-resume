import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app.main import app
    from app.services.scheduler import GreenSquareScheduler
    from app.services.style_matcher import StyleMatcher
    from app.services.audio_engine import AudioEngine
    from app.services.sanitizer import CorporateSanitizer
    from app.services.scorer import RecruiterVisionScorer
    
    print("All modules imported successfully.")
    
    # Basic instantiation tests
    scheduler = GreenSquareScheduler("./temp_repo")
    style_matcher = StyleMatcher()
    audio_engine = AudioEngine()
    sanitizer = CorporateSanitizer()
    scorer = RecruiterVisionScorer()
    
    print("All services instantiated successfully.")
    
    # Test Sanitizer
    code = "api_key = 'sk-1234567890123456789012345'"
    sanitized = sanitizer.sanitize(code)
    print(f"Original: {code}")
    print(f"Sanitized: {sanitized}")
    if "YOUR_API_KEY" in sanitized:
        print("Sanitizer test passed.")
    else:
        print("Sanitizer test failed.")
        
except Exception as e:
    print(f"Verification failed: {e}")
