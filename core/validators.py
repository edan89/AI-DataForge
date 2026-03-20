"""
Code validation helpers.

Provides syntax checking and PySpark import validation
for LLM-generated code (used by Module 2: Code-Gen Agent).
"""

import ast
import re
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of code validation."""
    syntax_valid: bool = False
    has_pyspark_imports: bool = False
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.syntax_valid

    def to_dict(self) -> dict:
        return {
            "syntax_valid": self.syntax_valid,
            "has_pyspark_imports": self.has_pyspark_imports,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def validate_python_syntax(code: str) -> ValidationResult:
    """
    Validate that a code string is syntactically correct Python.

    Args:
        code: Python source code string.

    Returns:
        ValidationResult with syntax check details.
    """
    result = ValidationResult()

    if not code or not code.strip():
        result.errors.append("Empty code string provided.")
        return result

    # Clean code: remove markdown fences if present
    code = _strip_markdown_fences(code)

    try:
        ast.parse(code)
        result.syntax_valid = True
    except SyntaxError as e:
        result.errors.append(f"SyntaxError at line {e.lineno}: {e.msg}")

    # Check for PySpark imports
    pyspark_patterns = [
        r"from\s+pyspark",
        r"import\s+pyspark",
        r"SparkSession",
        r"pyspark\.sql",
    ]
    for pattern in pyspark_patterns:
        if re.search(pattern, code):
            result.has_pyspark_imports = True
            break

    if result.syntax_valid and not result.has_pyspark_imports:
        result.warnings.append(
            "No PySpark imports detected. The generated code may not be a PySpark script."
        )

    return result


def _strip_markdown_fences(code: str) -> str:
    """Remove markdown code fences (```python ... ```) if present."""
    code = code.strip()
    if code.startswith("```"):
        # Remove opening fence
        first_newline = code.find("\n")
        if first_newline != -1:
            code = code[first_newline + 1:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()
