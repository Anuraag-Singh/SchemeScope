from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
DOCS = ROOT / "documents"
DATA = ROOT / "data"
CHROMA = DATA / "chroma"
MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
def setting(name, default=""):
    value = os.getenv(name, "")
    if value:
        return value
    try:
        import streamlit as st
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return value or default

LLM_MODEL = setting("LLM_MODEL", "gpt-4o-mini")
LLM_BASE_URL = setting("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
LLM_API_KEY = setting("LLM_API_KEY", "").strip()
TOP_K = int(os.getenv("TOP_K", "4"))
THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.35"))
MAX_SENTENCES = 3
SCHEMES = [
    "HDFC Large Cap Fund",
    "HDFC Flexi Cap Fund",
    "HDFC ELSS - Tax Saver Fund",
    "HDFC Small Cap Fund",
    "HDFC Balanced Advantage Fund",
]
