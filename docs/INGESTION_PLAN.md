# 📥 Ingestion Plan

## AI_Engineering_Digital_Signal_Telemetry

---

## 📄 Dataset Format

The dataset will use **JSON** as the primary format.  
This supports:

- Nested fields  
- Multi‑step resolution sequences  
- Mixed numeric + text data  
- RAG retrieval  
- Finetuning (JSONL conversion)  
- Agentic workflows  

---

## 🔧 Python Ingestion Architecture  

### 1. ingestion/load_cases.py

**Responsibilities:**

- Load JSON dataset  
- Validate required fields  
- Normalize field names  
- Save raw copy to `data/raw/`

---

### 2. cleaning/clean_cases.py

**Responsibilities:**

- Normalize ProtocolFamily  
- Normalize ObservedSignals  
- Clean text fields  
- Prepare combined “embedding_text” field  
- Save cleaned dataset to `data/processed/`

---

### 3. schema/case_schema.py

**Responsibilities:**

- Define canonical data model  
- Validate cleaned dataset  
- Enforce required fields  
- Output validated dataset

---

## 🔄 Data Flow

```Text
JSON Dataset
↓
ingestion/load_cases.py
↓
data/raw/cases_raw.json
↓
cleaning/clean_cases.py
↓
data/processed/cases_clean.json
↓
schema/case_schema.py
↓
validated_cases.json
```

---

## 📘 Notes
  
This ingestion pipeline is intentionally simple and modular.  
It mirrors N‑Tier architecture principles and supports future expansion into:

- Embeddings  
- Vector DB population  
- RAG retrieval  
- Finetuning  
- Agentic workflows
  