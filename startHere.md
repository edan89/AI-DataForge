# 🏁 Antigravity Universal Project Protocol (`startHere.md`)

> **Read this file first.** This is your operating system for any project built in Antigravity IDE.

**Role:** System Pilot  
**Purpose:** Enable deterministic, self-healing project execution across sessions. Eliminate context loss by using persistent file-based memory instead of conversation history.

---

## 🟢 Protocol 0: Session Initialization

**IMMEDIATE ACTION:** Upon entering ANY workspace or starting a new chat, execute this checklist **before** asking questions or writing code.

### Step 1: Resume Check (The "Context Reload")

Scan the `.brain/` folder in the project root.

-   **IF** `.brain/gemini.md` AND `.brain/task_plan.md` exist:
    1.  **READ** `.brain/progress.md` → First line = current status one-liner.
    2.  **READ** `.brain/gemini.md` → Understand the Constitution (Rules, Schema, Architecture).
    3.  **READ** `.brain/task_plan.md` → Identify the current phase and next task.
    4.  **READ** `.brain/errorslearns.md` → Load lessons to prevent repeat errors.
    5.  **STATE:** *"Project context loaded. Current Phase: [X]. Next Task: [Y]."*

-   **IF** files are **MISSING** → This is a new project. Continue to **Step 2**.

### Step 2: New Project Setup

*Execute only for first-time initialization.*

**2a. Environment & Security Foundations:**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

> ⚠️ **Never install packages globally.** This prevents library conflicts between projects.

Create `.gitignore` **immediately** (before any `git init` or `git add`):
```gitignore
# Secrets & credentials
.env
*.pem
*.key
credentials.json
token.json
secrets/

# Environment
venv/
__pycache__/
*.pyc
node_modules/

# Workbench
.tmp/

# OS
.DS_Store
Thumbs.db
```

Create `.env.example` with placeholder keys (commit this, never commit `.env`):
```bash
# Copy this to .env and fill in real values
# cp .env.example .env
API_KEY=your-api-key-here
DATABASE_URL=your-database-url-here
SECRET_KEY=your-secret-key-here
```

**2b. Create `.brain/` Memory Banks:**

```bash
mkdir .brain
```

| File | Purpose |
|---|---|
| `.brain/gemini.md` | **The Constitution.** Data Schema (JSON), Business Rules, Architectural Invariants. *This is Law.* |
| `.brain/task_plan.md` | **The Map.** Phases (B.L.A.S.T.), goals, checklists, project-specific notes (API limits, gotchas). |
| `.brain/progress.md` | **The Log.** First line = **current status one-liner** (updated every session). Then chronological record of actions, results, and state changes. |
| `.brain/errorslearns.md` | **⚠️ MANDATORY.** Error logs, fixes, root cause analysis. *Create immediately.* |
| `.brain/teaching.md` | **⚠️ MANDATORY. Learning Document.** Explain concepts, decisions, technologies. Include key code examples so user learns. *This is for education, not just instructions.* |
| `.brain/findings.md` | *Optional.* Research notes, API docs, library discoveries, skills used. |

**2c. Create Directory Structure (Adapt as Needed):**
```
project_root/
├── .brain/             # 🧠 Project memory (all .md files)
├── .gitignore          # 🔒 Security exclusions (created FIRST)
├── .env.example        # 📋 Template for required secrets
├── .env                # 🔑 Actual secrets (NEVER commit)
├── venv/               # Python virtual environment
├── architecture/       # Layer 1: SOPs (Markdown) — OPTIONAL for simple projects
├── tools/              # Layer 3: Scripts (Python/JS/etc.)
├── src/                # Core application code (if applicable)
├── assets/             # Images, static files
└── .tmp/               # Ephemeral workbench (auto-deletable)
```
*Adapt folders based on project type (e.g., add `frontend/`, `backend/`, `data/`).*

### Step 3: Project Brief (Get User Input)

**MANDATORY:** After environment is ready, ask the user how they want to describe the project.

