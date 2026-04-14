# LexAI V1 — Fine-Tuned Legal Contract Intelligence Engine

## 1. Objective

Build a domain-specific legal AI backend that can:
- Analyze contracts
- Detect risks
- Answer legal questions
- Generate explanations
- Suggest clause improvements

---

## 2. Core Features

### 2.1 Summarization
- Document-level summary
- Clause-level summary

### 2.2 Legal Q&A
- Context-aware question answering based on contract input

### 2.3 Risk Analysis
- Clause-level risk detection
- Risk classification: Low / Medium / High

### 2.4 Clause Classification
- Identify clause types:
  - Confidentiality
  - Liability
  - Termination
  - Indemnity

### 2.5 Explanation Engine
- Provide reasoning for detected risks
- Contextual legal justification

### 2.6 Clause Rewriting
- Suggest safer or improved clause versions

### 2.7 Metadata Extraction
- Extract:
  - Parties
  - Dates
  - Jurisdiction

---

## 3. System Architecture

### 3.1 High-Level Flow

User Input → Preprocessing → Model Inference → Post-processing → API Response

---

### 3.2 Layers

#### API Layer
- Handles HTTP requests and responses

#### Service Layer
- Clause parsing
- Processing logic
- Data transformation

#### Interface Layer
- Model interaction
- Inference handling
- Fine-tuned model usage

---

## 4. Project Structure
src/
│
├── api/
│ ├── app.py
│ ├── routes.py
│
├── interfaces/
│ ├── fine_tuner.py
│ ├── llm_client.py
│ ├── qa_engine.py
│ ├── risk_analyzer.py
│ ├── summarizer.py
│ ├── clause_rewriter.py
│
├── services/
│ ├── dataset_builder.py
│ ├── evaluator.py
│ ├── inference_service.py
│ ├── clause_parser.py
│ ├── explanation_generator.py
│ ├── metadata_extractor.py
│
├── tests/
│ ├── test_api.py
│ ├── test_dataset_builder.py
│ ├── test_evaluator.py
│ ├── test_fine_tuner.py


---

## 5. API Design

### Base Path

/api/v1


---

### 5.1 Summarize

POST /summarize

Request:

{
"text": "contract text"
}

Response:

{
"summary": "..."
}


---

### 5.2 Ask Question

POST /ask

Request:

{
"question": "...",
"context": "contract text"
}


---

### 5.3 Analyze Risk

POST /analyze-risk

Response:

{
"overall_risk": "High",
"clauses": [
{
"text": "...",
"risk": "High",
"reason": "..."
}
]
}


---

### 5.4 Suggest Edits

POST /suggest-edits


---

### 5.5 Extract Metadata

POST /extract-metadata


---

### 5.6 Train Model

POST /train-model


---

### 5.7 Upload Dataset

POST /upload-dataset


---

### 5.8 Model Status

GET /model-status


---

## 6. Core Modules

### 6.1 dataset_builder.py
- Clause extraction
- Label structuring
- JSONL generation

### 6.2 fine_tuner.py
- Handles fine-tuning process
- Stores model reference

### 6.3 inference_service.py
- Central inference handler
- Uses fine-tuned model if available

### 6.4 clause_parser.py
- Splits contracts into logical clauses

### 6.5 risk_analyzer.py
- Assigns risk levels to clauses

### 6.6 explanation_generator.py
- Generates reasoning for outputs

### 6.7 clause_rewriter.py
- Suggests improved clause versions

### 6.8 metadata_extractor.py
- Extracts structured contract metadata

---

## 7. Evaluation

- Q&A Accuracy
- Risk Detection Precision / Recall
- Summarization Quality (ROUGE or equivalent)
- Response Quality (manual validation)

---

## 8. Tech Stack

- Backend: FastAPI
- Language: Python
- Model: Fine-tuned LLM (OpenAI or open-source)
- NLP: spaCy / transformers

---

## 9. Non-Functional Requirements

- Low latency responses
- Modular and scalable architecture
- Clean API design
- Secure key handling

---

## 10. Future Scope

- RAG-based retrieval system (V2)
- Contract comparison engine
- Multi-agent reasoning system
- Next.js frontend integration

---