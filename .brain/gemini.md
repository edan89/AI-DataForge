# 📜 Gemini — The Constitution

> **This is Law.** Data Schema, Business Rules, Architectural Invariants.

---

## User Brief

**Project:** AI-DataForge — An Agentic Framework for Secure, Automated Data Engineering

**North Star:** Build an end-to-end tool that uses LLM Agents to automate PySpark ETL script creation, generate professional technical documentation, and enforce banking-grade PII masking — simulating an internal tool like OP's "Maiju".

**4 Modules:**
1. **PII Scrubber** — Microsoft Presidio, detect & mask PII before AI sees it
2. **PySpark Code-Gen Agent** — LangChain + Groq/Ollama, NL → PySpark scripts
3. **Data-Wiki Generator** — Auto-generate Markdown data dictionaries
4. **CI/CD Guardrail** — GitHub Action for linting + PII leak scanning

**Integrations:** Groq API (LLM), Microsoft Presidio, Streamlit Cloud, GitHub Actions
**Source of Truth:** Anonymized Kaggle sample datasets
**Payload:** Live Streamlit app + GitHub repo showcasing all modules
**Behavior:**
- DO: Security first, banking-grade PII masking, optimized PySpark code, professional docs
- DO NOT: Expose real PII, hardcode secrets, generate invalid PySpark syntax

---

## Data Schema (JSON)

### PII Scrubber Input/Output
```json
{
  "input": {
    "text": "string | null",
    "dataframe": "CSV file | null",
    "mask_mode": "redact | hash | encrypt"
  },
  "output": {
    "masked_text": "string",
    "masked_dataframe": "CSV",
    "report": {
      "entities_found": [
        { "type": "EMAIL", "count": 0, "confidence": 0.0 }
      ],
      "total_pii_count": 0,
      "columns_with_pii": ["col1"]
    }
  }
}
```

### Code-Gen Agent Input/Output
```json
{
  "input": {
    "prompt": "Clean this insurance data and calculate monthly claim averages",
    "context": "optional schema/column info"
  },
  "output": {
    "code": "# PySpark script string",
    "validation": {
      "syntax_valid": true,
      "has_pyspark_imports": true,
      "warnings": []
    }
  }
}
```

### Data-Wiki Generator Input/Output
```json
{
  "input": {
    "dataframe": "CSV file"
  },
  "output": {
    "markdown": "# Data Dictionary\n...",
    "columns": [
      {
        "name": "col1",
        "type": "int64",
        "description": "LLM-generated description",
        "null_rate": 0.05,
        "unique_count": 100,
        "sample_values": ["a", "b"]
      }
    ]
  }
}
```

---

## Business Rules

1. PII must be masked BEFORE any data reaches the LLM
2. Generated PySpark code must pass syntax validation
3. All secrets in `.env`, never in code
4. CI/CD must block commits containing PII patterns

---

## Architectural Invariants

1. **3-Layer Model:** Architecture SOPs → Agent Navigation → Atomic Tools
2. **Security-first:** Presidio scan runs before any data processing
3. **Zero-trust for LLM output:** All generated code validated before display
4. **Modular design:** Each module is independently testable