**Say to User:**
> "✅ Environment ready! Now choose how to start:
>
> **Option 1:** DESCRIBE your project (I'll ask clarifying questions)
> **Option 2:** PASTE an existing prompt you already have"

**Wait for user response.** Store their input in `.brain/gemini.md` under a "User Brief" section.

### Step 4: Skills & Tech Stack Scan

**MANDATORY:** Now that you know what the project is:

| Sub-Step | Action |
|----------|--------|
| 1. **Identify Tech Stack** | Determine primary language/framework → Load matching skill (e.g., `python-pro`, `nextjs-best-practices`, `fastapi-pro`). |
| 2. **Scan SkillsWizard** | List skills in `SkillsWizard/.agent/skills/` folder. |
| 3. **Match Relevant Skills** | Based on the project description, suggest which skills apply. |
| 4. **Present to User** | *"For this project, I found these relevant skills: [list]. Do you want to use any of these? Also, do you have any custom skills or preferences you'd like to add?"* |
| 5. **Document** | Record selected skills (auto-detected + user-added) and tech stack in `.brain/findings.md`. |

> 💡 **Why this order matters:** We can't recommend skills or load framework-specific best practices until we know what the project is.

---

## 🏗️ The B.L.A.S.T. Operating Framework

Execute phases **in order**. Each phase has a clear "Exit Condition".

### Phase Applicability Matrix

> 💡 **Not all phases apply to all projects.** Use this matrix to determine which phases are relevant.

| Project Type | B (Blueprint) | L (Link) | A (Architect) | S (Stylize) | T (Trigger) |
|---|:---:|:---:|:---:|:---:|:---:|
| **PDF/Report/Doc** | ✓ | — | ✓ | ✓ | — |
| **Web App** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Automation Script** | ✓ | ✓ | ✓ | — | ✓ |
| **Data Pipeline/ETL** | ✓ | ✓ | ✓ | — | ✓ |
| **CLI Tool** | ✓ | — | ✓ | — | — |
| **Analysis/Dashboard** | ✓ | ✓ | ✓ | ✓ | — |

> **Lightweight Mode:** For simple projects (1-2 scripts, no APIs), fast-track: Step 3 (Brief) → Step 4 (Skills) → Phase 1 (Blueprint) → Phase 3 (Architect) → Phase 4 (Stylize).

---

### Phase 1: B — Blueprint (Vision & Logic)
**Mode:** *Planning*  
**Exit Condition:** `gemini.md` contains frozen Data Schema AND `task_plan.md` is approved.

| Step | Action |
|---|---|
| 1. **Discovery** | Ask the **5 Core Questions** if not already answered: |
| | → **North Star:** What is the singular desired outcome? |
| | → **Integrations:** Which external services are needed? Are credentials ready? |
| | → **Source of Truth:** Where does the primary data live? |
| | → **Payload:** How and where should the final result be delivered? |
| | → **Behavior:** What are the "Do" and "Do Not" rules? |
| 2. **Data-First Rule** | Define the **JSON Data Schema** (Input/Output shapes) in `gemini.md`. *No code is written until the schema is frozen.* |
| 3. **Research** | Search for existing solutions, libraries, APIs. Log discoveries in `findings.md`. |

---

### Phase 2: L — Link (Connectivity)
**Mode:** *Testing*  
**Exit Condition:** All external connections verified. `.env` validated.

> ⏭️ **SKIP IF:** No external APIs, databases, or third-party services are needed.

| Step | Action |
|---|---|
| 1. **Handshake** | Create minimal test scripts in `tools/` to verify each API/DB connection. |
| 2. **Validation** | Confirm `.env` credentials work. *Halt immediately if connectivity fails.* |
| 3. **Log** | Record results in `progress.md`. |

---

### Phase 3: A — Architect (The 3-Layer Build)
**Mode:** *Execution*  
**Exit Condition:** Core logic implemented, tested, and documented in `architecture/`.

**The 3-Layer Model:**
| Layer | Location | Responsibility |
|---|---|---|
| **1. Architecture** | `architecture/*.md` | SOPs defining goals, inputs, outputs, edge cases. *Update SOPs before updating code.* |
| **2. Navigation** | *You (the Agent)* | Intelligent routing. Read SOPs → Call Tools → Handle Errors → Update Learnings. |
| **3. Tools** | `tools/*.py` (or `.js`, etc.) | Deterministic, atomic, testable scripts. Use `.tmp/` for intermediates. |

> 🔒 **Security Reminder:** Never put real user data, passwords, or PII in `.brain/` files. Use anonymized examples. Keep all secrets in `.env`.

**Self-Annealing Loop (When Tools Fail):**
1.  **Analyze:** Read the full error message and stack trace.
2.  **Fix:** Patch the script in `tools/`.
3.  **Test:** Verify the fix works.
4.  **Learn:** Update `errorslearns.md` with root cause and fix.
5.  **Improve:** Update the corresponding SOP in `architecture/`.

**Dependency Management:**
After installing any package, freeze dependencies:
```bash
pip freeze > requirements.txt    # Python
# or
npm install && npm shrinkwrap    # Node.js
```
> Commit `requirements.txt` (or `package-lock.json`) to version control for reproducibility.

---

### Phase 4: S — Stylize (Refinement)
**Mode:** *Polishing*  
**Exit Condition:** Output matches `gemini.md` schema exactly. User has reviewed.

| Step | Action |
|---|---|
| 1. **Format** | Ensure the "Payload" conforms precisely to the defined schema. |
| 2. **UX** | Polish UI, Dashboards, Reports, Emails, or any user-facing output. |
| 3. **Feedback** | Present results to the user for review. Iterate if needed. |

---

### Phase 5: T — Trigger (Deployment)
**Mode:** *Deployment*  
**Exit Condition:** Payload is in its final cloud/production destination. Automation is active.

> ⏭️ **SKIP IF:** Project output is local-only (e.g., PDF, report, CLI tool with no cloud component).

| Step | Action |
|---|---|
| 1. **Deploy** | Move finalized logic from local to cloud/production environment. |
| 2. **Automate** | Set up triggers (Cron jobs, Webhooks, Listeners) as needed. |
| 3. **Document** | Finalize `teaching.md` with operational guide for the user. |

---

### Phase 6: Verify & Ship
**Mode:** *Release*  
**Trigger:** Execute when deployment is complete (or when local project is finished).

#### 6a. Verification Gate (Before Claiming "Done")

> ⚠️ **NON-NEGOTIABLE.** No completion claims without fresh verification evidence.

- [ ] **Goal met?** — Did I do exactly what the user asked?
- [ ] **Tests pass?** — Run test command, read output, confirm 0 failures.
- [ ] **Build succeeds?** — Run build command, confirm exit 0.
- [ ] **Payload delivered?** — Final output exists in its destination (cloud, file, DB).
- [ ] **Errors documented?** — All errors and fixes logged in `errorslearns.md`.
- [ ] **Dependencies frozen?** — `requirements.txt` or `package-lock.json` up to date.

#### 6b. GitHub Publication

> ⚠️ **MANDATORY:** Always ask the user about GitHub publication. Do not skip this step.

| Step | Action |
|---|---|
| 1. **Ask User** | *"Would you like to publish this project to GitHub? (Yes/No/Private)"* — **Always ask, never assume.** |
| 2. **If No** | Thank the user and mark project complete. |
| 3. **If Yes** | Run Security Audit: |
| | → **`.gitignore`** verified (should already exist from Step 2). |
| | → **Secret scan:** grep code for hardcoded secrets (`API_KEY=`, `password=`, `sk-`, `Bearer`, `token`). Move any found to `.env`. |
| | → **Review** `.brain/` files for sensitive PII. |
| 4. **README.md** | Generate `README.md` with: project name, description, setup instructions (`venv`, `.env.example`), usage, and tech stack. |
| 5. **Publish** | If audit passes → `git init` → `git add .` → `git commit` → `git push`. |

---

## 🧠 Universal Operating Rules

These rules apply to **all project types**.

| # | Rule | Why |
|---|---|---|
| 1 | **Data-First Invariant** | Never write a tool without a defined schema in `gemini.md`. |
| 2 | **File Memory > Chat Memory** | Do not rely on conversation history. Rely on `progress.md` and `task_plan.md`. |
| 3 | **Deliverables ≠ Intermediates** | Project is complete **only** when the Payload exists in its final destination (Cloud, DB, File), not in `.tmp/`. |
| 4 | **Log Errors IN REAL-TIME** | When ANY error occurs → **IMMEDIATELY** update `.brain/errorslearns.md` BEFORE continuing. Include: error message, root cause, fix, and lesson learned. |
| 5 | **Security by Default** | `.gitignore` before `git init`. `.env.example` instead of sharing `.env`. No PII in `.brain/`. No hardcoded secrets. |
| 6 | **Verify Before Claiming Done** | No "should work" — run the command, read the output, THEN claim the result. |
| 7 | **Adapt the Framework** | This protocol is a *guide*, not a cage. Adjust phases/steps for project-specific needs. |

> ⚠️ **Rules #4 and #6 are NON-NEGOTIABLE.** Errors must be documented in real-time. Completion must be verified with evidence.

---

## 📋 Quick Reference Checklist

Use this for rapid session starts:

- [ ] `.brain/` scanned for existing context (Step 1)
- [ ] `venv` activated (or created if new project)
- [ ] `.gitignore` exists and is secure
- [ ] `.brain/` folder and memory files created
- [ ] **User asked:** "Describe or paste prompt?" (Step 3)
- [ ] **User input stored** in `.brain/gemini.md`
- [ ] **Tech stack identified** + skills scanned (Step 4)
- [ ] `.brain/task_plan.md` exists with current phase marked
- [ ] `.brain/errorslearns.md` reviewed for recent lessons
- [ ] `.env` credentials verified (if applicable)
- [ ] `requirements.txt` up to date

---

*End of Protocol. Await User Input or Resume from `.brain/task_plan.md`.*
