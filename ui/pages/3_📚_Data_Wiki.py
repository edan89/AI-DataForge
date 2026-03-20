"""
Page 3: 📚 Data Wiki

Upload a CSV → auto-generate a professional Markdown data dictionary → download.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd

from agents.wiki_generator import WikiGenerator
from ui.components.styles import THEME_CSS, SIDEBAR_LOGO

# Page config
st.set_page_config(page_title="Data Wiki | AI-DataForge", page_icon="📚", layout="wide")
st.markdown(THEME_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(SIDEBAR_LOGO, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.markdown('<p class="hero-title">📚 Data Wiki Generator</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">'
    "Automatically generate professional data dictionaries for any dataset"
    "</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

col_name, col_llm = st.columns([2, 1])

with col_name:
    dataset_name = st.text_input(
        "Dataset Name",
        value="Insurance Claims",
        help="This name will appear in the generated documentation.",
    )

with col_llm:
    api_key = os.getenv("GROQ_API_KEY", "")
    use_llm = st.toggle(
        "🤖 Use AI descriptions",
        value=bool(api_key),
        help="Enable LLM-powered column descriptions. Requires Groq API key.",
    )

if use_llm and not api_key:
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        key="wiki_api_key",
    )

# ---------------------------------------------------------------------------
# File Upload
# ---------------------------------------------------------------------------

st.markdown("#### Upload Dataset")

uploaded = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    help="Upload a CSV file to generate its data dictionary.",
    key="wiki_upload",
)

if uploaded is not None:
    df = pd.read_csv(uploaded)

    st.markdown(f"**Preview** ({len(df)} rows × {len(df.columns)} columns)")
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)

    st.markdown("---")

    # Quick stats
    st.markdown("#### Quick Stats")
    stat_cols = st.columns(4)
    with stat_cols[0]:
        st.metric("Rows", f"{len(df):,}")
    with stat_cols[1]:
        st.metric("Columns", len(df.columns))
    with stat_cols[2]:
        st.metric("Numeric Cols", len(df.select_dtypes(include="number").columns))
    with stat_cols[3]:
        null_pct = df.isnull().mean().mean()
        st.metric("Avg Null Rate", f"{null_pct:.1%}")

    st.markdown("---")

    # Generate button
    generate_btn = st.button(
        "📚 Generate Data Wiki",
        type="primary",
        use_container_width=True,
    )

    if generate_btn:
        with st.spinner("Generating data dictionary..."):
            try:
                generator = WikiGenerator(
                    api_key=api_key if use_llm else None,
                    use_llm=use_llm and bool(api_key),
                )
                wiki = generator.generate(df, dataset_name=dataset_name)
                markdown_output = wiki.to_markdown()

                st.markdown("---")
                st.markdown("#### Generated Data Dictionary")

                # Show in tabs: rendered vs raw
                tab_render, tab_raw = st.tabs(["📖 Rendered", "📝 Raw Markdown"])

                with tab_render:
                    st.markdown(markdown_output)

                with tab_raw:
                    st.code(markdown_output, language="markdown")

                # Download
                st.download_button(
                    "⬇️ Download Data Dictionary",
                    data=markdown_output,
                    file_name=f"{dataset_name.lower().replace(' ', '_')}_wiki.md",
                    mime="text/markdown",
                    type="primary",
                )

            except Exception as e:
                st.error(f"❌ Generation failed: {str(e)}")
else:
    # Show sample when no file uploaded
    st.info(
        "👆 Upload a CSV file to get started, or use the sample data in `data/sample_insurance.csv`"
    )
