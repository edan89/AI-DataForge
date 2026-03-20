"""
Page 1: 🔒 PII Scanner

Upload a CSV or enter text → scan for PII → view detections → download masked version.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd

from core.pii_scrubber import PIIScrubber, MaskMode
from ui.components.styles import THEME_CSS, SIDEBAR_LOGO

# Page config
st.set_page_config(page_title="PII Scanner | AI-DataForge", page_icon="🔒", layout="wide")
st.markdown(THEME_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(SIDEBAR_LOGO, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.markdown('<p class="hero-title">🔒 PII Scanner</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">'
    "Banking-grade PII detection & masking powered by Microsoft Presidio"
    "</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Initialize scrubber (cached)
@st.cache_resource
def get_scrubber():
    return PIIScrubber()

scrubber = get_scrubber()

# ---------------------------------------------------------------------------
# Input Mode Selection
# ---------------------------------------------------------------------------

tab_text, tab_csv = st.tabs(["📝 Text Input", "📄 CSV Upload"])

# ---------------------------------------------------------------------------
# Tab 1: Text Input
# ---------------------------------------------------------------------------

with tab_text:
    st.markdown("#### Enter text to scan for PII")

    sample_text = (
        "Contact John Smith at john.smith@bank.fi or call +358401234567. "
        "His SSN is 123-45-6789 and IBAN is FI2112345600000785."
    )

    text_input = st.text_area(
        "Text to scan",
        value=sample_text,
        height=150,
        label_visibility="collapsed",
    )

    col_scan, col_mode = st.columns([1, 1])
    with col_mode:
        mask_mode = st.selectbox(
            "Masking Mode",
            options=[m.value for m in MaskMode],
            format_func=lambda x: {
                "redact": "🔴 Redact (replace with <MASKED>)",
                "hash": "🔵 Hash (SHA-256)",
                "replace": "🟢 Replace (synthetic fake data) ✨",
            }.get(x, x),
        )

    with col_scan:
        scan_btn = st.button("🔍 Scan & Mask", type="primary", use_container_width=True)

    if scan_btn and text_input:
        with st.spinner("Scanning for PII..."):
            detections = scrubber.scan_text(text_input)
            masked = scrubber.mask_text(text_input, MaskMode(mask_mode))

        # Results
        st.markdown("---")

        if detections:
            st.success(f"✅ Found **{len(detections)}** PII entities")

            # Detection details
            det_data = [
                {
                    "Entity Type": d.entity_type,
                    "Detected Text": d.text,
                    "Confidence": f"{d.confidence:.0%}",
                }
                for d in detections
            ]
            st.dataframe(
                pd.DataFrame(det_data),
                use_container_width=True,
                hide_index=True,
            )

            # Masked output
            st.markdown("#### Masked Output")
            st.code(masked, language=None)
        else:
            st.info("ℹ️ No PII detected in the provided text.")

# ---------------------------------------------------------------------------
# Tab 2: CSV Upload
# ---------------------------------------------------------------------------

with tab_csv:
    st.markdown("#### Upload a CSV file to scan for PII")

    uploaded = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file. All string columns will be scanned for PII.",
    )

    if uploaded is not None:
        df = pd.read_csv(uploaded)

        st.markdown(f"**Preview** ({len(df)} rows × {len(df.columns)} columns)")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)

        col_scan2, col_mode2 = st.columns([1, 1])
        with col_mode2:
            csv_mask_mode = st.selectbox(
                "Masking Mode ",
                options=[m.value for m in MaskMode],
                format_func=lambda x: {
                    "redact": "🔴 Redact",
                    "hash": "🔵 Hash",
                    "replace": "🟢 Replace",
                }.get(x, x),
                key="csv_mode",
            )

        with col_scan2:
            csv_scan = st.button(
                "🔍 Scan DataFrame", type="primary", use_container_width=True
            )

        if csv_scan:
            with st.spinner("Scanning all columns for PII... This may take a moment."):
                report = scrubber.scan_dataframe(df)

            st.markdown("---")

            # Summary metrics
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total PII Found", report.total_pii_count)
            with m2:
                st.metric("Entity Types", len(report.entities_by_type))
            with m3:
                st.metric("Columns Affected", len(report.columns_with_pii))

            if report.total_pii_count > 0:
                # Entity breakdown
                st.markdown("#### Entity Breakdown")
                ent_df = pd.DataFrame(
                    [
                        {"Entity Type": k, "Count": v}
                        for k, v in report.entities_by_type.items()
                    ]
                )
                st.dataframe(ent_df, use_container_width=True, hide_index=True)

                # Columns with PII
                st.markdown(f"**Columns with PII:** {', '.join(report.columns_with_pii)}")

                # Mask button
                if st.button("🛡️ Generate Masked Dataset", type="primary"):
                    with st.spinner("Masking PII..."):
                        masked_df = scrubber.mask_dataframe(df, MaskMode(csv_mask_mode))

                    st.markdown("#### Masked Preview")
                    st.dataframe(
                        masked_df.head(10), use_container_width=True, hide_index=True
                    )

                    # Download
                    csv_buffer = masked_df.to_csv(index=False)
                    st.download_button(
                        "⬇️ Download Masked CSV",
                        data=csv_buffer,
                        file_name="masked_data.csv",
                        mime="text/csv",
                        type="primary",
                    )
            else:
                st.info("ℹ️ No PII detected in the uploaded file.")
