# 📘 Phase 10 — Local RAG Vector Database Workflow (MiniLM + Chroma)
### AI_Engineering_Digital_Signal_Telemetry — RAG Architecture Overview  
### RAW Markdown — Single Fenced Block

# 🧭 Purpose

Phase 10 builds the **local Retrieval-Augmented Generation (RAG) vector database** used by the Llama 3B and 8B models. It converts embedding text into searchable vectors and stores them in a ChromaDB collection located in the local `rag_db/` directory.

This phase provides the factual grounding required for the Agentic Loop and Dashboard UI.

# 🧱 Inputs

- `embedding_cases.jsonl`  
  Generated in Phase 8 (embedding)  
  Contains cleaned, validated, domain‑specific text blocks.

# 🗂️ Output

- `rag_db/`  
  Local ChromaDB directory containing:
  - vector index  
  - metadata  
  - collection configuration  

# ⚙️ Components

### **run_phase_vector_ingestion()**
Responsible for:

- loading `embedding_cases.jsonl`  
- generating MiniLM embeddings  
- creating the ChromaDB collection  
- inserting all case vectors  
- verifying index integrity  

# 📦 Vector DB Structure

### **Collection Name**
`radio_cases`

### **Stored Fields**
- `id`  
- `text`  
- `embedding`  
- `metadata` (CaseId, protocol type, symptom tags)

# 🔍 Retrieval Behavior

Queries from:

- Python sidecar (`/rag/query`)  
- Dashboard UI  
- Agentic Loop (Phase 12)

are resolved through:

1. MiniLM embedding of the query  
2. similarity search in `radio_cases`  
3. return of top‑k relevant cases  

# 🧩 Summary

Phase 10 produces the **local RAG index** that powers:

- Llama 3B/8B retrieval  
- Agentic reasoning  
- Dashboard UI diagnostics  

It is a foundational component of the full PHASE 1–PHASE 12 pipeline.
