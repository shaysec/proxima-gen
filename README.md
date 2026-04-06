# 🛡️ PROXIMA-GEN | The Autonomous AI Security Factory

**From 386 Raw Signals to 9 Verified Exploits.** PROXIMA-GEN is an autonomous threat intelligence system designed to discover, research, and verify vulnerabilities in AI Agents and LLM frameworks. It transforms raw security noise into high-fidelity, actionable intelligence.

---

## 💸 The "Zero-Cost" Philosophy
PROXIMA-GEN was born out of a strict **Zero-Cost** mindset. In an era of expensive cloud APIs and proprietary security tools, we chose to rely entirely on local infrastructure. By running everything on-prem, we ensure:
* **Absolute Privacy:** Your research data never leaves your hardware.
* **Zero Operating Expenses:** No per-token costs or monthly subscriptions.
* **Full Control:** You own the intelligence factory from end to end.

## 🤖 The Sentinel Architecture
PROXIMA-GEN operates as a collective of autonomous units, inspired by the concept of specialized, self-evolving machines. Each unit in the factory has a specific role in the transformation of data:
* **Core-Unit:** The central reasoning engine powered by **Qwen 2.5 32B**.
* **Sentinel-Scan:** Our frontline discovery agent, constantly monitoring for emerging threats.
* **Vector-Research:** Specialized in technical validation, deep-diving into GitHub issues and academic papers to find functional PoCs.
* **Forge-Master:** The reporting unit that enriches raw data into structured security reports with Impact and Mitigation analysis.

## 🏗️ Tech Stack & Hardware
* **Inference:** [Ollama](https://ollama.com/) running **Qwen 2.5 32B**.
* **Orchestration:** LangGraph / LangChain ReAct loops.
* **Package Management:** [uv](https://github.com/astral-sh/uv) - Ultra-fast Python project management.
* **Hardware Optimized:** Developed and battle-tested on **AMD Radeon RX 6800 XT** (via DirectML/ROCm).
    * *Compatibility Note:* While optimized for the 6800XT, PROXIMA-GEN is designed to be hardware-agnostic. It may run on lower-spec hardware or with smaller models (e.g., 7B/8B), but this has not been officially tested and PoC quality may vary.

## 🚀 Quick Start

### 1. Prerequisites
* Install **Ollama** and pull the model: `ollama pull qwen2.5:32b`
* Install **uv**: `powershell -c "ir | iex"`

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/YOUR_USER/proxima-gen.git](https://github.com/YOUR_USER/proxima-gen.git)
cd proxima-gen

# Sync environment and dependencies
uv sync