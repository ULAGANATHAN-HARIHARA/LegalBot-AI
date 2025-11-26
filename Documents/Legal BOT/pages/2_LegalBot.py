import streamlit as st
import os
import sys
from datetime import datetime
import time

# --- Import project modules ---
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from modules.ai.vector_db import load_retriever
from modules.ai.gemini_engine import ask_gemini
from modules.ai.recommender import recommend_section
from modules.utils.db_utils import save_history

# --- Page config ---
st.set_page_config(page_title="LegalBot Assistant", page_icon="⚖️", layout="wide")

# --- Remove default top bar / padding for premium look ---
st.markdown("""
<style>
/* Add some breathing room at the top */
div.block-container {
    padding-top: 40px !important;
}

/* Prevent header cut-off on small screens */
header[data-testid="stHeader"] {
    margin-top: 20px !important;
}
</style>
""", unsafe_allow_html=True)


# --- Premium Chat CSS ---
st.markdown("""
<style>
.app-title {
    font-size: 1.9rem;
    font-weight: 800;
    background: linear-gradient(90deg,#0ea5e9,#22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.app-sub {
    color: #9ca3af;
    font-size: 0.9rem;
}

/* Chat layout */
.chat-container {
    border-radius: 16px;
    padding: 12px 16px;
    background: radial-gradient(circle at top, #020617 0%, #020617 40%, #020617);
    border: 1px solid rgba(148,163,184,0.3);
    max-height: 65vh;
    overflow-y: auto;
}

.msg-row {
    display: flex;
    margin: 6px 0;
}

.msg-user {
    justify-content: flex-end;
}

.msg-bot {
    justify-content: flex-start;
}

.msg-bubble {
    max-width: 70%;
    padding: 10px 14px;
    border-radius: 18px;
    font-size: 0.95rem;
    line-height: 1.4;
    position: relative;
}

/* User bubble (right, cyan/green gradient) */
.msg-bubble-user {
    background: linear-gradient(120deg,#0ea5e9,#22c55e);
    color: #020617;
    border-bottom-right-radius: 4px;
}

/* Bot bubble (left, dark) */
.msg-bubble-bot {
    background: rgba(15,23,42,0.96);
    color: #e5e7eb;
    border: 1px solid rgba(148,163,184,0.5);
    border-bottom-left-radius: 4px;
}

.msg-time {
    font-size: 0.7rem;
    color: #9ca3af;
    margin-top: 4px;
    text-align: right;
}

/* Recommendation tags */
.rec-row {
    margin: 4px 0 2px 0;
    padding-left: 4px;
}

.rec-tag {
    display: inline-block;
    padding: 4px 10px;
    margin: 3px 4px 0 0;
    border-radius: 999px;
    background: rgba(8,47,73,0.95);
    border: 1px solid rgba(56,189,248,0.55);
    color: #e0f2fe;
    font-size: 0.75rem;
}

/* Input bar */
.input-container {
    margin-top: 10px;
    padding: 10px 12px;
    border-radius: 14px;
    background: rgba(15,23,42,0.98);
    border: 1px solid rgba(51,65,85,0.9);
}

/* Send button */
.send-btn > button {
    width: 100%;
    height: 2.8rem;
    border-radius: 999px;
    border: none;
    background: linear-gradient(120deg,#0ea5e9,#22c55e);
    color: #020617;
    font-weight: 700;
    font-size: 1.1rem;
}
.send-btn > button:hover {
    filter: brightness(1.05);
}

/* Mode toggle container */
.mode-box {
    padding: 6px 8px;
    border-radius: 999px;
    background: rgba(15,23,42,0.95);
    border: 1px solid rgba(51,65,85,0.9);
}
</style>
""", unsafe_allow_html=True)

# --- Cached retriever so it doesn't reload every time ---
@st.cache_resource(show_spinner=False)
def get_retriever():
    return load_retriever()

try:
    retriever = get_retriever()
except Exception as e:
    retriever = None
    st.error(f"Vector DB error: {e}")

# --- Session state for chat ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # each item: {role, content, time, recs?}

username = st.session_state.get("username", "Guest")

# --- Header / Nav ---
top_left, top_mid, top_right = st.columns([3, 3, 1.5])

