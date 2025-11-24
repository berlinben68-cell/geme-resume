import shutil
import os
import datetime

def backup_project():
    source_dir = "DevCareer_Project"
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"Backup_DevCareer_Project_{timestamp}"
    
    try:
        if os.path.exists(backup_dir):
            print(f"Backup directory {backup_dir} already exists.")
        else:
            shutil.copytree(source_dir, backup_dir)
            print(f"Successfully backed up {source_dir} to {backup_dir}")
    except Exception as e:
        print(f"Error during backup: {e}")

if __name__ == "__main__":
    backup_project()
