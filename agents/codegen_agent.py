"""
Module 2: PySpark Code-Gen Agent

A LangChain agent that takes a natural language prompt and generates
valid, optimized PySpark scripts. Uses Groq API (Llama 3) for inference.

Knowledge Proved: Agent-based AI solutions, PySpark, and LLM orchestration.
"""

import os
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from agents.prompts.codegen_prompts import (
    CODEGEN_CONTEXT_TEMPLATE,
    CODEGEN_SYSTEM_PROMPT,
    CODEGEN_USER_TEMPLATE,
)
from core.validators import ValidationResult, validate_python_syntax


@dataclass
class GeneratedCode:
    """Result of code generation."""
    code: str = ""
    validation: ValidationResult = field(default_factory=ValidationResult)
    prompt_used: str = ""
    model: str = ""

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "validation": self.validation.to_dict(),
            "prompt_used": self.prompt_used,
            "model": self.model,
        }


class PySparkCodeGenAgent:
    """
    LangChain-powered agent that generates PySpark ETL scripts
    from natural language prompts.

    Uses Groq API with Llama 3 models for fast, free inference.

    Example:
        agent = PySparkCodeGenAgent(api_key=os.getenv("GROQ_API_KEY"))
        code_result = agent.generate("Clean this insurance data and calculate monthly claim averages")
        print(code_result.code)
    """

    DEFAULT_MODEL = "llama-3.3-70b-versatile"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ):
        """
        Initialize the Code-Gen Agent.

        Args:
            api_key: Groq API key. Falls back to GROQ_API_KEY env var.
            model: LLM model name. Defaults to Llama 3.1 70B.
            temperature: Generation temperature (lower = more deterministic).
            max_tokens: Maximum tokens in the response.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.model = model or self.DEFAULT_MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens

        if not self.api_key:
            raise ValueError(
                "Groq API key is required. Set GROQ_API_KEY env var or pass api_key parameter."
            )

        self.llm = ChatGroq(
            api_key=self.api_key,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

    def generate(
        self,
        prompt: str,
        df: Optional[pd.DataFrame] = None,
        max_retries: int = 1,
    ) -> GeneratedCode:
        """
        Generate a PySpark ETL script from a natural language prompt.

        Args:
            prompt: Natural language description of the ETL task.
            df: Optional DataFrame to provide schema context.
            max_retries: Number of retry attempts if validation fails.

        Returns:
            GeneratedCode with the script and validation results.
        """
        result = GeneratedCode(model=self.model, prompt_used=prompt)

        # Build context from DataFrame if provided
        context_section = ""
        if df is not None:
            context_section = CODEGEN_CONTEXT_TEMPLATE.format(
                columns=list(df.columns),
                dtypes=dict(df.dtypes.astype(str)),
                sample=df.head(3).to_string(index=False),
            )

        # Build the user message
        user_message = CODEGEN_USER_TEMPLATE.format(
            prompt=prompt,
            context_section=context_section,
        )

        # Generate code
        messages = [
            SystemMessage(content=CODEGEN_SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]

        try:
            response = self.llm.invoke(messages)
            code = self._clean_code(response.content)
            result.code = code

            # Validate
            result.validation = validate_python_syntax(code)

            # Retry if validation fails
            if not result.validation.syntax_valid and max_retries > 0:
                result = self._retry_generation(prompt, code, result, max_retries)

        except Exception as e:
            result.validation.errors.append(f"Generation failed: {str(e)}")

        return result

    def _retry_generation(
        self,
        original_prompt: str,
        bad_code: str,
        result: GeneratedCode,
        retries_left: int,
    ) -> GeneratedCode:
        """
        Retry code generation with error feedback.

        Args:
            original_prompt: The original user prompt.
            bad_code: The code that failed validation.
            result: The current GeneratedCode result.
            retries_left: Number of retries remaining.

        Returns:
            Updated GeneratedCode with retried output.
        """
        fix_prompt = (
            f"The following PySpark code has syntax errors. Fix them and return ONLY valid code:\n\n"
            f"Original task: {original_prompt}\n\n"
            f"Code with errors:\n{bad_code}\n\n"
            f"Errors found: {result.validation.errors}\n\n"
            f"Return ONLY the corrected Python code."
        )

        messages = [
            SystemMessage(content=CODEGEN_SYSTEM_PROMPT),
            HumanMessage(content=fix_prompt),
        ]

        try:
            response = self.llm.invoke(messages)
            code = self._clean_code(response.content)
            result.code = code
            result.validation = validate_python_syntax(code)
        except Exception as e:
            result.validation.errors.append(f"Retry failed: {str(e)}")

        return result

    def _clean_code(self, raw: str) -> str:
        """Strip markdown fences and extra whitespace from LLM output."""
        code = raw.strip()
        # Remove markdown code fences
        if code.startswith("```python"):
            code = code[len("```python"):]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        return code.strip()
