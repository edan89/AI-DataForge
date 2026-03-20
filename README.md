# ⚡ AI-DataForge: Enterprise-Grade Data Engineering Assistant

An Agentic Framework for Secure, Automated Data Engineering, built to simulate a production internal tool for banking and finance. 

**AI-DataForge** solves the core bottleneck in modern data pipelines: writing boilerplate ETL code while strictly adhering to data privacy laws (GDPR/CCPA). It combines **Agentic AI (LangChain + Llama 3)** with **Enterprise NLP (Microsoft Presidio)** to automatically scrub sensitive PII and generate production-ready PySpark scripts.

---

## 🌟 Core Modules

### 1. 🔒 PII Scrubber (Security First)
*The cornerstone of the application, ensuring no sensitive data ever leaks to the LLM or third parties.*
- **NLP Engine:** Uses Microsoft Presidio for automated detection & masking.
- **Coverage:** Out-of-the-box support for Names, Emails, Phone Numbers, Credit Cards, IBANs, and SSNs.
- **Modes:** 🔴 `REDACT` (mask tags), 🔵 `HASH` (SHA-256 for deterministic tracking), and 🟢 `REPLACE` (Zero-dependency Synthetic Fake Data generator).
- **Scale:** Seamlessly handles both raw text and massive pandas DataFrames.

### 2. ⚡ PySpark Code-Gen Agent (Productivity)
*An intelligent AI pair-programmer dedicated to data transformation.*
- **AI Stack:** LangChain orchestration powered by Groq's lightning-fast **Llama 3.3 70B** model.
- **Context-Aware:** Ingests CSV schemas to generate highly accurate, column-aware PySpark (`pyspark.sql`) scripts.
- **Self-Healing:** Built-in Python AST (Abstract Syntax Tree) validation automatically detects syntax errors and forces the LLM to self-correct before presenting code to the user.

### 3. 📚 Data-Wiki Generator (Documentation)
*Automating the most tedious part of Data Engineering: Documentation.*
- Automatically profiles uploaded datasets (calculating null rates, types, and basic statistics).
- Uses the LLM to generate professional, business-friendly Markdown descriptions for every column.

### 4. 🛡️ CI/CD Guardrail (DevOps)
*Enterprise standards enforced at the repository level.*
- GitHub Action workflows enforcing `ruff` linting and running 50+ `pytest` unit tests.
- Automated pipeline scanning for hardcoded secrets and PII leaks on every push to production.

---

## 🏗️ Technology Stack

- **Frontend:** Streamlit (with a custom premium Dark Mode & Glassmorphism UI)
- **AI / LLM:** LangChain, Groq API (Llama-3.3-70b-versatile)
- **Security / NLP:** Microsoft Presidio, spaCy
- **Data:** pandas, PySpark (Target Output)
- **DevOps:** GitHub Actions, Pytest, Ruff

---

## 🚀 Getting Started

### 1. Requirements
- Python 3.11+
- [Groq API Key](https://console.groq.com) (Free Tier available)

### 2. Installation & Setup
```bash
# Clone the repository
git clone <repo-url>
cd AI-DataForge

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\\venv\\Scripts\\Activate.ps1

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

### 3. Configuration
Copy the `.env.example` file to a new `.env` file and securely add your API key:
```bash
cp .env.example .env
# Edit .env and insert your GROQ_API_KEY
```

### 4. Launch the Application
```bash
streamlit run ui/app.py
```
