"""
AI-DataForge — Streamlit Main Application

Multi-page dashboard for secure, automated data engineering.
Entry point: `streamlit run ui/app.py`
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from ui.components.styles import THEME_CSS, SIDEBAR_LOGO

# ---------------------------------------------------------------------------
# Page Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI-DataForge",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply theme
st.markdown(THEME_CSS, unsafe_allow_html=True)

# Sidebar branding
with st.sidebar:
    st.markdown(SIDEBAR_LOGO, unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🧭 Navigation")
    st.markdown(
        """
        Use the pages in the sidebar to access each module:
        - **🔒 PII Scanner** — Detect & mask sensitive data
        - **⚡ Code Generator** — NL → PySpark scripts
        - **📚 Data Wiki** — Auto-generate data dictionaries
        """
    )
    st.divider()
    st.markdown(
        '<div style="color: #B0B3B8; font-size: 0.7rem; text-align: center;">'
        "Built with ❤️ using LangChain, Presidio & Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Main Page — Hero
# ---------------------------------------------------------------------------

st.markdown(
    '<p class="hero-title">AI-DataForge</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="hero-subtitle">An Agentic Framework for Secure, Automated Data Engineering</p>',
    unsafe_allow_html=True,
)

st.markdown("---")

# ---------------------------------------------------------------------------
# Module Overview Cards
# ---------------------------------------------------------------------------

st.markdown("### 🧩 Modules")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="module-card">
            <span class="badge badge-security">Security</span>
            <h3 style="margin-top: 12px;">🔒 PII Scrubber</h3>
            <p style="color: #B0B3B8;">
                Banking-grade PII detection & masking powered by Microsoft Presidio.
                Detects Names, Emails, Phone Numbers, Credit Cards, IBANs, and SSNs.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="module-card">
            <span class="badge badge-docs">Documentation</span>
            <h3 style="margin-top: 12px;">📚 Data-Wiki Generator</h3>
            <p style="color: #B0B3B8;">
                Automatically generates professional Markdown data dictionaries
                with column profiles, statistics, and LLM-powered descriptions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="module-card">
            <span class="badge badge-ai">AI Agent</span>
            <h3 style="margin-top: 12px;">⚡ PySpark Code-Gen</h3>
            <p style="color: #B0B3B8;">
                LangChain agent that generates optimized PySpark ETL scripts
                from natural language, with built-in code validation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="module-card">
            <span class="badge badge-devops">DevOps</span>
            <h3 style="margin-top: 12px;">🛡️ CI/CD Guardrail</h3>
            <p style="color: #B0B3B8;">
                GitHub Action that lints code, runs tests, and performs
                security scans for PII leaks on every push.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------------------------------------------------------------------------
# Tech Stack & Architecture
# ---------------------------------------------------------------------------

st.markdown("### ⚙️ Tech Stack")

tech_cols = st.columns(6)
tech_items = [
    ("🐍", "PySpark"),
    ("🦜", "LangChain"),
    ("🤖", "Groq / Llama 3"),
    ("🔐", "Presidio"),
    ("📊", "Streamlit"),
    ("⚙️", "GitHub Actions"),
]
for col, (icon, name) in zip(tech_cols, tech_items):
    with col:
        st.markdown(
            f"""
            <div style="
                text-align: center;
                background: #1A1D23;
                border: 1px solid #2D3139;
                border-radius: 12px;
                padding: 16px 8px;
                transition: all 0.3s ease;
            ">
                <div style="font-size: 1.8rem;">{icon}</div>
                <div style="color: #FAFAFA; font-size: 0.85rem; margin-top: 8px; font-weight: 600;">
                    {name}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# Architecture diagram
st.markdown("### 🏗️ Architecture")
st.markdown(
    """
    ```
    ┌─────────────────────────────────────────────────────────────┐
    │                    Streamlit Frontend                        │
    │  ┌──────────┐  ┌──────────────┐  ┌──────────────────────┐  │
    │  │PII Scan  │  │Code Generator│  │  Data Wiki Generator │  │
    │  └────┬─────┘  └──────┬───────┘  └──────────┬───────────┘  │
    ├───────┼────────────────┼─────────────────────┼──────────────┤
    │       ▼                ▼                     ▼              │
    │  ┌─────────┐    ┌────────────┐    ┌─────────────────────┐  │
    │  │Presidio │    │ LangChain  │    │ Pandas + LLM        │  │
    │  │Analyzer │    │ + Groq API │    │ (Column Profiler)   │  │
    │  └─────────┘    └────────────┘    └─────────────────────┘  │
    ├─────────────────────────────────────────────────────────────┤
    │           GitHub Actions CI/CD Guardrail                    │
    │     (Ruff Lint → Pytest → PII Leak Scan → Secret Scan)     │
    └─────────────────────────────────────────────────────────────┘
    ```
    """
)

st.markdown(
    """
    > **Azure Mapping:** In a production banking environment, this architecture would map to:
    > - **Streamlit** → **Azure AI Foundry** (model deployment & UI)
    > - **LangChain Agent** → **Azure Copilot Studio** (agent orchestration)
    > - **Presidio** → **Microsoft Purview** (compliance & data governance)
    > - **GitHub Actions** → **Azure DevOps Pipelines** (CI/CD)
    > - **PySpark** → **Azure Databricks** (data processing)
    """
)
