import sqlite3
import chromadb
import os

# ==========================================
# Database Configuration & Paths
# ==========================================
# Resolve absolute paths based on the current file location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQLITE_DB_PATH = os.path.join(DATA_DIR, 'ai_vulnerabilities.db')
CHROMA_DB_PATH = os.path.join(DATA_DIR, 'chroma_db')

def init_databases():
    """
    Initializes both SQLite (for tabular reporting) 
    and ChromaDB (for Agent RAG/semantic search).
    """
    print("Initializing databases...")
    
    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # ---------------------------------------------------------
    # 1. Initialize SQLite (Relational DB for Dashboards)
    # ---------------------------------------------------------
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        # Create the main vulnerabilities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discovery_date TEXT NOT NULL,
                cve_id TEXT,
                framework TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ SQLite database initialized successfully.")
    except Exception as e:
        print(f"❌ Error initializing SQLite: {e}")

    # ---------------------------------------------------------
    # 2. Initialize ChromaDB (Vector DB for Agent Memory)
    # ---------------------------------------------------------
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        # Create or get the collection for AI threats
        collection = chroma_client.get_or_create_collection(name="ai_threat_intel")
        print("✅ ChromaDB vector database initialized successfully.")
    except Exception as e:
        print(f"❌ Error initializing ChromaDB: {e}")

if __name__ == "__main__":
    # Run initialization when the script is executed directly
    init_databases()