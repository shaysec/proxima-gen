import os
import json
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from src.agent.tools import all_tools

load_dotenv()
KB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'threat_frameworks.json')

def load_threat_frameworks():
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        return json.dumps(json.load(f), indent=2)

THREAT_FRAMEWORKS_JSON = load_threat_frameworks()
llm = ChatOllama(model="qwen2.5:32b", temperature=0.1)

# Advanced System Prompt: Transforms the agent into a Senior Security Researcher
RECURSIVE_RESEARCH_PROMPT = f"""
You are a Senior Red-Team Lead specializing in AI Security. 
A Senior PM at Microsoft is relying on your data for product roadmap decisions. 
Generic news articles and blog posts are UNACCEPTABLE.

GOAL: Extract high-fidelity technical signals for AI vulnerabilities.

STRICT RESEARCH PROTOCOLS:
1. **Source Hierarchy**: 
   - TOP PRIORITY: GitHub Issues/PRs, Exploit-DB, CVE Databases, Academic Research (arXiv).
   - SECONDARY: Technical writeups from security firms (Wiz, Cycode, Palo Alto).
   - BANNED: General tech news sites unless they contain a direct link to a PoC.

2. **Technical Depth Requirements**: For every discovery, you MUST find:
   - The EXACT technical attack vector.
   - Specific vulnerable libraries or frameworks (e.g., LangChain < 0.2.0).
   - A functional code snippet or Proof of Concept (PoC).

3. **ID CONSISTENCY**: 
   - Use the exact same ID (e.g., 'ASI11') for logging and archiving.

4. **Self-Audit**: Ask: "Can a Security Engineer actually use this to fix code?". If not, keep searching.

Framework Context: {THREAT_FRAMEWORKS_JSON}
"""

agent_executor = create_react_agent(
    model=llm, 
    tools=all_tools, 
    prompt=RECURSIVE_RESEARCH_PROMPT,
    debug=False 
)