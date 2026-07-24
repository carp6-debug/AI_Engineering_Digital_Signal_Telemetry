# 🧭 AI Engineering — Unified PHASE 1–PHASE 12 Overview

This document summarizes the operational architecture of the AI_Engineering_Digital_Signal_Telemetry system, including Llama 3B/8B model integration, RAG workflows, finetuning pipelines, and the Agentic Loop. It also outlines the validation and test scripts used to verify the Python sidecar API that powers the Dashboard UI.

---

# 🏗️ System Architecture Summary

The system consists of:

1. **PHASE 1–PHASE 9: Data Preparation Pipeline**  
2. **PHASE 10: RAG Vector Database**  
3. **PHASE 11: Finetuning Engine (QLoRA)**  
4. **PHASE 12: Agentic RAG Loop**  
5. **Python Intelligence Sidecar (API Layer)**  
6. **Dashboard UI (.NET 9)**  
7. **Test Harness Scripts (Validation Layer)**  

All components are orchestrated through the **main.py execution flow**, which controls creation, validation, and invocation of each phase.

---

# 🧩 PHASE 1–PHASE 12 — Main Execution Flow (Conceptual)

The main pipeline consists of the following engines:

- **ingestion case load()**  
- **schema validator()**  
- **embedding builder()**  
- **finetune builder()**  
- **finetune engine()**  
- **rag engine()**  
- **agentic engine()**

These represent the *core functional units* of the entire system.

---

# ⚙️ PHASE 1–PHASE 5 — Ingestion Pipeline

### Purpose  
Convert raw troubleshooting cases into normalized, structured JSON objects.

### Components  
- `run_ingestion()`  
- `load_json_dataset()`  
- `save_json_dataset()`

### Outputs  
- `cases_raw.json`  
- `cases_normalized.json`

### Notes  
This phase is skippable once baseline files exist.

---

# 🧼 PHASE 6 — Cleaning Engine

### Purpose  
Remove noise, fix formatting, unify terminology.

### Component  
- `clean_case(case)`

### Output  
- `cases_clean.json`

---

# 📐 PHASE 7 — Schema Validation

### Purpose  
Ensure all cases conform to the canonical CASE_SCHEMA.

### Component  
- `validate_case_schema(case, CASE_SCHEMA)`

### Output  
- `validated_cases.json`

---

# 🧩 PHASE 8 — Embedding Text Construction

### Purpose  
Generate embedding‑ready text blocks.

### Component  
- `run_embedding()`

### Output  
- `embedding_cases.jsonl`

---

# 🧪 PHASE 9 — Finetuning JSONL Construction

### Purpose  
Create instruction‑response pairs for QLoRA finetuning.

### Component  
- `run_phase_9_finetune()`

### Output  
- `finetune_cases.jsonl`

---

# 🗂️ PHASE 10 — RAG Vector Database Build

### Purpose  
Build the ChromaDB vector index.

### Component  
- `run_phase_vector_ingestion()`

### Output  
- `rag_db/` (ChromaDB directory)

---

# 🧠 PHASE 11 — QLoRA Finetuning Engine

### Purpose  
Finetune Llama 3B/8B using domain‑specific cases.

### Component  
- `run_phase11_finetune()`

### Output  
- `models/finetune_engine_phase11/`

---

# 🤖 PHASE 12 — Agentic RAG Loop

### Purpose  
Combine RAG retrieval + finetuned reasoning + multi‑step agentic workflow.

### Component  
- `run_phase12_agentic()`

### Behavior  
Autonomous multi‑step reasoning using RAG → LLM → tool invocation → refinement.

---

# 🛰️ Python Intelligence Sidecar (API Layer)

### Purpose  
Expose model, RAG, and agentic capabilities to the Dashboard UI.

### Components  
- `intelligence_sidecar.py`  
- `fingerprint_adapter_3B.py`  
- `fingerprint_adapter_8B.py`

### Notes  
FastAPI endpoints for inference, RAG, metadata, and agentic flow.

---

# 🖥️ Dashboard UI (.NET 9)

### Purpose  
Provide user interface for diagnostics, RAG queries, finetuning tests, and agentic workflows.

### Notes  
Communicates with Python sidecar via HTTP endpoints.

---

# 🧪 Test Harness — Post‑Process Validation Layer

These scripts validate the correctness of each phase and ensure the system behaves as expected after PHASE 1–PHASE 12 execution.

### **RAG Validation**
- `test_phase10_rag.py`  
  Validates ChromaDB ingestion and retrieval.

### **Finetuning Validation**
- `test_phase11_finetune.py`  
  Runs standalone finetuning tests.

### **Agentic Loop Validation**
- `test_phase12_agentic.py`  
  Runs standalone agentic reasoning loop.

### **Sidecar Endpoint Validation**
- `test_sidecar_rag.py`  
  Validates RAG endpoint behavior.  
- `test_rag_metadata.py`  
  Validates metadata retrieval.

### **Model Adapter Validation**
- `fingerprint_adapter_3B.py`  
  Ensures correct loading of Llama 3B.  
- `fingerprint_adapter_8B.py`  
  Ensures correct loading of Llama 8B.

### **Final Process Validation**
- `intelligence_sidecar.py`  
  Full server endpoint for Model, RAG, and Agentic API.  
- `test_llama_3B.py`  
  Script client version of Dashboard UI for 3B model.  
- `test_llama_8B.py`  
  Script client version of Dashboard UI for 8B model.

---

# 🧩 Final Summary

This unified document reflects the **actual working PHASE 1–PHASE 12 system**, including:

- ingestion  
- cleaning  
- validation  
- embedding  
- finetuning  
- RAG  
- agentic reasoning  
- sidecar endpoints  
- Dashboard UI  
- full test harness  

It incorporates all insights from project completion and fully aligns with the modern Llama 3B/8B architecture.

This is the authoritative overview for the entire system.
