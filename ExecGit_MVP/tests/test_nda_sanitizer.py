import unittest
import sys
import os
import textwrap

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.nda_sanitizer import NDASanitizer

class TestNDASanitizer(unittest.TestCase):

    def setUp(self):
        self.sanitizer = NDASanitizer(forbidden_terms=["Etisalat", "HDFC", "SecretProject"])

    def test_debrand_code(self):
        code = textwrap.dedent("""
        api_key = "sk-1234567890123456789012345"
        client = "Etisalat"
        def connect_to_hdfc():
            pass
        """)
        sanitized = self.sanitizer.debrand_code(code)
        
        self.assertNotIn("sk-1234567890123456789012345", sanitized)
        self.assertIn("REDACTED_SECRET", sanitized)
        self.assertNotIn("Etisalat", sanitized)
        self.assertIn("GenericEntity1", sanitized) # Etisalat is first in list
        self.assertNotIn("HDFC", sanitized)

    def test_generate_shadow_structure(self):
        code = textwrap.dedent("""
        def transfer_money(user_id: str, amount: float) -> bool:
            # Secret logic
            db.connect("secret_host")
            return True
        """)
        shadow = self.sanitizer.generate_shadow_structure(code)
        
        self.assertIn("def transfer_money(user_id: str, amount: float) -> bool:", shadow)
        self.assertNotIn("db.connect", shadow)
        self.assertIn("Implementation hidden for NDA compliance", shadow)
        self.assertIn("logger.info", shadow)

    def test_code_to_mermaid(self):
        code = textwrap.dedent("""
        class BankAccount:
            def deposit(self): pass
            
        class SavingsAccount(BankAccount):
            def add_interest(self): pass
        """)
        mermaid = self.sanitizer.code_to_mermaid(code)
        
        self.assertIn("classDiagram", mermaid)
        self.assertIn("class BankAccount", mermaid)
        self.assertIn("BankAccount <|-- SavingsAccount", mermaid)
        self.assertIn("BankAccount : +deposit()", mermaid)

if __name__ == '__main__':
    unittest.main()
