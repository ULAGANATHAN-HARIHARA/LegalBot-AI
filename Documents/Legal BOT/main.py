import streamlit as st
import time
from utils.db_utils import login_user, register_user

st.set_page_config(page_title="LegalBot Login", page_icon="⚖️", layout="centered")

st.markdown("""
    <style>
    body { background: linear-gradient(135deg, #0a0a0a 40%, #1f1f1f 100%); color: white; }
    .main { background-color: transparent; }
    div.block-container { padding-top: 3rem; max-width: 500px; margin: auto; }
    h1 { text-align: center; color: #00b4d8; font-size: 2.2rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚖️ LegalBot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#bdbdbd;'>AI-Powered Judiciary Reference System</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔐 Login", "🆕 Sign Up"])

with tab1:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state["username"] = username
            st.success("✅ Welcome back! Redirecting...")
            time.sleep(1)
            st.switch_page("pages/2_LegalBot.py")
        else:
            st.error("❌ Invalid credentials.")

with tab2:
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Sign Up"):
        if new_user and new_pass:
            register_user(new_user, new_pass)
            st.success("✅ Account created! You can log in now.")
        else:
            st.warning("Please fill all fields.")

