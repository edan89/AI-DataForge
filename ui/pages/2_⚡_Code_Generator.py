"""
Page 2: ⚡ Code Generator

Enter a natural language prompt → get an optimized PySpark script → copy/download.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd

from ui.components.styles import THEME_CSS, SIDEBAR_LOGO

# Page config
st.set_page_config(page_title="Code Generator | AI-DataForge", page_icon="⚡", layout="wide")
st.markdown(THEME_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(SIDEBAR_LOGO, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.markdown('<p class="hero-title">⚡ PySpark Code Generator</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">'
    "LangChain agent that generates optimized PySpark ETL scripts from natural language"
    "</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ---------------------------------------------------------------------------
# API Key Check
# ---------------------------------------------------------------------------

api_key = os.getenv("GROQ_API_KEY", "")

if not api_key:
    st.warning(
        "⚠️ **Groq API Key Required** — Set `GROQ_API_KEY` in your `.env` file "
        "or enter it below to use the code generator."
    )
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get a free key at https://console.groq.com",
    )

# ---------------------------------------------------------------------------
# Prompt Input
# ---------------------------------------------------------------------------

st.markdown("#### Describe your ETL task")

sample_prompts = [
    "Clean this insurance data and calculate monthly claim averages by policy type",
    "Read a CSV, remove duplicates, filter rows where amount > 1000, and save as Parquet",
    "Join customer and orders tables, aggregate total spend per customer, and rank them",
    "Read JSON logs, extract error messages, count errors by date, and write to Delta table",
]

selected_sample = st.selectbox(
    "💡 Try a sample prompt",
    options=["— Write your own —"] + sample_prompts,
)

if selected_sample != "— Write your own —":
    default_prompt = selected_sample
else:
    default_prompt = ""

prompt = st.text_area(
    "ETL Task Description",
    value=default_prompt,
    height=120,
    placeholder="e.g., Read a CSV of insurance claims, clean null values, calculate average claim amount by month...",
    label_visibility="collapsed",
)

# Optional: upload CSV for schema context
with st.expander("📎 Optional: Upload CSV for schema context"):
    context_file = st.file_uploader(
        "Upload a sample CSV to provide column information",
        type=["csv"],
        key="codegen_csv",
    )
    context_df = None
    if context_file:
        context_df = pd.read_csv(context_file)
        st.dataframe(context_df.head(5), use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Generate Button
# ---------------------------------------------------------------------------

generate_btn = st.button("⚡ Generate PySpark Code", type="primary", use_container_width=True)

if generate_btn:
    if not prompt:
        st.error("Please enter a task description.")
    elif not api_key:
        st.error("Please provide a Groq API key.")
    else:
        with st.spinner("🤖 Agent is generating your PySpark script..."):
            try:
                from agents.codegen_agent import PySparkCodeGenAgent

                agent = PySparkCodeGenAgent(api_key=api_key)
                result = agent.generate(prompt, df=context_df)

                st.markdown("---")

                # Validation badges
                v = result.validation
                col_syntax, col_pyspark = st.columns(2)
                with col_syntax:
                    if v.syntax_valid:
                        st.success("✅ Syntax Valid")
                    else:
                        st.error("❌ Syntax Errors Found")
                with col_pyspark:
                    if v.has_pyspark_imports:
                        st.success("✅ PySpark Imports Detected")
                    else:
                        st.warning("⚠️ No PySpark Imports")

                # Show errors/warnings
                for err in v.errors:
                    st.error(f"Error: {err}")
                for warn in v.warnings:
                    st.warning(f"Warning: {warn}")

                # Generated code
                st.markdown("#### Generated PySpark Script")
                st.code(result.code, language="python")

                # Download button
                st.download_button(
                    "⬇️ Download Script",
                    data=result.code,
                    file_name="etl_script.py",
                    mime="text/x-python",
                    type="primary",
                )

                # Model info
                with st.expander("ℹ️ Generation Details"):
                    st.json({
                        "model": result.model,
                        "prompt_used": result.prompt_used,
                        "validation": result.validation.to_dict(),
                    })

            except Exception as e:
                st.error(f"❌ Generation failed: {str(e)}")
