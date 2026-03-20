"""
Unit tests for Module 1: PII Scrubber.

Tests PII detection and masking for text strings and DataFrames,
including edge cases and custom banking recognizers.
"""

import pytest
import pandas as pd

from core.pii_scrubber import PIIScrubber, MaskMode


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def scrubber():
    """Create a fresh PIIScrubber instance."""
    return PIIScrubber()


@pytest.fixture
def sample_df():
    """Sample DataFrame with PII data."""
    return pd.DataFrame({
        "name": ["John Smith", "Jane Doe", "Bob Wilson"],
        "email": ["john@example.com", "jane@bank.fi", "bob@test.org"],
        "phone": ["+358401234567", "+1-555-0100", "+44 20 7946 0958"],
        "amount": [1500.00, 2300.50, 890.25],
        "notes": [
            "Contact via john@example.com",
            "Customer Jane Doe prefers email",
            "No special notes",
        ],
    })


@pytest.fixture
def clean_df():
    """Sample DataFrame without PII data."""
    return pd.DataFrame({
        "product_id": ["P001", "P002", "P003"],
        "price": [29.99, 49.99, 99.99],
        "category": ["electronics", "clothing", "furniture"],
    })


# ---------------------------------------------------------------------------
# Text Scanning Tests
# ---------------------------------------------------------------------------

class TestScanText:
    """Tests for PIIScrubber.scan_text()."""

    def test_detect_email(self, scrubber):
        detections = scrubber.scan_text("Contact me at john@example.com")
        entity_types = [d.entity_type for d in detections]
        assert "EMAIL_ADDRESS" in entity_types

    def test_detect_phone(self, scrubber):
        detections = scrubber.scan_text("Call me at +358401234567")
        entity_types = [d.entity_type for d in detections]
        assert "PHONE_NUMBER" in entity_types

    def test_detect_person_name(self, scrubber):
        detections = scrubber.scan_text("Meeting with John Smith tomorrow")
        entity_types = [d.entity_type for d in detections]
        assert "PERSON" in entity_types

    def test_detect_multiple_entities(self, scrubber):
        text = "John Smith (john@bank.com, +358401234567) signed the contract."
        detections = scrubber.scan_text(text)
        assert len(detections) >= 3  # At least: PERSON, EMAIL, PHONE

    def test_empty_string(self, scrubber):
        assert scrubber.scan_text("") == []

    def test_none_input(self, scrubber):
        assert scrubber.scan_text(None) == []

    def test_no_pii(self, scrubber):
        detections = scrubber.scan_text("The product costs 29.99 euros")
        # May detect some entities, but core PII types should be absent
        pii_types = {"EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "US_SSN"}
        detected_types = {d.entity_type for d in detections}
        assert not pii_types.intersection(detected_types)

    def test_detection_has_confidence(self, scrubber):
        detections = scrubber.scan_text("Email: test@example.com")
        for d in detections:
            assert 0.0 <= d.confidence <= 1.0


# ---------------------------------------------------------------------------
# Text Masking Tests
# ---------------------------------------------------------------------------

class TestMaskText:
    """Tests for PIIScrubber.mask_text()."""

    def test_redact_mode(self, scrubber):
        masked = scrubber.mask_text("Email: john@example.com", MaskMode.REDACT)
        assert "john@example.com" not in masked
        assert "<MASKED>" in masked

    def test_replace_mode(self, scrubber):
        masked = scrubber.mask_text("Email: john@example.com", MaskMode.REPLACE)
        assert "john@example.com" not in masked
        assert "@" in masked  # Should be replaced by a synthetic fake email

    def test_hash_mode(self, scrubber):
        masked = scrubber.mask_text("Email: john@example.com", MaskMode.HASH)
        assert "john@example.com" not in masked

    def test_empty_string(self, scrubber):
        assert scrubber.mask_text("") == ""

    def test_no_pii_unchanged(self, scrubber):
        text = "Product price is 29.99"
        masked = scrubber.mask_text(text, MaskMode.REDACT)
        # Text without PII should remain mostly unchanged
        assert "29.99" in masked


# ---------------------------------------------------------------------------
# DataFrame Tests
# ---------------------------------------------------------------------------

class TestScanDataFrame:
    """Tests for PIIScrubber.scan_dataframe()."""

    def test_detects_pii_in_columns(self, scrubber, sample_df):
        report = scrubber.scan_dataframe(sample_df)
        assert report.total_pii_count > 0
        assert len(report.columns_with_pii) > 0

    def test_report_contains_email_type(self, scrubber, sample_df):
        report = scrubber.scan_dataframe(sample_df)
        assert "EMAIL_ADDRESS" in report.entities_by_type

    def test_clean_df_no_pii(self, scrubber, clean_df):
        report = scrubber.scan_dataframe(clean_df)
        pii_types = {"EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "US_SSN"}
        detected_types = set(report.entities_by_type.keys())
        assert not pii_types.intersection(detected_types)

    def test_empty_df(self, scrubber):
        report = scrubber.scan_dataframe(pd.DataFrame())
        assert report.total_pii_count == 0

    def test_report_to_dict(self, scrubber, sample_df):
        report = scrubber.scan_dataframe(sample_df)
        d = report.to_dict()
        assert "total_pii_count" in d
        assert "entities_by_type" in d
        assert "columns_with_pii" in d


class TestMaskDataFrame:
    """Tests for PIIScrubber.mask_dataframe()."""

    def test_masks_emails(self, scrubber, sample_df):
        masked = scrubber.mask_dataframe(sample_df, MaskMode.REDACT)
        # Original emails should be gone
        for email in sample_df["email"]:
            assert email not in masked["email"].values

    def test_preserves_numeric_columns(self, scrubber, sample_df):
        masked = scrubber.mask_dataframe(sample_df, MaskMode.REDACT)
        # Numeric columns should not change
        pd.testing.assert_series_equal(
            masked["amount"], sample_df["amount"], check_names=True
        )

    def test_empty_df(self, scrubber):
        masked = scrubber.mask_dataframe(pd.DataFrame(), MaskMode.REDACT)
        assert masked.empty

    def test_output_same_shape(self, scrubber, sample_df):
        masked = scrubber.mask_dataframe(sample_df, MaskMode.REDACT)
        assert masked.shape == sample_df.shape


# ---------------------------------------------------------------------------
# Custom Recognizer Tests
# ---------------------------------------------------------------------------

class TestCustomRecognizers:
    """Tests for custom banking recognizers."""

    def test_iban_detection(self, scrubber):
        detections = scrubber.scan_text("IBAN: FI2112345600000785")
        entity_types = [d.entity_type for d in detections]
        assert "IBAN_CODE" in entity_types


# ---------------------------------------------------------------------------
# Utility Tests
# ---------------------------------------------------------------------------

class TestUtility:
    """Tests for utility methods."""

    def test_supported_entities(self, scrubber):
        entities = scrubber.get_supported_entities()
        assert "EMAIL_ADDRESS" in entities
        assert "PERSON" in entities
        assert "IBAN_CODE" in entities
