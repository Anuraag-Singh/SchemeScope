import re, requests
from .config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, MAX_SENTENCES

FIELD_HINTS = {
    "expense": "Expense ratio", "ter": "Expense ratio", "exit load": "Exit load", "exit": "Exit load",
    "minimum": "Minimum", "sip": "Minimum SIP", "lock-in": "Lock-in period", "lock in": "Lock-in period",
    "riskometer": "Riskometer", "risk": "Riskometer", "benchmark": "Benchmark", "objective": "Objective"
}

def choose_evidence(question, hits):
    q=question.lower()
    for needle, section in FIELD_HINTS.items():
        if needle in q:
            for h in hits:
                if section.lower() in h.chunk.section.lower():
                    return h
    return hits[0]

def fallback(question, hit):
    text=hit.chunk.text.strip()
    sentences=re.split(r"(?<=[.!?])\s+", text)
    return " ".join(sentences[:MAX_SENTENCES])

def llm(question, hits):
    evidence="\n\n".join(f"[{i+1}] {h.chunk.scheme} | {h.chunk.section}\n{h.chunk.text}" for i,h in enumerate(hits))
    prompt=("Answer only from the supplied evidence. Answer the user's factual mutual-fund question in at most 3 sentences. "
            "Do not give advice, rankings, return comparisons, or facts absent from evidence. Do not include URLs. "
            "If evidence is insufficient, say you cannot verify the fact from the supplied sources.\n\nQUESTION: "+question+"\n\nEVIDENCE:\n"+evidence)
    r=requests.post(LLM_BASE_URL+"/chat/completions",headers={"Authorization":f"Bearer {LLM_API_KEY}","Content-Type":"application/json"},json={"model":LLM_MODEL,"messages":[{"role":"system","content":"You are a facts-only mutual-fund FAQ assistant."},{"role":"user","content":prompt}],"temperature":0},timeout=30)
    r.raise_for_status(); return r.json()["choices"][0]["message"]["content"].strip()

def generate(question,hits):
    chosen=choose_evidence(question,hits)
    if LLM_API_KEY:
        try: text=llm(question,hits)
        except Exception: text=fallback(question,chosen)
    else: text=fallback(question,chosen)
    parts=re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(parts[:MAX_SENTENCES]), chosen
