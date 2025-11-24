import ast
import subprocess
import tempfile
import os

class BugFreeValidator:
    """
    'Bug-Free' Validator.
    Checks AI-generated code for syntax errors and linting issues.
    """

    def __init__(self):
        pass

    def validate_and_fix(self, code: str, language: str = "python") -> str:
        """
        Runs code through linter and attempts to fix errors using LLM.
        """
        if language != "python":
            return code # MVP only supports Python validation

        # 1. Syntax Check (AST)
        try:
            ast.parse(code)
        except SyntaxError as e:
            print(f"Syntax Error detected: {e}")
            return self._fix_with_llm(code, str(e))

        # 2. Linter Check (Pylint/Flake8) - Mocked for speed/environment
        # In real app: write to temp file, run subprocess(['pylint', temp_file])
        
        # Mocking a linter check
        if "eval(" in code:
            error = "Security Risk: Use of eval() detected."
            return self._fix_with_llm(code, error)
            
        return code

    def _fix_with_llm(self, code: str, error_msg: str) -> str:
        """
        Feeds the error back to the LLM to fix itself.
        """
        prompt = f"""
        The following Python code has an error:
        {error_msg}
        
        Code:
        {code}
        
        Please fix the code and return ONLY the corrected code.
        """
        
        # Mock LLM Fix
        # fixed_code = llm.generate(prompt)
        
        print(f"Attempting to fix error: {error_msg}")
        fixed_code = code.replace("eval(", "int(") # Simple mock fix
        
        return fixed_code
