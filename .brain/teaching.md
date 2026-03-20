# 📚 Teaching — Learning Document

> **MANDATORY.** Explain concepts, decisions, and technologies so the user learns, not just follows instructions.

---

Welcome to the internal workings of **AI-DataForge**! This document will break down exactly how the technologies in this project interact. Think of this as the "under-the-hood" guide.

## 0. The Big Picture: What are we actually building?

In real-world Enterprise Data Engineering (like at a bank), data teams spend countless hours doing three extremely tedious things:

1. **Compliance:** Checking if new datasets contain sensitive customer data (PII) before moving them into analytics databases.
2. **Exploration & Documentation:** Manually calculating statistics on raw data files and writing "Data Dictionaries" to explain what each column in a dataset means to business users.
3. **Boilerplate Coding:** Writing the exact same PySpark ETL (Extract, Transform, Load) scripts over and over to group, clean, and filter data.

**AI-DataForge automates all three processes.** 
We built a simulated "Internal Developer Tool." 

Here is the real-life workflow our tool creates:
- A Data Engineer receives a raw `.csv` file from a business partner and uploads it to our dashboard.
- **Module 1 (Security API)** instantly scans it, finds Social Security Numbers or Emails, and masks them so the data is legally safe to use.
- **Module 3 (Data Wiki API)** reads this safe data, calculates statistics (like how many null values exist), and uses an AI (Groq/Llama) to write a beautiful, human-readable Data Dictionary explaining the contents.
- **Module 2 (Code-Gen Agent)** takes that safe schema and plain English instructions (*"Filter by age > 30 and group by city"*), and forces the AI to write a perfect, syntax-checked PySpark script that the engineer can immediately deploy to Databricks.

We are taking the most boring, error-prone parts of Data Engineering and using AI Agents to do them for us—but safely, behind an enterprise wall of compliance checks.

---

## 1. How Microsoft Presidio Works (Module 1)

In the `core/pii_scrubber.py` file, we implemented **Microsoft Presidio**. Presidio is an enterprise-grade PII detection engine. But how does it actually *know* a string is a name versus a random word?

Presidio relies on three main components working together:

1. **The NLP Engine (Natural Language Processing):** Usually powered by `spaCy` or `Stanza`. It reads the text and identifies parts of speech. For instance, it uses Named Entity Recognition (NER) to tag "John Doe" as a `PERSON`.
2. **The Pattern Recognizers:** These are rule-based bots. Instead of AI, they use strict Regular Expressions (Regex). For example, finding `[0-9]{3}-[A-Z]{2}`.
3. **The Score System (Confidence):** This is the magic. If the NLP engine thinks something is a name, it gives it a score (e.g., `0.85`). If an email matches a Regex pattern exactly, it gives it a score of `1.0`. In `PIIScrubber`, we set `score_threshold=0.4`, meaning we only mask things the engine is at least 40% confident about.

**Learning Point:** By combining AI (NER) with hard rules (Regex), we get the best of both worlds. We even added our own custom rules! In `_build_iban_recognizer()`, we explicitly told Presidio the math and regex behind an IBAN number, so it doesn't have to guess.

---

## 2. Prompt Engineering and LangChain (Modules 2 & 3)

In `agents/codegen_agent.py` and `agents/wiki_generator.py`, we use **LangChain** and **Groq (Llama 3)**.

You might think an LLM agent is just a chatbot wrapper, but it's much more structured. Look at the `codegen_prompts.py` file. We use `ChatPromptTemplate` from LangChain.

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", CODEGEN_SYSTEM_PROMPT),
    ("human", "Instruction: {instruction}\n\nDataset Context: {df_context}")
])
```

**Why do this?**
- **System Prompt:** This is the agent's "Identity". We define strict rules: "You are an elite PySpark engineer. Do NOT output markdown. ONLY output code."
- **Variables (`{instruction}`, `{df_context}`):** LangChain automatically injects user input here. 
- **Context injection:** This is a core AI engineering concept. Instead of hoping the AI guesses what the data looks like, we use pandas to take a literal *sample* of the first 3 rows of the CSV (`df_context = df.head(3).to_markdown()`) and shove it into the prompt behind the scenes. The AI now actually "sees" the columns before writing PySpark code!

---

## 3. Abstract Syntax Trees (AST) for Defensive AI 

LLMs hallucinate. Even the best models will sometimes add random text like *"Here is your script:"* before the code, even if you explicitly told them not to. 

If we executed that output natively, it would instantly crash with a `SyntaxError`.

To solve this, we built a **Guardrail** in `core/validators.py`.
We use Python's built-in `ast` (Abstract Syntax Tree) module:

```python
import ast

def validate_python_code(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False
```

**How it works:**
Instead of trying to execute the code, `ast.parse()` reads the string and checks if it conforms to the strict grammatical rules of the Python language. If the LLM output includes conversational text, `ast.parse()` immediately raises a SyntaxError. 

If this happens, our LangChain agent is programmed to say, "Oops," and execute an automatic retry cycle, generating a fresh response until it passes the AST check.

---

## 4. Understanding Streamlit State Management (`st.session_state`)

Streamlit is incredible for quickly building UIs, but it has one massive quirk: **Every time you click a button or type in a box, Streamlit reruns the *entire* Python script from top to bottom.**

If you upload a CSV file, and then click a "Generate" button, Streamlit reruns the script. If you didn't save that CSV file somewhere, it gets wiped from memory instantly!

To solve this, we used `st.session_state` in `ui/pages/1_🔒_PII_Scanner.py` and the other pages:

```python
# Check if we already have the data saved in state
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

file = st.file_uploader(...)
if file:
    # Save the dataframe into the state so it survives the page reload!
    st.session_state.uploaded_data = pd.read_csv(file)
```

By heavily relying on `st.session_state`, we ensure that data, generated scripts, and chat histories persist smoothly as the user interacts with the app.

---

## 5. Clean Architecture (Separation of Concerns)

Notice how the project is organized into `core/`, `agents/`, `ui/`, and `tests/`.

This is called **Separation of Concerns**, and it is what separates beginner scripts from professional software engineering:
1. **`core/pii_scrubber.py`** knows *nothing* about Streamlit or buttons. It only takes strings and returns strings.
2. **`agents/codegen_agent.py`** knows *nothing* about how the user typed their prompt. It just takes text and returns PySpark code.
3. **`ui/app.py`** knows *nothing* about Microsoft Presidio or LangChain. It just draws buttons on a screen and calls the tools from the other folders.

Because they are separated, writing accurate Unit Tests (`tests/`) becomes incredibly easy. We don't have to launch a browser to test if the PII scrubber works; we just pass it a string in a Pytest function. This is how OP (Bank) expects modern data tooling to be built!
