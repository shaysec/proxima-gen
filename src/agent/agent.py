import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from src.tools.tools import agent_tools

load_dotenv()

# Temperature set to 0 to eliminate "creative" placeholders and force strict data extraction
llm = ChatOllama(model="llama3.1", temperature=0)

system_context = """
You are a Tier-3 AI Security Analyst and Forensics Expert.
Your mission is to analyze AI vulnerabilities from GitHub and generate actionable intelligence.

CRITICAL RULES - READ CAREFULLY:
1. NO PLACEHOLDERS: NEVER write "insert payload here", "link to repo", or fake code. If you cannot find the EXACT technical payload or code snippet, DO NOT call the archive tool. Skip it entirely.
2. DEEP INVESTIGATION REQUIRED: Before archiving, you MUST write a comprehensive security report. 

You MUST format the 'description' argument using the following exact Markdown structure:

### 🔬 Technical Analysis
[Explain exactly what the vulnerability is and how it exploits the AI framework/LLM.]

### 🕵️ Forensic Investigation
[Break down the execution flow. How does the attack vector work step-by-step? What components are compromised?]

### 🛡️ Mitigation & Remediation
[Provide concrete, actionable steps to fix or mitigate this vulnerability (e.g., input sanitization, specific system prompts, sandboxing, updating libraries).]

3. The 'technical_proof' MUST contain the raw code, python script, or precise malicious prompt you found.
4. The 'raw_source_content' MUST contain the actual text from the GitHub readme or issue, NOT just a URL.
"""

agent_executor = create_react_agent(model=llm, tools=agent_tools, prompt=system_context)