with top_left:
    st.markdown("<div class='app-title'>⚖️ LegalBot</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='app-sub'>AI assistant for Indian Penal Code & criminal complaints — Logged in as <b>{username}</b></div>",
        unsafe_allow_html=True,
    )

with top_mid:
    # Mode toggle
    st.markdown("<div class='mode-box'>", unsafe_allow_html=True)
    mode = st.radio(
        "Mode",
        ["⚖ Complaint Mode", "📘 Section Info Mode"],
        horizontal=True,
        label_visibility="collapsed",
        key="mode_toggle",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with top_right:
    if st.button("🕘 View History", use_container_width=True):
        st.switch_page("pages/3_History.py")

st.markdown("---")

# Case law toggle
show_cases = st.checkbox("Include case law references (optional)", value=False)

# --- Main layout: chat column centered ---
left_pad, chat_col, right_pad = st.columns([0.3, 3, 0.3])

with chat_col:
    # Chat area
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    for msg in st.session_state["messages"]:
        role = msg["role"]
        content = msg["content"]
        ts = msg.get("time", "")
        recs = msg.get("recs", None)

        if role == "user":
            st.markdown("<div class='msg-row msg-user'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='msg-bubble msg-bubble-user'>{content}<div class='msg-time'>{ts}</div></div>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='msg-row msg-bot'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='msg-bubble msg-bubble-bot'>{content}<div class='msg-time'>{ts}</div></div>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # Show recommendation tags if present
            if recs:
                tags_html = "<div class='rec-row'>"
                for r in recs:
                    short = r.strip()
                    if len(short) > 60:
                        short = short[:60] + "…"
                    tags_html += f"<span class='rec-tag'>{short}</span>"
                tags_html += "</div>"
                st.markdown(tags_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close chat-container

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # =========================
    #   INPUT AREA BY MODE
    # =========================
    if mode.startswith("⚖"):  # Complaint Mode
        st.subheader("📝 Describe your complaint")

        complaint_text = st.text_area(
            "Describe what happened (in your own words)",
            key="complaint_text",
            placeholder="Example: Yesterday night, my neighbour broke into my house and stole my phone...",
            height=140,
        )

        c1, c2 = st.columns(2)
        with c1:
            date_of_incident = st.date_input("Date of incident")
            place = st.text_input("Place / Area", placeholder="City / Police station jurisdiction")
        with c2:
            time_of_incident = st.time_input("Time of incident")
            suspect = st.selectbox(
                "Who did this?",
                ["Known to me", "Unknown person", "Police/authority", "Other"],
            )

        evidence_files = st.file_uploader(
            "Upload any evidence (optional) – images / pdf",
            type=["png", "jpg", "jpeg", "pdf"],
            accept_multiple_files=True,
        )

        # Button row
        btn_col1, btn_col2 = st.columns([3, 1])
        with btn_col2:
            get_help = st.button("Get Legal Help 🚀", key="get_help_btn", use_container_width=True)

        if get_help:
            base_text = (complaint_text or "").strip()
            if not base_text:
                st.warning("Please describe your issue in the text area.")
            else:
                # Save evidence files locally
                evidence_paths = []
                if evidence_files:
                    evidence_root = os.path.join(ROOT, "evidence_uploads", username)
                    os.makedirs(evidence_root, exist_ok=True)
                    for f in evidence_files:
                        ts = int(time.time())
                        safe_name = f"{ts}_{f.name}"
                        file_path = os.path.join(evidence_root, safe_name)
                        with open(file_path, "wb") as out:
                            out.write(f.getbuffer())
                        evidence_paths.append(file_path)

                # Build a detailed query text for logging + Gemini
                full_query = f"""
[COMPLAINT MODE]

Description:
{base_text}

Date: {date_of_incident}
Time: {time_of_incident}
Place: {place}
Suspect relation: {suspect}
Evidence files (paths): {", ".join(evidence_paths) if evidence_paths else "None"}
"""

                # Add user message to chat
                now_str = datetime.now().strftime("%H:%M")
                st.session_state["messages"].append(
                    {"role": "user", "content": base_text, "time": now_str}
                )

                # Build legal context using complaint text
                context = ""
                if retriever:
                    with st.spinner("Retrieving relevant IPC sections for your complaint..."):
                        try:
                            docs = retriever.invoke(base_text)
                            context = "\n".join([d.page_content for d in docs])
                        except Exception as e:
                            st.error(f"Retriever error: {e}")

                # Build Gemini prompt
                case_clause = ""
                if show_cases:
                    case_clause = """
Also mention 1–3 relevant Indian case laws (case name + year), only if clearly connected.
"""

                prompt = f"""
You are an Indian criminal law assistant.
The user has described a real-world complaint.

First, identify possible offences and map to relevant IPC sections.

Then respond in the following structure (short and clear):

1. Offence Classification
   - List each possible offence in plain English.
   - Along with IPC section numbers (e.g., 378 – Theft).

2. Recommended Action Steps
   - Whether FIR is needed or simple complaint.
   - Where to go (police station / cyber cell / magistrate).
   - Any urgent safety measures.

3. Punishments & Nature of Offences
   - For each key IPC section: max punishment.
   - Mention if cognizable / non-cognizable, bailable / non-bailable, and which court usually tries it.

4. Important Notes
   - Any caution, limitations, or practical tips.

Complaint details:
{full_query}

Legal context from IPC book:
{context}
{case_clause}
Answer in concise bullet points, easy for a normal person to understand.
"""

                with st.spinner("LegalBot is analyzing your complaint..."):
                    answer = ask_gemini(prompt)

                # Recommendations
                recs = []
                try:
                    recs = recommend_section(base_text, retriever)
                except Exception:
                    recs = []

                now_str = datetime.now().strftime("%H:%M")
                st.session_state["messages"].append(
                    {
                        "role": "bot",
                        "content": answer,
                        "time": now_str,
                        "recs": recs,
                    }
                )

                # Save to DB (store full complaint with structured info)
                try:
                    save_history(username, full_query, answer)
                except Exception as e:
                    st.error(f"History save error: {e}")

                st.rerun()

    else:
        # =======================
        # SECTION INFO MODE
        # =======================
        st.subheader("📘 Ask about a law / IPC section")

        col_q, col_btn = st.columns([6, 1])
        with col_q:
            section_query = st.text_input(
                "Ask your legal question",
                key="section_query",
                placeholder="Example: Explain IPC 420. What is the punishment?",
            )
        with col_btn:
            ask_btn = st.button("➤", key="section_send", use_container_width=True)

        if ask_btn:
            q = (section_query or "").strip()
            if not q:
                st.warning("Type a question about a law or IPC section.")
            else:
                now_str = datetime.now().strftime("%H:%M")
                # Show user message
                st.session_state["messages"].append(
                    {"role": "user", "content": q, "time": now_str}
                )

                context = ""
                if retriever:
                    with st.spinner("Fetching relevant IPC sections..."):
                        try:
                            docs = retriever.invoke(q)
                            context = "\n".join([d.page_content for d in docs])
                        except Exception as e:
                            st.error(f"Retriever error: {e}")

                case_clause = ""
                if show_cases:
                    case_clause = """
Include 1–3 key Indian case laws that interpret this section.
"""

                prompt = f"""
You are an Indian Penal Code legal explainer.
The user is asking about law/sections, not a complaint description.

Please respond in this structure:

1. Plain English Explanation
   - What this section covers, in simple language.

2. Key Ingredients
   - Bullet list of legal ingredients.

3. Punishment
   - Maximum punishment, and any variations.

4. Nature of the Offence
   - Cognizable / non-cognizable.
   - Bailable / non-bailable.
   - Triable by which court.

5. Practical Example
   - One short practical example scenario.

Question:
{q}

Legal context from IPC book:
{context}
{case_clause}
Keep it concise but informative.
"""

                with st.spinner("LegalBot is preparing a legal explanation..."):
                    answer = ask_gemini(prompt)

                recs = []
                try:
                    recs = recommend_section(q, retriever)
                except Exception:
                    recs = []

                now_str = datetime.now().strftime("%H:%M")
                st.session_state["messages"].append(
                    {"role": "bot", "content": answer, "time": now_str, "recs": recs}
                )

                try:
                    save_history(username, q, answer)
                except Exception as e:
                    st.error(f"History save error: {e}")

                st.rerun()
