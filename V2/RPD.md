# ⚖️ Legal Contract Intelligence Engine (V2) — Product Requirements Document

## 1. 📌 Overview

### 1.1 Product Name
Legal Contract Intelligence Engine (V2)

### 1.2 Vision
To build an intelligent, explainable, and fully offline-capable legal AI system that can analyze entire contracts, detect risks, retrieve relevant clauses, and assist users with contextual legal insights using a hybrid RAG + LLM architecture.

### 1.3 Objectives
- Extend V1 clause-level intelligence to full document understanding
- Introduce Retrieval-Augmented Generation (RAG)
- Improve risk detection accuracy using hybrid reasoning
- Enable contract-level insights and Q&A
- Maintain low-cost, offline-first capability

---

## 2. 🎯 Goals & Success Metrics

### 2.1 Goals
- Accurate clause classification and risk detection
- Context-aware Q&A using contract data
- Explainable outputs for legal understanding
- Scalable modular architecture

### 2.2 Success Metrics

| Metric | Target |
|------|--------|
| Clause Classification Accuracy | ≥ 85% |
| Risk Detection Accuracy | ≥ 50% |
| Q&A Relevance | ≥ 80% |
| Latency (per query) | < 5 sec |
| System Cost | $0 (offline mode) |

---

## 3. 👤 Target Users

- Law students
- Developers building legal AI tools
- Small businesses reviewing contracts
- Researchers in NLP / Legal AI

---

## 4. 🧠 Core Features

### 4.1 Document Parsing
- Input: PDF / DOCX contracts
- Extract:
  - Full text
  - Sections
  - Clauses

---

### 4.2 Clause Classification (Enhanced V1)
- Classify clauses into:
  - Liability
  - Indemnity
  - Termination
  - Confidentiality
  - IP Ownership
- Uses:
  - Few-shot LLM prompting
  - Dataset-based labels

---

### 4.3 Hybrid Risk Engine
- Combines:
  - LLM predictions
  - Rule-based scoring

#### Risk Logic:
final_risk = max(llm_risk, rule_risk)


#### Risk Categories:
- 🔴 High
- 🟡 Medium
- 🟢 Low

---

### 4.4 RAG-based Q&A System
- Uses vector database (FAISS / Chroma)
- Retrieves relevant clauses before answering

#### Flow:

User Query → Retriever → Context → LLM → Answer + Citations


---

### 4.5 Contract Summarization
- Extract:
  - Parties
  - Duration
  - Key obligations
  - Risk overview

---

### 4.6 Conflict Detection
- Detect contradictions such as:
  - Mismatched termination periods
  - Conflicting obligations

---

### 4.7 Risk Scoring System (New)
- Assign overall contract score:

0–30 → Low Risk
31–70 → Medium Risk
71–100 → High Risk


---

### 4.8 Explainability Layer
- Provide:
  - Reason for classification
  - Reason for risk
  - Highlight keywords

---

### 4.9 Multi-Clause Insights (New)
- Top risky clauses
- Missing clause detection
- Contract-level recommendations

---

## 5. 🏗️ System Architecture

### 5.1 High-Level Flow


Document Input
↓
Document Parser
↓
Chunking + Embeddings
↓
Vector Database (FAISS)
↓
┌──────────────┬──────────────┬──────────────┐
↓ ↓ ↓
Classifier Risk Engine QA System (RAG)
(V1 + LLM) (Hybrid) (Retriever + LLM)
↓ ↓ ↓
└────────── Final Output ──────────┘


---

## 6. 🧩 Module Breakdown

### Core Modules

| Module | Description |
|------|-------------|
| document_parser.py | Extract structured text from contracts |
| indexer.py | Build vector embeddings |
| clause_classifier.py | Classify clause types |
| risk_engine.py | Hybrid risk scoring |
| summarizer.py | Generate summaries |
| conflict_detector.py | Detect contradictions |
| qa_chain.py | RAG-based Q&A |

---

## 7. 🔌 API Requirements

### 7.1 Analyze Contract

POST /analyze
Input: contract file / text
Output: summary, clauses, risks


### 7.2 Ask Question

POST /ask
Input: question + contract context
Output: answer + citations


### 7.3 Summarize

POST /summarize
Input: contract text
Output: structured summary


---

## 8. 🖥️ UI Requirements

### Features:
- Upload contract (PDF/DOCX)
- Display:
  - Summary
  - Clause list
  - Risk levels (color-coded)
- Q&A interface
- Highlight risky terms

---

## 9. ⚙️ Technical Requirements

### Backend
- Python
- FastAPI

### AI Stack
- Mistral 7B (LM Studio)
- Sentence Transformers
- FAISS

### Frontend
- Streamlit

---

## 10. 📊 Data Requirements

- Kaggle legal clauses dataset
- Custom labeled clauses
- Prompt templates

---

## 11. ⚠️ Constraints

- Limited context window for LLM
- PDF parsing inaccuracies
- Subjective nature of risk detection
- No legal liability (educational use only)

---

## 12. 🚧 Non-Goals (V2 Scope Limitations)

- No full legal compliance guarantee
- No jurisdiction-specific legal advice
- No real-time legal updates

---

## 13. 🔮 Future Scope (V3+)

- Fine-tuned legal LLM
- Multi-language contracts
- OCR for scanned PDFs
- Legal recommendation engine
- Clause rewriting suggestions

---

## 14. 🧪 Evaluation Plan

### Metrics:
- Classification accuracy
- Risk accuracy
- Retrieval relevance (RAG)
- User satisfaction (manual testing)

---

## 15. 📌 Conclusion

V2 transforms the system from a clause-level analyzer into a **full contract intelligence platform** by integrating:

- Retrieval-Augmented Generation (RAG)
- Hybrid reasoning (LLM + rules)
- Contract-level insights
- Explainable legal AI

This version positions the system as a **practical legal copilot for contract understanding and risk analysis**.

---