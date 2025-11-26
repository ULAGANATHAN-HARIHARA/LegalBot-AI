import streamlit as st
import os, sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from modules.utils.db_utils import init_db, get_history

st.set_page_config(page_title="LegalBot History", page_icon="🕘", layout="centered")
init_db()

username = st.session_state.get("username", "guest")

st.markdown("<h2 style='margin-top:20px;'>🕘 Your Query History</h2>", unsafe_allow_html=True)

rows = get_history(username, limit=100)

search = st.text_input("Filter by keyword / IPC / date")

if not rows:
    st.info("No saved history yet.")
else:
    for i, (q, a, ts) in enumerate(rows):
        if search and search.lower() not in (q + a + str(ts)).lower():
            continue
        with st.expander(f"⏺ {ts} — {q[:60]}{'…' if len(q)>60 else ''}", expanded=False):
            st.markdown(f"**Question:**\n\n{q}")
            st.markdown("---")
            st.markdown(f"**Answer:**\n\n{a}")
