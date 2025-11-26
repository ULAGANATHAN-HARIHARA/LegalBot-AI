# Home.py (Landing Page)
import streamlit as st

st.set_page_config(
    page_title="LegalBot - Home",
    page_icon="⚖️",
    layout="centered"
)

# ---- GLOBAL STYLE ----
st.markdown("""
<style>
body {
    background: linear-gradient(145deg, #0b1120 0%, #1e293b 100%);
}
.main {
    background: transparent;
}
.hero {
    margin-top: 90px;
    padding: 50px 30px;
    text-align: center;
}
.title {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(90deg, #0ea5e9, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    font-size: 1.2rem;
    color: #cbd5e1;
}
.btn-start button {
    width: 60%;
    border-radius: 15px;
    padding: 13px;
    font-weight: bold;
    background-color: #0ea5e9;
    border: none;
    color: #fff;
}
.btn-start button:hover {
    background-color: #0284c7;
}
</style>
""", unsafe_allow_html=True)

# ---- UI CONTENT ----
st.markdown("""
<div class='hero'>
    <div style='font-size:60px;'>⚖️</div>
    <div class='title'>LegalBot</div>
    <div class='subtitle'>Understand the law. Know your rights.</div><br>
</div>
""", unsafe_allow_html=True)

col = st.columns(3)
with col[1]:
    if st.button("Start ⚡", key="start", use_container_width=True):
        st.switch_page("pages/1_Login.py")
