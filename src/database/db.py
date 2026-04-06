import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'data', 'ai_vulnerabilities.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discovery_date TEXT,
            source_links TEXT,
            framework TEXT,
            category_id TEXT,
            title TEXT UNIQUE,
            description TEXT,
            attack_vector TEXT,
            technical_proof TEXT,
            impact TEXT,
            severity TEXT,
            is_breaking_news INTEGER DEFAULT 1,
            raw_content TEXT,
            use_case TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"✅ DB Initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()