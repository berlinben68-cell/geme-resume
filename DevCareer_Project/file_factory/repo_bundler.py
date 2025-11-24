
# repo_bundler.py
import os
import zipfile
import shutil

def create_project_bundle(project_name, readme_content, mermaid_code, structure_text, output_dir):
    """
    Creates a project folder with README, Mermaid, and Structure file, then zips it.
    """
    try:
        # Create base directory for the project
        project_path = os.path.join(output_dir, project_name)
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
        os.makedirs(project_path)
        
        # Write README.md
        with open(os.path.join(project_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)
            
        # Write architecture.mermaid
        with open(os.path.join(project_path, "architecture.mermaid"), "w", encoding="utf-8") as f:
            f.write(mermaid_code)

        # Write structure.txt
        with open(os.path.join(project_path, "structure.txt"), "w", encoding="utf-8") as f:
            f.write(structure_text)
            
        # Create ZIP file
        zip_path = os.path.join(output_dir, f"{project_name}.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, arcname)
                    
        # Cleanup (optional, keeping it for now might be useful for debugging)
        # shutil.rmtree(project_path) 
        
        return zip_path
    except Exception as e:
        print(f"Error bundling repo: {e}")
        return None
