"""
Prompt templates for the Data-Wiki Generator.

Templates that guide the LLM to produce professional,
human-readable column descriptions for data dictionaries.
"""

WIKI_SYSTEM_PROMPT = """You are a Technical Data Analyst creating professional data documentation.
Your job is to write clear, concise column descriptions for a data dictionary.

## Rules
1. Each description should be 1-2 sentences maximum
2. Describe what the column represents in business terms
3. Mention the data format when relevant (e.g., "ISO 8601 date", "2-letter country code")
4. Use professional, banking-friendly language
5. Do NOT include sample values in the description
"""

WIKI_COLUMN_PROMPT = """Generate professional descriptions for these dataset columns.

Dataset name: {dataset_name}
Columns and their statistics:
{column_info}

Return a JSON object where keys are column names and values are 1-2 sentence descriptions.
Example: {{"customer_id": "Unique identifier for each customer in the system.", "amount": "Transaction amount in the local currency."}}

Return ONLY the JSON, no markdown or explanation.
"""

WIKI_SUMMARY_PROMPT = """Write a brief 2-3 sentence summary of this dataset based on the following information:

Dataset: {dataset_name}
Number of rows: {row_count}
Number of columns: {col_count}
Column names: {columns}
Sample data types: {dtypes}

Return ONLY the summary paragraph, no markdown or explanation.
"""
