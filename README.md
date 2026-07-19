# 📡 AI Engineering: Digital Signal Telemetry System  
### **RAG • Finetuning • Agentic Workflows • Python‑Driven N‑Tier Architecture**

---

# 🧭 Executive Summary — The Evolution of AI Engineering

AI Engineering has progressed from early statistical language models to modern agentic, model‑driven systems capable of autonomous reasoning. Its evolution spans four eras:

## **1. Early Foundations (1940s–1980s)**
- Shannon’s information theory formalized prediction.  
- N‑gram models enabled early text prediction and speech recognition.  
- Vector Space Models introduced document similarity — the precursor to embeddings.

## **2. Machine Learning Era (1980s–2010s)**
- Rise of supervised, unsupervised, and reinforcement learning.  
- Practical systems emerged: spam filters, search ranking, recommendations, speech recognition, computer vision.  
- Software shifted from deterministic logic to probabilistic learning.

## **3. Deep Learning & Early LLMs (2010s)**
- Word2Vec, GloVe, LSTMs, GRUs improved semantic modeling.  
- Transformers revolutionized NLP with attention mechanisms.  
- Early LLMs (GPT‑1/2) demonstrated summarization, translation, and reasoning.

## **4. Modern AI Engineering (2020s–present)**
- LLMs integrated into applications  
- RAG architectures combining vector search + generation  
- Agentic workflows enabling multi‑step reasoning  
- Finetuning pipelines for domain specialization  
- AI‑native applications built around model reasoning rather than UI‑driven logic

---

# 🧭 Project Overview  
The **AI Engineering: Digital Signal Telemetry System** is a fully Python‑driven, enterprise‑grade AI platform designed to ingest, structure, embed, retrieve, and reason about **digital radio communications**, **signal integrity**, and **failure diagnostics**.

### ✔ Fully Local, Self‑Contained Python Architecture  
This project is intentionally designed to run **entirely on local hardware**, without any cloud dependencies. All components — ingestion, cleaning, embeddings, vector database, RAG retrieval, QLoRA finetuning, and agentic reasoning — are implemented using **Python only** and operate fully offline.

The system uses:

- **Local LLM inference** (Mistral‑7B + QLoRA adapter)  
- **Local embeddings** (MiniLM)  
- **Local vector database** (ChromaDB)  
- **Local agentic loop** (Python orchestration)  

This demonstrates complete AI architecture capability using **self‑contained Python modules**, showcasing practical, real‑world AI engineering skills without relying on external APIs or cloud‑hosted models.

### ✔ Demonstration of System Architect & Data Engineering Skills  
This project was intentionally built to demonstrate:

- **System Architecture** — multi‑tier design, separation of concerns, modular pipelines  
- **Data Engineering** — ingestion, normalization, validation, cleaning, schema design  
- **AI Engineering** — embeddings, vector DB, RAG, finetuning, agentic reasoning  
- **LLM Operations** — local inference, adapter loading, model lifecycle  
- **Pipeline Orchestration** — multi‑phase execution, reproducible workflows  

The entire architecture is implemented using **Python only**, reinforcing mastery of Python as a primary language for modern AI systems.

---

# 🎯 Project Objective  
To design and implement a complete AI Engineering system that:

- Ingests and cleans structured troubleshooting cases  
- Normalizes schema for multi‑phase processing  
- Generates embeddings and builds a vector database  
- Implements RAG retrieval  
- Finetunes a domain‑specific LLM  
- Executes agentic multi‑step diagnostic reasoning  
- Demonstrates full AI architecture using **Python only**  
- Produces a portfolio‑ready, interview‑ready, enterprise‑grade system  

---

# 🌐 Domain Rationale — Digital Radio Communications  
This project focuses on **DMR Tier II**, **P25 Phase I**, and **NXDN 4800** digital radio systems because they provide:

### ✔ Rich, structured, text‑dense diagnostic data  
Digital radio systems generate logs, metrics, and structured telemetry ideal for:

- RAG retrieval  
- Finetuning  
- Agentic workflows  

### ✔ Strong parallels to LLM internal mechanics  
Digital RF systems rely on:

