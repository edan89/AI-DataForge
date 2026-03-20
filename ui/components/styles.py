"""
Streamlit UI Styles — Premium Dark Theme

Provides consistent, modern styling across all pages
with glassmorphism effects, smooth gradients, and micro-animations.
"""

THEME_CSS = """
<style>
/* ============ ROOT VARIABLES ============ */
:root {
    --primary: #6C63FF;
    --primary-light: #8B83FF;
    --secondary: #00D4AA;
    --accent: #FF6B6B;
    --bg-dark: #0E1117;
    --bg-card: #1A1D23;
    --bg-card-hover: #22252B;
    --text-primary: #FAFAFA;
    --text-secondary: #D1D5DB;
    --border: #2D3139;
    --success: #00D4AA;
    --warning: #FFB84D;
    --error: #FF6B6B;
    --gradient-primary: linear-gradient(135deg, #6C63FF 0%, #00D4AA 100%);
    --gradient-accent: linear-gradient(135deg, #FF6B6B 0%, #FFB84D 100%);
    --shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
    --shadow-hover: 0 8px 32px rgba(108, 99, 255, 0.2);
}

/* ============ GLOBAL ============ */
.stApp {
    background-color: var(--bg-dark);
}

/* ============ HEADINGS ============ */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
}

/* ============ SIDEBAR ============ */
section[data-testid="stSidebar"] {
    background-color: #131620;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--primary-light);
}

/* ============ CARDS ============ */
div.stMetric {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    transition: all 0.3s ease;
}

div.stMetric:hover {
    border-color: var(--primary);
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
}

/* ============ BUTTONS ============ */
.stButton > button {
    background: var(--gradient-primary);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 2px 12px rgba(108, 99, 255, 0.3);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(108, 99, 255, 0.5);
}

/* ============ TEXT AREA / INPUT ============ */
.stTextArea textarea, .stTextInput input {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.2) !important;
}

/* ============ CODE BLOCK ============ */
.stCodeBlock {
    border-radius: 10px;
    border: 1px solid var(--border);
}

/* ============ TABS ============ */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 16px;
    background: var(--bg-card);
}

.stTabs [aria-selected="true"] {
    background: var(--gradient-primary) !important;
}

/* ============ DATA FRAME ============ */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
}

/* ============ DIVIDER ============ */
hr {
    border-color: var(--border);
    margin: 2rem 0;
}

/* ============ FILE UPLOADER ============ */
.stFileUploader > div {
    background: var(--bg-card);
    border: 2px dashed var(--border);
    border-radius: 12px;
    transition: border-color 0.3s ease;
}

.stFileUploader > div:hover {
    border-color: var(--primary);
}

/* ============ EXPANDER ============ */
.streamlit-expanderHeader {
    background: var(--bg-card);
    border-radius: 8px;
    border: 1px solid var(--border);
}

/* ============ SUCCESS/ERROR BOXES ============ */
.stSuccess {
    background: rgba(0, 212, 170, 0.1);
    border-left: 4px solid var(--success);
}

.stWarning {
    background: rgba(255, 184, 77, 0.1);
    border-left: 4px solid var(--warning);
}

.stError {
    background: rgba(255, 107, 107, 0.1);
    border-left: 4px solid var(--error);
}

/* ============ HEADER GRADIENT ============ */
.hero-title {
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0;
}

.hero-subtitle {
    color: var(--text-secondary);
    font-size: 1.1rem;
    margin-top: 0.5rem;
}

/* ============ MODULE CARDS ============ */
.module-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    transition: all 0.3s ease;
}

.module-card h3 {
    color: var(--text-primary) !important;
    margin-top: 12px !important;
    margin-bottom: 8px !important;
}

.module-card p {
    color: var(--text-secondary) !important;
    line-height: 1.6 !important;
}

.module-card:hover {
    border-color: var(--primary);
    box-shadow: var(--shadow-hover);
    transform: translateY(-3px);
}

/* ============ ANIMATIONS ============ */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-in {
    animation: fadeIn 0.5s ease-out;
}

/* ============ BADGES ============ */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge-security { background: rgba(255, 107, 107, 0.15); color: var(--accent); }
.badge-ai { background: rgba(108, 99, 255, 0.15); color: var(--primary-light); }
.badge-docs { background: rgba(0, 212, 170, 0.15); color: var(--secondary); }
.badge-devops { background: rgba(255, 184, 77, 0.15); color: var(--warning); }
</style>
"""

SIDEBAR_LOGO = """
<div style="text-align: center; padding: 1rem 0;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔧</div>
    <div style="
        background: linear-gradient(135deg, #6C63FF, #00D4AA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: 1px;
    ">AI-DataForge</div>
    <div style="color: #B0B3B8; font-size: 0.75rem; margin-top: 4px;">
        Secure • Automated • Intelligent
    </div>
</div>
"""
