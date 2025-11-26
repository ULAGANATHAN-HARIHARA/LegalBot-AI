import streamlit as st
import os, sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from modules.utils.db_utils import init_db, register_user, login_user
# ---------------- REMOVE TOP BAR ----------------
st.markdown("""
<style>
section[data-testid="stHeader"] {
    background-color: transparent;
}
div.block-container {
    padding-top: 0px !important;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="LegalBot Login", page_icon="🔐", layout="centered")
init_db()

# 🔥 FAST REDIRECT IMMEDIATELY AFTER LOGIN
if st.session_state.get("go_to_legalbot", False):
    st.session_state["go_to_legalbot"] = False
    st.switch_page("pages/2_LegalBot.py")

# ---------------- UI CSS ----------------
st.markdown("""
<style>
.login-card {
    margin-top: 80px;
    padding: 32px 28px;
    border-radius: 18px;
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(148, 163, 184, 0.4);
    backdrop-filter: blur(14px);
    max-width: 420px;
    margin-left: auto;
    margin-right: auto;
}
.login-title {
    font-size: 1.9rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg,#0ea5e9,#22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.login-sub {
    text-align: center;
    color: #9ca3af;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='login-card'>", unsafe_allow_html=True)
st.markdown("<div class='login-title'>Sign in to LegalBot</div>", unsafe_allow_html=True)
st.markdown("<div class='login-sub'>Track your law queries and revisit past answers.</div>", unsafe_allow_html=True)

tabs = st.tabs(["🔐 Login", "🆕 Sign up"])

# --------------- LOGIN TAB ---------------
with tabs[0]:
    user = st.text_input("Username", key="login_user")
    pw = st.text_input("Password", type="password", key="login_pw")

    if st.button("Login", use_container_width=True):
        if login_user(user, pw):
            st.session_state["username"] = user
            st.session_state["go_to_legalbot"] = True
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# --------------- SIGNUP TAB ---------------
with tabs[1]:
    new_user = st.text_input("New username", key="reg_user")
    new_pw = st.text_input("New password", type="password", key="reg_pw")

    if st.button("Create account", use_container_width=True):
        if register_user(new_user, new_pw):
            st.success("Account created! Login now.")
        else:
            st.error("Username already exists!")

st.markdown("</div>", unsafe_allow_html=True)
