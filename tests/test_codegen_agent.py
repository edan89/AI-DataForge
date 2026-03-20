"""
Unit tests for Module 2: PySpark Code-Gen Agent.

Uses mocked LLM responses to test without requiring a Groq API key.
"""

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd

from core.validators import validate_python_syntax, ValidationResult


# ---------------------------------------------------------------------------
# Code Validator Tests (no API needed)
# ---------------------------------------------------------------------------

class TestPythonSyntaxValidation:
    """Tests for the code validation module."""

    def test_valid_python(self):
        code = "x = 1\nprint(x)"
        result = validate_python_syntax(code)
        assert result.syntax_valid is True
        assert len(result.errors) == 0

    def test_invalid_python(self):
        code = "def foo(\n  return 1"
        result = validate_python_syntax(code)
        assert result.syntax_valid is False
        assert len(result.errors) > 0

    def test_valid_pyspark_code(self):
        code = '''
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("Test").getOrCreate()
df = spark.read.csv("data.csv", header=True)
result = df.filter(F.col("amount") > 0)
result.show()
spark.stop()
'''
        result = validate_python_syntax(code)
        assert result.syntax_valid is True
        assert result.has_pyspark_imports is True

    def test_no_pyspark_imports_warning(self):
        code = "import pandas as pd\ndf = pd.read_csv('test.csv')"
        result = validate_python_syntax(code)
        assert result.syntax_valid is True
        assert result.has_pyspark_imports is False
        assert len(result.warnings) > 0

    def test_empty_code(self):
        result = validate_python_syntax("")
        assert result.syntax_valid is False
        assert len(result.errors) > 0

    def test_strips_markdown_fences(self):
        code = '```python\nx = 1\nprint(x)\n```'
        result = validate_python_syntax(code)
        assert result.syntax_valid is True

    def test_is_valid_property(self):
        result = ValidationResult(syntax_valid=True)
        assert result.is_valid is True

    def test_to_dict(self):
        result = validate_python_syntax("x = 1")
        d = result.to_dict()
        assert "syntax_valid" in d
        assert "has_pyspark_imports" in d
        assert "errors" in d
        assert "warnings" in d


# ---------------------------------------------------------------------------
# Code-Gen Agent Tests (mocked LLM)
# ---------------------------------------------------------------------------

class TestCodeGenAgentMocked:
    """Tests for PySparkCodeGenAgent with mocked LLM."""

    @patch("agents.codegen_agent.ChatGroq")
    def test_generate_returns_code(self, mock_groq_class):
        """Test that generate() returns a GeneratedCode object."""
        # Mock the LLM response
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = '''from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("ETL").getOrCreate()
df = spark.read.csv("data.csv", header=True, inferSchema=True)
result = df.groupBy("category").agg(F.avg("amount").alias("avg_amount"))
result.show()
spark.stop()'''
        mock_llm.invoke.return_value = mock_response
        mock_groq_class.return_value = mock_llm

        from agents.codegen_agent import PySparkCodeGenAgent

        agent = PySparkCodeGenAgent(api_key="test-key")
        result = agent.generate("Calculate average amount by category")

        assert result.code != ""
        assert result.validation.syntax_valid is True
        assert result.validation.has_pyspark_imports is True

    @patch("agents.codegen_agent.ChatGroq")
    def test_generate_with_dataframe_context(self, mock_groq_class):
        """Test that DataFrame context is included in the prompt."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "from pyspark.sql import SparkSession\nprint('hello')"
        mock_llm.invoke.return_value = mock_response
        mock_groq_class.return_value = mock_llm

        from agents.codegen_agent import PySparkCodeGenAgent

        agent = PySparkCodeGenAgent(api_key="test-key")
        df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        result = agent.generate("Process this data", df=df)

        # Verify LLM was called with context
        call_args = mock_llm.invoke.call_args
        messages = call_args[0][0]
        user_msg = messages[1].content
        assert "col1" in user_msg
        assert "col2" in user_msg

    @patch("agents.codegen_agent.ChatGroq")
    def test_generate_handles_llm_error(self, mock_groq_class):
        """Test graceful handling of LLM errors."""
        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("API timeout")
        mock_groq_class.return_value = mock_llm

        from agents.codegen_agent import PySparkCodeGenAgent

        agent = PySparkCodeGenAgent(api_key="test-key")
        result = agent.generate("Some task")

        assert result.validation.syntax_valid is False
        assert any("Generation failed" in e for e in result.validation.errors)

    def test_no_api_key_raises(self):
        """Test that missing API key raises ValueError."""
        import os
        # Temporarily clear the env var
        original = os.environ.get("GROQ_API_KEY")
        os.environ.pop("GROQ_API_KEY", None)

        from agents.codegen_agent import PySparkCodeGenAgent
        with pytest.raises(ValueError, match="Groq API key is required"):
            PySparkCodeGenAgent(api_key="")

        # Restore
        if original:
            os.environ["GROQ_API_KEY"] = original
