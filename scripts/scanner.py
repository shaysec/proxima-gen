import sys
import os
import sqlite3
import json
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.agent.multi_agents import agent_executor, load_threat_frameworks

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'ai_vulnerabilities.db')

def run_factory_cycle():
    print("\n🕵️ PHASE 1: DISCOVERING...")
    agent_executor.invoke({"messages": [HumanMessage(content="Find new AI agent threats.")]})

    print("\n🔍 PHASE 2: DEEP DIVE...")
    frameworks = json.loads(load_threat_frameworks())
    conn = sqlite3.connect(DB_PATH)
    
    for fw, items in frameworks.items():
        for item in items:
            t_id = item['id']
            # Check if a verified report already exists
            exists = conn.execute("SELECT id FROM vulnerabilities WHERE category_id = ?", (t_id,)).fetchone()
            if exists:
                print(f"⏩ Skipping {t_id} - Already verified.")
                continue

            print(f"🔬 Investigating {t_id}...")
            agent_executor.invoke({"messages": [HumanMessage(content=f"Research {t_id}. Only archive if a REAL PoC is found.")]})
    conn.close()

if __name__ == "__main__":
    run_factory_cycle()