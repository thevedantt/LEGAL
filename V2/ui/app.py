import streamlit as st
import requests
import os
import matplotlib.pyplot as plt

BACKEND = os.getenv("LEGAL_BACKEND_URL", "http://127.0.0.1:8000")

st.title("Legal Contract Intelligence Engine v2")

st.sidebar.header("1. Upload or Paste your contract")
uploaded = st.sidebar.file_uploader("PDF or DOCX contract", type=["pdf", "docx"])
text = ""
if "contract_text" not in st.session_state:
    st.session_state.contract_text = ""

if uploaded:
    resp = requests.post(f"{BACKEND}/parse", files={"file": uploaded})
    if resp.ok:
        text = resp.json()["text"]
        st.session_state.contract_text = text
        st.success("Parsed contract loaded.")
    else:
        st.error(f"Parse error: {resp.text}")

txt_input = st.sidebar.text_area("Or paste contract text", value=st.session_state.contract_text, height=250)

if st.sidebar.button("Use Text"):
    st.session_state.contract_text = txt_input
    st.success("Using custom contract text.")

if not st.session_state.contract_text:
    st.info("Upload a contract or paste text to begin.")
    st.stop()

contract_text = st.session_state.contract_text

st.header("Contract Explorer")
st.subheader("Parsed Contract Text")
with st.expander("Show contract text", expanded=False):
    st.write(contract_text[:5000] + ("..." if len(contract_text) > 5000 else ""))

if st.button("Show Chunks"):
    with st.spinner("Chunking ..."):
        resp = requests.post(f"{BACKEND}/rag/chunks", json={"contract_text": contract_text})
        if resp.ok:
            chunks = resp.json()["chunks"]
            for i, chunk in enumerate(chunks):
                with st.expander(f"Chunk {i}"):
                    st.write(chunk)
        else:
            st.error(f"Error getting chunks: {resp.text}")

if st.button("Classify Clauses"):
    with st.spinner("Classifying ..."):
        resp = requests.post(f"{BACKEND}/classify", json={"contract_text": contract_text})
        if resp.ok:
            clauses = resp.json()["clauses"]
            for i, c in enumerate(clauses):
                with st.expander(f"Clause {i} [{c['label']}]"):
                    st.write(c["text"])
                    st.caption(f"Reasoning: {c['reasoning']}")
        else:
            st.error(f"Classification error: {resp.text}")

if st.button("Risk Assessment"):
    with st.spinner("Scoring risk ..."):
        resp = requests.post(f"{BACKEND}/risk", json={"contract_text": contract_text})
        if resp.ok:
            risks = resp.json()["risks"]
            for i, r in enumerate(risks):
                with st.expander(f"Chunk {i} [LLM Risk: {r['llm_risk']}, Rules: {', '.join(r['rule_flags'])}]"):
                    st.write(r["text"])
                    st.caption(f"LLM Reasoning: {r['llm_reasoning']}")
        else:
            st.error(f"Risk error: {resp.text}")

import matplotlib.pyplot as plt

if st.button("Analyze Risk"):
    with st.spinner("Analyzing contract risk ..."):
        resp = requests.post(f"{BACKEND}/summarize", json={"contract_text": contract_text})
        if resp.ok:
            data = resp.json()
            if "summary" in data:
                summary = data["summary"]
                # 📊 Summary Panel
                st.subheader("📊 Contract Summary")
                st.markdown(f"**Parties:** {', '.join(summary.get('parties', []))}")
                st.markdown(f"**Effective Date:** {summary.get('effective_date', None)}")
                st.markdown(f"**Duration:** {summary.get('duration', None)}")
                # ⚠️ Clause Analysis Panel
                st.subheader("⚠️ Clause Analysis")
                key_clauses = summary.get('key_clauses', [])
                for c in key_clauses:
                    col1, col2 = st.columns([2,1])
                    with col1:
                        st.markdown(f"**{c.get('label', 'Clause')}**")
                        st.write(c.get('text', ''))
                    risk = c.get('risk', 'Unknown')
                    reason = c.get('reasoning', '')
                    risk_color = {'High':'#FF3B30','Medium':'#FFD600','Low':'#4CD964'}.get(risk, '#CCCCCC')
                    with col2:
                        st.markdown(f"**Risk:** <span style='color:{risk_color}'>{risk}</span>", unsafe_allow_html=True)
                        st.caption(f"{reason}")
                # 📈 Risk Distribution
                st.subheader("📈 Risk Distribution Pie Chart")
                # Aggregate risks
                risk_counts = {'High':0, 'Medium':0, 'Low':0}
                for c in key_clauses:
                    r = c.get('risk','Unknown')
                    if r in risk_counts:
                        risk_counts[r] += 1
                labels = [k for k in risk_counts.keys() if risk_counts[k]>0]
                sizes = [risk_counts[k] for k in labels]
                colors = ['#FF3B30','#FFD600','#4CD964'][:len(labels)]
                if sizes:
                    fig, ax = plt.subplots()
                    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
                    ax.axis('equal')
                    st.pyplot(fig)
                else:
                    st.info("No risk data to display.")
            else:
                st.error("Backend error: The 'summary' key is missing from the response.")
                st.write("Raw Response:")
                st.json(data)
        else:
            st.error(f"Summarization error: {resp.status_code}")
            st.write(resp.text)

if st.button("Check Conflicts"):
    with st.spinner("Detecting ..."):
        resp = requests.post(f"{BACKEND}/conflicts", json={"contract_text": contract_text})
        if resp.ok:
            conf = resp.json()
            st.subheader("Rule-based conflicts:")
            st.json(conf["rule_based_conflicts"])
            st.subheader("LLM-based conflicts:")
            st.json(conf["llm_conflicts"])
        else:
            st.error(f"Conflict error: {resp.text}")

st.divider()
st.header("Ask Contract Q&A")
q = st.text_input("Your question")
if st.button("Ask") and q and contract_text:
    with st.spinner("Thinking ..."):
        resp = requests.post(f"{BACKEND}/qa", json={"contract_text": contract_text, "question": q})
        if resp.ok:
            res = resp.json()
            st.subheader("Answer:")
            st.write(res["answer"])
            st.subheader("Citations:")
            for c in res["citations"]:
                st.caption(f"[Chunk {c['index']}]: {c['text'][:120]}...")
        else:
            st.error(f"Q&A error: {resp.text}")
