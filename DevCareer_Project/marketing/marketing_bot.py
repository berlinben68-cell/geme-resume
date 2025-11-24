
# marketing_bot.py
import csv
import os
from datetime import datetime

class LeadManager:
    def __init__(self, filename="leads.csv"):
        self.filename = filename
        self.headers = ["Name", "Profile URL", "Status", "Date Added", "Notes"]
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)

    def add_lead(self, name, profile_url, status="New", notes=""):
        """
        Adds a new lead to the CSV file.
        """
        date_added = datetime.now().strftime("%Y-%m-%d")
        with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, profile_url, status, date_added, notes])
        print(f"✅ Lead '{name}' added successfully.")

    def list_leads(self):
        """
        Prints all leads.
        """
        if not os.path.exists(self.filename):
            print("No leads file found.")
            return

        with open(self.filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)

if __name__ == "__main__":
    # Simple CLI for testing
    manager = LeadManager(os.path.join(os.path.dirname(__file__), "leads.csv"))
    
    print("--- Lead Manager ---")
    print("1. Add Lead")
    print("2. List Leads")
    
    choice = input("Enter choice (1/2): ")
    
    if choice == "1":
        name = input("Name: ")
        url = input("Profile URL: ")
        manager.add_lead(name, url)
    elif choice == "2":
        manager.list_leads()
    else:
        print("Invalid choice.")
