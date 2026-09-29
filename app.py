import csv
import re
from html import escape
from pathlib import Path

import streamlit as st
from schemescope.pipeline import Pipeline
from schemescope.config import THRESHOLD

st.set_page_config(page_title="SchemeScope | Facts-only MF FAQ", page_icon="◈", layout="wide")

@st.cache_resource(show_spinner=False)
def get_pipeline():
    return Pipeline()

@st.cache_data(show_spinner=False)
def get_source_registry():
    path = Path(__file__).parent / "deliverables" / "SOURCES.csv"
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

st.markdown("""
<style>
:root {
  --bg:#090b10; --panel:#11151d; --panel2:#151a24; --line:#252c38;
  --text:#f4f7fb; --muted:#9ba6b5; --accent:#7c9cff; --accent2:#a98cff;
}
.stApp { background: radial-gradient(circle at 75% 0%, #17203a 0%, #090b10 38%); color:var(--text); }
.block-container{max-width:1120px;padding-top:2rem;padding-bottom:4rem}
section[data-testid="stSidebar"]{background:#0c0f15;border-right:1px solid var(--line)}
section[data-testid="stSidebar"] *{color:#dfe5ee}
.hero{padding:2.2rem 2.2rem;border:1px solid var(--line);border-radius:26px;background:linear-gradient(135deg,rgba(24,31,48,.96),rgba(14,17,24,.94));box-shadow:0 20px 60px rgba(0,0,0,.24);}
.kicker{font-size:.72rem;font-weight:800;letter-spacing:.16em;color:#9db3ff;text-transform:uppercase}
.hero h1{font-size:2.8rem;line-height:1.05;letter-spacing:-.045em;margin:.45rem 0 .65rem;color:#fff}
.hero p{color:#aeb8c7;font-size:1rem;max-width:790px;line-height:1.65;margin:0}
.card{border:1px solid var(--line);border-radius:18px;padding:1rem 1.1rem;background:rgba(17,21,29,.9);height:100%;transition:.2s ease;}
.card b{display:block;margin-bottom:.4rem;color:#dce5ff}.muted{color:#9da8b8;font-size:.88rem;line-height:1.45}
.answer{border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:16px;padding:1.1rem 1.2rem;margin:.8rem 0;background:#11151d;color:#edf2f8;line-height:1.6}
.refusal{border-left-color:#d9a441;background:#17140d}
.source{border:1px solid var(--line);border-radius:14px;padding:.9rem 1rem;margin-top:.7rem;background:#0f131a;color:#dfe5ee}
.small{font-size:.78rem;color:#8f9aaa}
.section-label{font-size:.75rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#7f8ba0;margin:1.4rem 0 .6rem}
.status{display:inline-flex;align-items:center;gap:.45rem;border:1px solid #263c35;background:#0d1916;color:#a9e6cb;border-radius:999px;padding:.35rem .65rem;font-size:.76rem;font-weight:700;margin-bottom:.65rem}
.status-dot{width:7px;height:7px;border-radius:50%;background:#56d6a1;box-shadow:0 0 10px rgba(86,214,161,.45)}
.evidence{display:flex;justify-content:space-between;align-items:center;gap:1rem;border:1px solid #263c35;background:#0d1715;border-radius:12px;padding:.7rem .85rem;margin-top:.7rem;color:#b7dccc;font-size:.8rem}
.registry{border:1px solid var(--line);border-radius:18px;padding:1rem 1.1rem;background:rgba(17,21,29,.72)}
.refusal-card{border:1px solid #3a3120;border-radius:16px;padding:1rem;background:linear-gradient(145deg,#17140e,#11151d);height:100%}
.refusal-card .tag{font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:#d9a441;font-weight:800}
.refusal-card b{display:block;color:#f3eee3;margin:.45rem 0}
.followup-title{font-size:.76rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#7f8ba0;margin:1rem 0 .55rem}
div[data-testid="stTextInput"] input{background:#11151d!important;color:#f5f7fb!important;border:1px solid #303846!important;border-radius:14px!important;padding:.8rem 1rem!important}
div[data-testid="stTextInput"] input:focus{border-color:#718fff!important;box-shadow:0 0 0 1px #718fff!important}
div[data-testid="stButton"] button{border:1px solid #303846;background:#11151d;color:#dfe6f2;border-radius:14px;min-height:46px;text-align:left;transition:.18s ease}
div[data-testid="stButton"] button:hover{border-color:#718fff;background:#171d2a;color:#fff}
div[data-testid="stButton"] button[kind="primary"], div[data-testid="stFormSubmitButton"] button{background:linear-gradient(135deg,#6f8fff,#8b73e6)!important;border:1px solid #8fa7ff!important;color:#fff!important;font-weight:700;box-shadow:0 6px 18px rgba(111,143,255,.20)}
div[data-testid="stFormSubmitButton"] button:hover{background:linear-gradient(135deg,#809cff,#9a83f0)!important;border-color:#b4c2ff!important;color:#fff!important}
div[data-testid="stForm"]{position:sticky;bottom:1rem;z-index:100;background:rgba(9,11,16,.94);border:1px solid #303846;border-radius:18px;padding:.8rem .9rem .9rem;box-shadow:0 16px 40px rgba(0,0,0,.42);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}
div[data-testid="stForm"] label{display:none}
.stAlert{background:#11151d!important;border:1px solid #303846!important;color:#dfe5ee!important}
[data-testid="stChatMessage"]{background:transparent}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state: st.session_state.history=[]
if "question_value" not in st.session_state: st.session_state.question_value=""

registry = get_source_registry()
scheme_names = ["HDFC Large Cap", "HDFC Flexi Cap", "HDFC ELSS Tax Saver", "HDFC Small Cap", "HDFC Balanced Advantage"]

with st.sidebar:
    st.markdown("## ◈ SchemeScope")
    st.caption("INDMoney context · facts-only mutual-fund FAQ")
    st.divider()
    if st.button("＋ New conversation", key="sidebar_new_conversation", use_container_width=True, type="primary"):
        st.session_state.history=[]
        st.session_state.question_value=""
        st.rerun()
    st.markdown("**Supported schemes**")
    for x in scheme_names:
        st.write("•", x)
    st.divider()
    st.markdown("**Knowledge base**")
    st.markdown(f'<div class="registry"><b>5 schemes · {len(registry) or 16} official sources</b><br><span class="small">HDFC Mutual Fund public pages · bounded corpus</span></div>', unsafe_allow_html=True)
    with st.expander("View source registry"):
        if registry:
            for row in registry:
                st.markdown(f'**{escape(row.get("scheme", "HDFC Mutual Fund"))}**  \n<span class="small">{escape(row.get("source_type", "Official source"))}</span>  \n{escape(row.get("url", ""))}', unsafe_allow_html=True)
        else:
            st.caption("16 official HDFC Mutual Fund sources are included in the submission corpus.")
    st.divider()
    st.markdown("**Trust model**")
    st.caption("Official HDFC sources → local retrieval → evidence gate → grounded answer. No recommendations or return comparisons.")

hero_col, action_col = st.columns([5, 1], gap="medium")
with hero_col:
    st.markdown('<div class="hero"><div class="kicker">Facts · Sources · No advice</div><h1>Mutual fund facts you can trace.</h1><p>SchemeScope answers factual questions about five HDFC Mutual Fund schemes using a constrained retrieval pipeline. Every grounded answer carries one source link; unsupported questions are refused.</p></div>', unsafe_allow_html=True)
with action_col:
    st.markdown('<div style="height:1.95rem"></div>', unsafe_allow_html=True)
    if st.button("＋ New conversation", key="top_new_conversation", use_container_width=True):
        st.session_state.history=[]
        st.session_state.question_value=""
        st.rerun()

st.markdown('<div class="section-label">Try a question</div>', unsafe_allow_html=True)
examples=[
    "What is the expense ratio of HDFC Large Cap Fund?",
    "What is the lock-in period for HDFC ELSS Tax Saver Fund?",
    "What is the exit load of HDFC Balanced Advantage Fund?",
]
cols=st.columns(3)
for i,(c,q) in enumerate(zip(cols,examples)):
    with c:
        if st.button(q, key="example_"+str(i), use_container_width=True):
            st.session_state.question_value=q
            st.rerun()

st.info("Facts-only. No investment advice. Do not enter PAN, Aadhaar, OTP, account numbers, phone numbers or email addresses.")

def render_turn(turn, idx):
    q, r = turn["q"], turn["r"]
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        cls="answer refusal" if r["refused"] else "answer"
        if r["refused"]:
            st.markdown('<div class="status" style="color:#e9c887;background:#1b160b;border-color:#4a3b1d"><span class="status-dot" style="background:#d9a441;box-shadow:none"></span>Evidence unavailable or question outside supported scope</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status"><span class="status-dot"></span>Source-backed answer</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{cls}">{escape(r["text"])}</div>',unsafe_allow_html=True)
        if not r["refused"]:
            score = r.get("score")
            if score is not None:
                label = "Strong evidence match" if score >= max(THRESHOLD, 0.80) else "Evidence threshold passed"
                st.markdown(f'<div class="evidence"><span>Evidence match</span><b>{label}</b></div>', unsafe_allow_html=True)
        if r.get("source"):
            st.markdown(f'<div class="source"><b>Source</b><br>{escape(r["scheme"])} · {escape(r["section"])}<br><span class="small">Last updated from sources: {escape(r["updated"])}</span><br><a href="{escape(r["source"])}" target="_blank">Open source ↗</a></div>',unsafe_allow_html=True)

        if not r["refused"] and r.get("scheme"):
            st.markdown('<div class="followup-title">Continue exploring</div>', unsafe_allow_html=True)
            followups = [
                f"What is the expense ratio of {r['scheme']}?",
                f"What is the exit load of {r['scheme']}?",
                f"What is the riskometer of {r['scheme']}?",
            ]
            fcols=st.columns(3)
            for j,(fc,fq) in enumerate(zip(fcols,followups)):
                with fc:
                    if st.button(fq, key=f"followup_{idx}_{j}", use_container_width=True):
                        st.session_state.question_value=fq
                        st.rerun()

for idx, turn in enumerate(st.session_state.history):
    render_turn(turn, idx)

# The composer stays sticky at the bottom so users can ask follow-up questions
# without scrolling back to the top of the conversation.
with st.form("question_form", clear_on_submit=False):
    question=st.text_input("Question", value=st.session_state.question_value, placeholder="Ask a factual scheme question…", label_visibility="collapsed")
    submitted=st.form_submit_button("Ask SchemeScope  →", use_container_width=True)

if submitted and question.strip():
    st.session_state.question_value=question
    p=get_pipeline()
    with st.spinner("Checking the verified corpus…"):
        result=p.ask(question)
    st.session_state.history.append({"q":question,"r":result})
    st.rerun()
