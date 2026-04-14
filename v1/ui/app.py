import streamlit as st
import requests

API_URL = "http://localhost:8000/api/v1"

st.set_page_config(page_title="Legal AI", layout="wide")

# ---- Styling ----
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
</style>
""", unsafe_allow_html=True)

# ---- Header ----
st.title("⚖️ Legal Contract Analyzer")
st.write("Analyze clauses, detect risks, and ask legal questions.")

# ---- Input ----
st.subheader("📄 Enter Contract or Clause")

uploaded_file = st.file_uploader("Upload a contract file (.txt or .pdf)", type=["txt", "pdf"])

if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        # For PDF, need pdfplumber or similar, but for simplicity, assume text
        st.error("PDF support not implemented yet. Please paste text.")
        text = ""
    else:
        text = ""
else:
    text = st.text_area("Paste contract text here", height=200)

# ---- Buttons ----
col1, col2, col3 = st.columns(3)

analyze = col1.button("Analyze Risk")
ask = col2.button("Ask Question")
summarize = col3.button("Summarize")

# ---- Analyze ----
if analyze and text:
    response = requests.post(
        f"{API_URL}/analyze-risk",
        json={"clause": text}
    ).json()

    st.subheader("📊 Analysis Result")

    st.write(f"**Type:** {response['type']}")
    
    risk = response['risk']
    if risk == "High":
        st.markdown(f"**Risk:** <span style='color:red;'>🔴 {risk}</span>", unsafe_allow_html=True)
    elif risk == "Medium":
        st.markdown(f"**Risk:** <span style='color:orange;'>🟡 {risk}</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"**Risk:** <span style='color:green;'>🟢 {risk}</span>", unsafe_allow_html=True)
    
    st.write(f"**Explanation:** {response['explanation']}")
    st.write(f"**Confidence:** {response['confidence']:.2f}")

# ---- Ask ----
if ask and text:
    question = st.text_input("Enter your question")

    if question:
        response = requests.post(
            f"{API_URL}/ask",
            json={"question": question, "context": text}
        ).json()

        st.subheader("💬 Answer")
        st.write(response["answer"])

# ---- Summarize ----
if summarize and text:
    response = requests.post(
        f"{API_URL}/summarize",
        json={"text": text}
    ).json()

    st.subheader("📝 Summary")
    st.write(response["summary"])