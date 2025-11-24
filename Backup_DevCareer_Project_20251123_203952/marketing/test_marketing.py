
# test_marketing.py
import os
from marketing_bot import LeadManager

def test_lead_manager():
    print("Testing Lead Manager...")
    csv_file = "test_leads.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
        
    manager = LeadManager(csv_file)
    manager.add_lead("Test User", "http://example.com")
    
    if os.path.exists(csv_file):
        print("✅ CSV Created: PASS")
        with open(csv_file, 'r') as f:
            content = f.read()
            if "Test User" in content:
                print("✅ Lead Added: PASS")
            else:
                print("❌ Lead Added: FAIL")
    else:
        print("❌ CSV Created: FAIL")
        
    # Cleanup
    if os.path.exists(csv_file):
        os.remove(csv_file)

if __name__ == "__main__":
    test_lead_manager()
