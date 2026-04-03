import sys
import os
import time

# --- PATH FIXING ---
# Ensure the script can find the 'src' module from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.tools.tools import research_ai_vulnerability
from src.database.db import init_databases

def run_daily_scan():
    """
    Automated scanner that iterates through known AI security frameworks
    and updates the local intelligence databases.
    """
    print("🚀 Starting Daily AI Security Scan...")
    
    # 1. Ensure databases are initialized (SQLite and ChromaDB)
    init_databases()
    
    # 2. Define target categories for the scan (Based on MITRE ATLAS)
    # In V2, this list will be fetched dynamically from our bootstrap_taxonomy.
    categories_to_scan = [
        ("MITRE_ATLAS", "AML.T0010: ML Supply Chain Compromise"),
        ("MITRE_ATLAS", "AML.T0051: LLM Prompt Injection"),
        ("MITRE_ATLAS", "AML.T0043: Model Theft")
    ]
    
    print(f"📊 Scheduled to scan {len(categories_to_scan)} categories.")
    print("-" * 40)

    for framework, category in categories_to_scan:
        try:
            print(f"🔎 Investigating: {category}...")
            
            # Use .invoke() because the function is wrapped in a LangChain Tool decorator
            result = research_ai_vulnerability.invoke({
                "framework": framework, 
                "category": category
            })
            
            print(f"✅ Success: {result}")
            
            # Small delay to ensure DB stability and mimic natural scanning
            time.sleep(1) 
            
        except Exception as e:
            print(f"❌ Error scanning {category}: {e}")

    print("-" * 40)
    print("🏁 Scan Operation Complete. Dashboard is now up to date.")

if __name__ == "__main__":
    run_daily_scan()