import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    # Technical
    from app.auth import login_github
    from app.models import SQL_SCHEMA
    
    # AI
    from app.services.rag_memory import RAGMemory
    from app.services.validator import BugFreeValidator
    from app.services.readme_gen import ReadMeGenerator
    
    # UX
    from app.services.onboarding import OnboardingQuestionnaire
    from app.services.notifications import NotificationSystem
    
    # Safety
    from app.services.kill_switch import KillSwitch
    
    print("All Full Infrastructure modules imported successfully.")
    
    # Test RAG
    rag = RAGMemory("user_123")
    patterns = rag.search_patterns("auth")
    if len(patterns) > 0:
        print("RAG Memory test passed.")
        
    # Test Validator
    validator = BugFreeValidator()
    code = "print('hello')"
    validated = validator.validate_and_fix(code)
    if validated == code:
        print("Validator test passed.")
        
    # Test Kill Switch
    kill_switch = KillSwitch()
    result = kill_switch.panic_delete_user_data("user_test")
    if result["status"] == "terminated":
        print("Kill Switch test passed.")
        
except Exception as e:
    print(f"Verification failed: {e}")
