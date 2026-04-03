import sqlite3
import chromadb
import os
from datetime import datetime
from langchain_core.tools import tool

# Resolve paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SQLITE_DB_PATH = os.path.join(BASE_DIR, 'data', 'ai_vulnerabilities.db')
CHROMA_DB_PATH = os.path.join(BASE_DIR, 'data', 'chroma_db')

# Global Taxonomy (Will be dynamic in V2, currently semi-dynamic)
AI_SECURITY_FRAMEWORKS = {
    "MITRE_ATLAS": {
        "AML.T0010: ML Supply Chain Compromise": ["supply chain", "malicious package", "trivy ai"],
        "AML.T0051: LLM Prompt Injection": ["prompt injection", "jailbreak"],
        "AML.T0043: Model Theft": ["model theft", "source code leak", "claude leak"]
    }
}

def save_to_databases(cve_id, framework, category, description, severity="High"):
    """Saves finding to both SQLite and ChromaDB."""
    # 1. Save to SQLite
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    discovery_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO vulnerabilities (discovery_date, cve_id, framework, category, description, severity)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (discovery_date, cve_id, framework, category, description, severity))
    conn.commit()
    conn.close()

    # 2. Save to ChromaDB
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = chroma_client.get_or_create_collection(name="ai_threat_intel")
    collection.add(
        documents=[description],
        metadatas=[{"cve_id": cve_id, "framework": framework, "category": category, "date": discovery_date}],
        ids=[f"{cve_id}_{datetime.now().timestamp()}"]
    )

@tool
def research_ai_vulnerability(framework: str, category: str) -> str:
    """
    Research a specific AI vulnerability category. 
    It simulates a deep scan and saves results to the local databases.
    """
    if framework not in AI_SECURITY_FRAMEWORKS or category not in AI_SECURITY_FRAMEWORKS[framework]:
        return "Error: Category or Framework not recognized."
    
    # Simulation of finding a vulnerability (In reality, this calls NVD/ArXiv APIs)
    mock_description = f"New potential weakness discovered in {category} involving nested tensor manipulation."
    cve_mock = f"CVE-2026-{int(datetime.now().timestamp()) % 10000}"
    
    save_to_databases(cve_mock, framework, category, mock_description)
    
    return f"Successfully researched {category}. Found: {cve_mock}. Data persisted to DB."

agent_tools = [research_ai_vulnerability]