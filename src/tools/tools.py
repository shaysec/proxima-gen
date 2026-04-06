import sqlite3
import os
from github import Github 
from tavily import TavilyClient
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Path Definitions
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'data', 'ai_vulnerabilities.db')

# --- Input Schemas for Structured Tools ---
class GitHubSearchInput(BaseModel):
    query: str = Field(description="Single search string for GitHub repositories")

class TavilySearchInput(BaseModel):
    query: str = Field(description="Search query for AI security research")

# --- Tool Definitions ---

@tool("tavily_search", args_schema=TavilySearchInput)
def tavily_search_tool(query: str):
    """Search the web for emerging AI security threats and research."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key: return "Error: TAVILY_API_KEY missing."
    try:
        client = TavilyClient(api_key=api_key)
        results = client.search(query=query, search_depth="advanced")
        return "\n\n".join([f"URL: {r['url']}\nContent: {r['content'][:400]}..." for r in results.get('results', [])])
    except Exception as e: return f"Tavily Error: {e}"

@tool("github_search", args_schema=GitHubSearchInput)
def github_search_tool(query: str):
    """Search GitHub for PoC code and technical vulnerability details."""
    token = os.getenv("GITHUB_TOKEN")
    if not token: return "Error: GITHUB_TOKEN missing."
    try:
        g = Github(token)
        clean_query = query.split(',')[0] if isinstance(query, str) else str(query)
        repositories = g.search_repositories(query=clean_query)
        results = [f"Repo: {repo.full_name} | URL: {repo.html_url}" for repo in repositories[:5]]
        return "\n".join(results) if results else "No GitHub matches found."
    except Exception as e: return f"GitHub Error: {e}"

@tool
def archive_verified_vulnerability(category_id: str, title: str, description: str, technical_proof: str, severity: str = "HIGH", impact_analysis: str = None, mitigation_steps: str = None):
    """MANDATORY: Archives a finalized security report. REJECTS generic/empty reports."""
    bad_phrases = ["further research", "insert code", "example poc", "tbd"]
    if any(phrase in technical_proof.lower() for phrase in bad_phrases):
        return "❌ REJECTED: Technical proof is too generic."
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Support for Actionable Intel columns (Impact & Mitigation)
        cursor.execute('''
            INSERT OR REPLACE INTO vulnerabilities 
            (discovery_date, category_id, title, description, technical_proof, severity, impact_analysis, mitigation_steps) 
            VALUES (date('now'), ?, ?, ?, ?, ?, ?, ?)
        ''', (category_id, title, description, technical_proof, severity, impact_analysis, mitigation_steps))
        conn.commit()
        conn.close()
        return f"✅ Archived & Enriched: {title}"
    except Exception as e: return f"Archive Error: {e}"

@tool
def log_research_artifact(vulnerability_id: str, source_type: str, url: str, content_snippet: str):
    """Logs raw research artifacts (URLs/Snippets) during the discovery phase."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO research_artifacts (vulnerability_id, source_type, url, content_snippet) VALUES (?, ?, ?, ?)', 
                       (vulnerability_id, source_type, url, content_snippet))
        conn.commit()
        conn.close()
        return f"✅ Artifact logged: {url}"
    except Exception as e: return f"Log Error: {e}"

# --- Exporting tools under both names for compatibility ---
all_tools = [tavily_search_tool, github_search_tool, archive_verified_vulnerability, log_research_artifact]
agent_tools = all_tools # Backward compatibility for legacy agent scripts