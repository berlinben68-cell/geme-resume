import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add project root to path
sys.path.append(os.path.join(os.getcwd(), 'DevCareer_Project'))

from core_engine.ai_logic import IntelligenceEngine
from file_factory.doc_builder import generate_html_preview, create_resume_docx

class TestSystem(unittest.TestCase):
    
    def setUp(self):
        self.api_key = "fake_key"
        self.engine = IntelligenceEngine(self.api_key)
        # Mock the model
        self.engine.model = MagicMock()

    def test_doc_builder_html(self):
        print("\nTesting HTML Generation...")
        text = "JOHN DOE\nSoftware Engineer\n- Built things"
        html = generate_html_preview(text, "Standard ATS")
        self.assertIn("JOHN DOE", html)
        self.assertIn("Software Engineer", html)
        print("✅ HTML Generation Passed")

    def test_doc_builder_docx(self):
        print("\nTesting DOCX Generation...")
        text = "JOHN DOE\nSoftware Engineer\n- Built things"
        output_path = "test_resume.docx"
        if os.path.exists(output_path):
            os.remove(output_path)
            
        success = create_resume_docx(text, output_path, "Standard ATS")
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_path))
        
        # Cleanup
        if os.path.exists(output_path):
            os.remove(output_path)
        print("✅ DOCX Generation Passed")

    def test_ai_architect_project(self):
        print("\nTesting AI Architect (Mocked)...")
        # Mock response
        mock_response = MagicMock()
        mock_response.text = "README Content\n### SECTION BREAK ###\ngraph TD; A-->B\n### SECTION BREAK ###\nsrc/\n  main.py"
        self.engine.model.generate_content.return_value = mock_response
        
        result = self.engine.architect_project("Test App")
        self.assertEqual(result['readme'], "README Content")
        self.assertEqual(result['mermaid'], "graph TD; A-->B")
        self.assertIn("src/", result['structure'])
        print("✅ AI Architect Passed")

    def test_ai_visual_extraction(self):
        print("\nTesting Visual Extraction (Mocked)...")
        # Mock response
        mock_response = MagicMock()
        mock_response.text = "Title: My Project\nProblem: Slow\nSolution: Fast\nResults: 100% | 200%\nSkills: Python"
        self.engine.model.generate_content.return_value = mock_response
        
        data = self.engine.extract_visual_content("Resume Text", "Role")
        self.assertEqual(data['title'], "My Project")
        self.assertEqual(data['problem'], "Slow")
        self.assertEqual(data['solution'], "Fast")
        self.assertEqual(data['skills'], "Python")
        print("✅ Visual Extraction Passed")

if __name__ == '__main__':
    unittest.main()