- Noise → signal correction  
- Compression  
- Error detection (CRC)  
- Symbol timing  
- Multi‑step decoding  
- Pattern recognition  

These concepts map directly to:

- Tokenization  
- Embeddings  
- Attention  
- Vector similarity  
- Multi‑step reasoning  

### ✔ Real‑world engineering depth  
DMR, P25, and NXDN each introduce unique digital behaviors:

- **DMR Tier II** — 4‑FSK modulation, TDMA slot timing, BER sensitivity  
- **P25 Phase I** — NAC codes, IMBE vocoder parameters, frame acceptance rules  
- **NXDN 4800** — narrowband 4‑level FSK, feedline loss sensitivity, CRC behavior  

These systems provide **excellent diagnostic complexity** for AI reasoning.

---

# 📚 Representative Validated Cases

Below are **representative examples** from the validated dataset.  
Full dataset available in:  
**[EXAMPLE_CASES.md](ca://s?q=Open_EXAMPLE_CASES_document)**

---

### **Case 1 — DMR Tier II**
**Symptom:** Intermittent audio dropouts when mobile unit is in motion  
**Root Cause:** Multipath reflections causing symbol timing errors  
**Key Signals:** RSSI −92 dBm, SNR 14 dB, BER 5–10%  
**Notes:** DMR’s 4‑FSK modulation is highly sensitive to multipath.

---

### **Case 2 — P25 Phase I**
**Symptom:** “INVALID NAC” error  
**Root Cause:** Subscriber radios programmed with mismatched NAC  
**Key Signals:** RSSI −78 dBm, SNR 22 dB  
**Notes:** NAC mismatches prevent frame acceptance even with excellent RF.

---

### **Case 3 — NXDN 4800**
**Symptom:** Frequent CRC failures on repeater uplink  
**Root Cause:** Excessive feedline loss causing marginal signal levels  
**Key Signals:** RSSI −85 dBm, SNR 18 dB, Cable Loss 6.5 dB  
**Notes:** NXDN narrowband FSK is highly sensitive to SNR degradation.

---

### **Case 4 — DMR Tier II**
**Symptom:** Slot 2 inaccessible; Slot 1 normal  
**Root Cause:** TDMA slot timing drift due to disabled GPS timing  
**Notes:** DMR TDMA requires strict 30 ms slot boundaries.

---

### **Case 5 — P25 Phase I**
**Symptom:** Garbled / robotic audio  
**Root Cause:** IMBE vocoder parameter mismatch  
**Notes:** Vocoder mismatches cause audio artifacts even with good RF.

---

# 🧩 Full Pipeline Summary — **PHASE 1 → PHASE 12**

## **PHASE 1 — Raw Case Acquisition**
Collect raw troubleshooting cases.

## **PHASE 2 — Normalization**
Convert raw cases into a consistent schema.

## **PHASE 3 — Schema Definition**
Define the **Normalized Case Object**.

## **PHASE 4 — Validation**
Validate fields, enforce types, ensure completeness.

## **PHASE 5 — Cleaning**
Remove noise, unify terminology.

## **PHASE 6 — JSONL Conversion**
Convert cleaned cases into JSONL for embeddings.

## **PHASE 7 — Embedding Generation**
Use MiniLM (`all-MiniLM-L6-v2`) to embed case text.

## **PHASE 8 — Vector Database Construction**
Build local RAG DB using ChromaDB.

## **PHASE 9 — Retrieval Harness**
Implement similarity search testing.

## **PHASE 10 — RAG Pipeline**
Full RAG retrieval using MiniLM + ChromaDB.

## **PHASE 11 — QLoRA Finetuning**
Finetune Mistral‑7B using `finetune_cases.jsonl`.

## **PHASE 12 — Agentic RAG Loop**
Combine RAG + finetuned LLM + multi‑step reasoning.

---

# 🏗 Architecture Overview — Python‑Driven N‑Tier System

Even without web tiers, this project remains **N‑Tier**, because N‑Tier is an architectural pattern, not a technology requirement.

### **Tier 1 — Data Layer**
- Raw → normalized → validated → cleaned → embedded → vector DB

### **Tier 2 — AI Layer**
- RAG retrieval  
- Finetuned LLM  
- Agentic reasoning

### **Tier 3 — Application Layer**
- CLI tools  
- Test harnesses  
- Orchestration scripts  

This demonstrates a complete AI architecture using **Python only**, aligning directly with industry expectations for:

- **System Architects**  
- **Data Engineers**  
- **AI Engineers**  
- **Machine Learning Engineers**

---

# 📁 Directory Trees (Option C)

## **TREE 1 — Source Code Structure**

```text
AI_ENGINEERING_DIGITAL_SIGNAL_TELEMETRY/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── validated/
│   └── embedding/
│
├── python/
│   ├── agentic_engine/
│   │   └── phase12_agentic_loop.py
│   │
│   ├── cleaning/
│   │   └── clean_cases.py
│   │
│   ├── embedding/
│   │   └── embedding_builder.py
│   │
│   ├── finetune_engine/
│   │   └── phase11_qlora.py
│   │
│   ├── ingestion/
│   │   └── load_cases.py
│   │
│   ├── rag_engine/
│   │   └── vector_ingestion.py
│   │
│   └── schema/
│       └── case_schema.py
│
├── tests/
│   ├── test_phase10_rag.py
│   ├── test_phase11_finetune.py
│   ├── test_phase12_agentic.py
│   ├── main.py
│   └── paths.py
│
└── docs/   (not expanded)
```

---

## **TREE 2 — Data Pipeline Structure**

```text
data/
│
├── raw/
│   ├── cases_raw.json
│   └── cases_normalized.json
│
├── processed/
│   └── cases_clean.json
│
├── validated/
│   ├── validated_cases.json
│   └── embedding_cases.jsonl
│
└── embedding/
    └── finetune_cases.jsonl
```

---

## **TREE 3 — Models + Vector Database Structure**

```text
models/
└── finetune_engine_phase11/
    └── checkpoint-5/
        ├── adapter_config.json
        ├── adapter_model.safetensors
        ├── optimizer.pt
        ├── scheduler.pt
        ├── rng_state.pth
        ├── trainer_state.json
        ├── training_args.bin
        └── README.md

rag_db/
└── <uuid>/
    ├── data_level0.bin
    ├── header.bin
    ├── length.bin
    ├── link_lists.bin
    └── chroma.sqlite3
```

---

# 📚 Documentation Index

All documentation is located in `/docs`:

- AI_ENGINEERING_ARCH_BRIEF.md  
- AI_ENGINEERING_BRIEF.md  
- BLUEPRINT.md  
- DATASET_NOTES.md  
- EXAMPLE_CASES.md  
- HOWTO_Agentic.md  
- HOWTO_Chroma.md  
- HOWTO_JSONL.md  
- HOWTO_QLoRA.md  
- INGESTION_PLAN.md  
- NORMALIZED_CASE_OBJECT.md  
- PHASE_10_RAG_VECTOR_DATABASE_FLOW.md  
- PHASE_11_FINETUNING_OVERVIEW_FLOW.md  
- PHASE_12_AGENTIC_RAG_LOOP_FLOW.md  
- REFERENCE_INGESTION_GUIDE.md
- FUNCTIONAL_BLUEPRINT.md  

---

# ▶️ How to Run

## **1. Build the Vector Database**
```bash
python -m python.embedding.embedding_builder
python -m python.rag_engine.vector_ingestion
```

## **2. Test Retrieval**
```bash
python -m python.tests.test_phase10_rag
```

## **3. Run Finetuning**
```bash
python -m python.finetune_engine.phase11_qlora
```

## **4. Run Agentic RAG Loop**
```bash
python -m python.tests.test_phase12_agentic
```

---

# 🏁 Final Project Status — **COMPLETE**

All phases (1–12) have been successfully implemented:

- Data ingestion  
- Schema normalization  
- Cleaning  
- Embedding  
- Vector DB  
- RAG retrieval  
- QLoRA finetuning  
- Agentic diagnostic reasoning  

This project now represents a **fully operational Python‑driven AI Engineering system**, suitable for:

- Senior AI Engineering roles  
- System Architecture roles  
- Data Engineering roles  
- Machine Learning Engineering roles  
- Portfolio demonstration  
- Interview discussion  
- Enterprise integration  

---

# ✔ End of README.md


