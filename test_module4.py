
# test_module4.py
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath("DevCareer_Project"))

from file_factory.doc_builder import create_resume_docx
from file_factory.repo_bundler import create_project_bundle

def test_docx_builder():
    print("Testing DOCX Builder...")
    dummy_text = "John Doe\nSoftware Engineer\n- Expert in Python\n- Built DevCareer OS"
    output_path = "test_resume.docx"
    
    if create_resume_docx(dummy_text, output_path):
        if os.path.exists(output_path):
            print("✅ DOCX Created: PASS")
            # os.remove(output_path) # Keep for inspection
        else:
            print("❌ DOCX Created: FAIL (File not found)")
    else:
        print("❌ DOCX Created: FAIL (Function returned False)")

def test_repo_bundler():
    print("\nTesting Repo Bundler...")
    project_name = "TestProject"
    readme = "# Test Project\nThis is a test."
    mermaid = "graph TD; A-->B;"
    output_dir = "."
    
    structure = "project/\n  main.py"
    zip_path = create_project_bundle(project_name, readme, mermaid, structure, output_dir)
    
    if zip_path and os.path.exists(zip_path):
        print(f"✅ ZIP Created: PASS ({zip_path})")
        # os.remove(zip_path) # Keep for inspection
    else:
        print("❌ ZIP Created: FAIL")

if __name__ == "__main__":
    test_docx_builder()
    test_repo_bundler()
