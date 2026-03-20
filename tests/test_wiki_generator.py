"""
Unit tests for Module 3: Data-Wiki Generator.

Tests DataFrame profiling and Markdown output generation.
LLM-dependent features are mocked.
"""

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd

from agents.wiki_generator import WikiGenerator, DataWiki


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_df():
    """Sample DataFrame for testing."""
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "amount": [100.5, 200.0, None, 400.25, 50.0],
        "category": ["A", "B", "A", "C", "B"],
        "date": ["2024-01-01", "2024-02-01", "2024-03-01", "2024-04-01", "2024-05-01"],
    })


@pytest.fixture
def generator():
    """Create WikiGenerator in offline mode (no LLM)."""
    return WikiGenerator(use_llm=False)


# ---------------------------------------------------------------------------
# Column Profiling Tests
# ---------------------------------------------------------------------------

class TestColumnProfiling:
    """Tests for column statistics generation."""

    def test_basic_profile(self, generator, sample_df):
        wiki = generator.generate(sample_df, dataset_name="Test")
        assert wiki.row_count == 5
        assert wiki.col_count == 5
        assert len(wiki.columns) == 5

    def test_numeric_stats(self, generator, sample_df):
        wiki = generator.generate(sample_df, dataset_name="Test")
        amount_col = next(c for c in wiki.columns if c.name == "amount")
        assert amount_col.mean is not None
        assert amount_col.std is not None
        assert amount_col.min_val is not None
        assert amount_col.max_val is not None

    def test_null_detection(self, generator, sample_df):
        wiki = generator.generate(sample_df, dataset_name="Test")
        amount_col = next(c for c in wiki.columns if c.name == "amount")
        assert amount_col.null_count == 1
        assert amount_col.null_rate == pytest.approx(0.2, abs=0.01)

    def test_unique_count(self, generator, sample_df):
        wiki = generator.generate(sample_df, dataset_name="Test")
        cat_col = next(c for c in wiki.columns if c.name == "category")
        assert cat_col.unique_count == 3  # A, B, C

    def test_sample_values(self, generator, sample_df):
        wiki = generator.generate(sample_df, dataset_name="Test")
        name_col = next(c for c in wiki.columns if c.name == "name")
        assert len(name_col.sample_values) > 0

    def test_empty_dataframe(self, generator):
        wiki = generator.generate(pd.DataFrame(), dataset_name="Empty")
        assert wiki.row_count == 0
        assert wiki.col_count == 0


# ---------------------------------------------------------------------------
# Markdown Output Tests
# ---------------------------------------------------------------------------

class TestMarkdownOutput:
    """Tests for Markdown generation."""

    def test_markdown_contains_title(self, generator, sample_df):
        wiki = generator.generate(sample_df, dataset_name="Insurance Claims")
        md = wiki.to_markdown()
        assert "Insurance Claims" in md

    def test_markdown_contains_columns(self, generator, sample_df):
        wiki = generator.generate(sample_df, dataset_name="Test")
        md = wiki.to_markdown()
        for col in sample_df.columns:
            assert col in md

    def test_markdown_contains_stats(self, generator, sample_df):
        wiki = generator.generate(sample_df, dataset_name="Test")
        md = wiki.to_markdown()
        assert "Numeric Column Statistics" in md
        assert "Mean" in md

    def test_markdown_contains_overview(self, generator, sample_df):
        wiki = generator.generate(sample_df, dataset_name="Test")
        md = wiki.to_markdown()
        assert "5" in md  # row count
        assert "Overview" in md

    def test_markdown_sample_values_section(self, generator, sample_df):
        wiki = generator.generate(sample_df, dataset_name="Test")
        md = wiki.to_markdown()
        assert "Sample Values" in md


# ---------------------------------------------------------------------------
# DataWiki Dataclass Tests
# ---------------------------------------------------------------------------

class TestDataWiki:
    """Tests for the DataWiki dataclass."""

    def test_default_values(self):
        wiki = DataWiki()
        assert wiki.dataset_name == "Untitled Dataset"
        assert wiki.row_count == 0
        assert wiki.columns == []

    def test_to_markdown_empty(self):
        wiki = DataWiki(dataset_name="Empty", generated_at="2024-01-01")
        md = wiki.to_markdown()
        assert "Empty" in md
        assert "2024-01-01" in md


# ---------------------------------------------------------------------------
# LLM Integration Tests (Mocked)
# ---------------------------------------------------------------------------

class TestLLMIntegration:
    """Tests for LLM-powered features with mocked responses."""

    @patch("agents.wiki_generator.ChatGroq")
    def test_descriptions_generated(self, mock_groq_class):
        """Test that LLM generates column descriptions."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = '{"id": "Unique row identifier.", "name": "Customer name."}'
        mock_llm.invoke.return_value = mock_response
        mock_groq_class.return_value = mock_llm

        gen = WikiGenerator(api_key="test-key", use_llm=True)
        df = pd.DataFrame({"id": [1, 2], "name": ["A", "B"]})
        wiki = gen.generate(df, dataset_name="Test")

        id_col = next(c for c in wiki.columns if c.name == "id")
        assert id_col.description == "Unique row identifier."
