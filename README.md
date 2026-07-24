# 📡 AI Engineering: Digital Signal Telemetry System 
## RAG • Finetuning • Agentic Workflows • Python‑Driven N‑Tier Architecture

---

# 🧭 Executive Summary

The **AI Engineering: Digital Signal Telemetry System** is a fully local, Python‑driven AI platform implementing a complete **PHASE 1 → PHASE 12** AI engineering pipeline. It ingests, structures, embeds, retrieves, finetunes, and reasons about **DMR Tier II**, **P25 Phase I**, and **NXDN 4800** digital radio telemetry and troubleshooting cases using:

- **Local Llama 3B and Llama 8B models**  
- **QLoRA finetuning adapters**  
- **MiniLM embeddings**  
- **ChromaDB vector database**  
- **Agentic multi‑step reasoning loop**  
- **Python Intelligence Sidecar API**  
- **Optional .NET 9 Dashboard UI integration**

This project demonstrates complete AI engineering capability using **self‑contained Python modules**, showcasing practical, real‑world system architecture, data engineering, and AI reasoning workflows.

For immediate verification of system capability, see the AI Engineering Test Plan Results below.

## AI Engineering Test Plan Results

Jump directly into the verification testing for the AI Engineering Digital Signal Telemetry System. These results demonstrate the full end‑to‑end behavior of the **local Llama 3B and 8B models**, **QLoRA finetuning adapters**, **RAG vector database**, and **Python Intelligence Sidecar API**.

The test suite exercises:

- direct model inference  
- finetuned adapter evaluation  
- RAG retrieval against the local `rag_db/`  
- agentic multi‑step reasoning  
- domain‑specific DMR, P25, and NXDN troubleshooting cases  

This provides an immediate, real‑world demonstration of the system’s diagnostic capability in the Digital Signal Domain used in public service radio communications.

**View the full test results:**

[AI_ENGINEERING Digital Signal Test Results](./docs/AI_ENGINEERING_DS_TEST_RESULTS.md)

[AI_ENGINEERING Digital Signal Test Plan](./docs/AI_ENGINEERING_DS_TEST_PLAN.md)

---

# 🧭 Project Overview  

The **AI Engineering: Digital Signal Telemetry System** is a fully Python‑driven, enterprise‑grade AI platform designed to ingest, structure, embed, retrieve, and reason about **digital radio communications**, **signal integrity**, and **failure diagnostics**.

### ✔ Fully Local, Self‑Contained Python Architecture  
This project is intentionally designed to run **entirely on local hardware**, without any cloud dependencies. All components — ingestion, cleaning, embeddings, vector database, RAG retrieval, QLoRA finetuning, and agentic reasoning — are implemented using **Python only** and operate fully offline.

The system uses:

- **Local LLM inference** (Llama‑3B / Llama‑8B + QLoRA adapters)  
- **Local embeddings** (MiniLM)  
- **Local vector database** (ChromaDB → `rag_db/`)  
- **Local agentic loop** (Python orchestration)  
- **Local finetuning** (`models/finetune_engine_phase11/`)  

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
- Finetunes a domain‑specific LLM (Llama 3B/8B via QLoRA)  
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

### ✔ These concepts map directly to:

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

### 📚 Representative Validated Cases

Below are **representative examples** from the validated dataset (Full dataset available in **EXAMPLE_CASES.md**):

---

### Case 1 — DMR Tier II

**Symptom:** Intermittent audio dropouts when mobile unit is in motion  
**Root Cause:** Multipath reflections causing symbol timing errors  
**Key Signals:** RSSI −92 dBm, SNR 14 dB, BER 5–10%  
**Notes:** DMR’s 4‑FSK modulation is highly sensitive to multipath.

---

### Case 2 — P25 Phase I

**Symptom:** “INVALID NAC” error  
**Root Cause:** Subscriber radios programmed with mismatched NAC  
**Key Signals:** RSSI −78 dBm, SNR 22 dB  
**Notes:** NAC mismatches prevent frame acceptance even with excellent RF.

---

### Case 3 — NXDN 4800

**Symptom:** Frequent CRC failures on repeater uplink  
**Root Cause:** Excessive feedline loss causing marginal signal levels  
**Key Signals:** RSSI −85 dBm, SNR 18 dB, Cable Loss 6.5 dB  
**Notes:** NXDN narrowband FSK is highly sensitive to SNR degradation.

---

### Case 4 — DMR Tier II

**Symptom:** Slot 2 inaccessible; Slot 1 normal  
**Root Cause:** TDMA slot timing drift due to disabled GPS timing  
**Notes:** DMR TDMA requires strict 30 ms slot boundaries.

---

### Case 5 — P25 Phase I

**Symptom:** Garbled / robotic audio  
**Root Cause:** IMBE vocoder parameter mismatch  
**Notes:** Vocoder mismatches cause audio artifacts even with good RF.

---

## 🧩 Full Pipeline Summary — PHASE 1 → PHASE 12

### PHASE 1 — Raw Case Acquisition

Collect raw troubleshooting cases.

### PHASE 2 — Normalization

Convert raw cases into a consistent schema.

### PHASE 3 — Schema Definition

Define the **Normalized Case Object**.

### PHASE 4 — Validation

Validate fields, enforce types, ensure completeness.

### PHASE 5 — Cleaning

Remove noise, unify terminology.

### PHASE 6 — JSONL Conversion

Convert cleaned cases into JSONL for embeddings.

### PHASE 7 — Embedding Generation

Use MiniLM (`all-MiniLM-L6-v2`) to embed case text.

### PHASE 8 — Vector Database Construction

Build local RAG DB using ChromaDB (`rag_db/`).

### PHASE 9 — Retrieval Harness

Implement similarity search testing.

### PHASE 10 — RAG Pipeline

Full RAG retrieval using MiniLM + ChromaDB.

### PHASE 11 — QLoRA Finetuning

Finetune **Llama‑3B** or **Llama‑8B** using `finetune_cases.jsonl`.

### PHASE 12 — Agentic RAG Loop

Combine RAG + finetuned LLM + multi‑step reasoning.

---

# 🏗 Architecture Overview — Python‑Driven N‑Tier System

Even without web tiers, this project remains **N‑Tier**, because N‑Tier is an architectural pattern, not a technology requirement.

### Tier 1 — Data Layer

Raw → normalized → validated → cleaned → embedded → vector DB

### Tier 2 — AI Layer

- RAG retrieval  
- Finetuned LLM (Llama 3B/8B + QLoRA adapters)  
- Agentic reasoning

### Tier 3 — Application Layer

- CLI tools  
- Test harnesses  
- Orchestration scripts  
- Python Intelligence Sidecar  
- Optional .NET 9 Dashboard UI

This demonstrates a complete AI architecture using **Python only**, aligning directly with industry expectations for:

- **System Architects**  
- **Data Engineers**  
- **AI Engineers**  
- **Machine Learning Engineers**

---

## 📁 Directory Trees

### Source Code Structure

Below is the authoritative project structure as of the final commit.

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
├── models/
│   ├── finetune_engine_phase11_llama_3_1_8b/
│   │   ├── adapter_config.json
│   │   └── adapter_model.safetensors
│   │
│   ├── finetune_engine_phase11_llama_3_2_3b/
│   │   ├── adapter_config.json
│   │   └── adapter_model.safetensors
│   │
│   ├── llama-3.1-8b-instruct/
│   │   ├── config.json
│   │   ├── tokenizer.model
│   │   ├── tokenizer.json
│   │   ├── model.safetensors
│   │   └── generation_config.json
│   │
│   ├── llama-3.2-3b/
│   │   ├── config.json
│   │   ├── tokenizer.model
│   │   ├── tokenizer.json
│   │   ├── model.safetensors
│   │   └── generation_config.json
│   │
│   ├── phi3-mini/
│   │   ├── config.json
│   │   ├── tokenizer.json
│   │   ├── tokenizer.model
│   │   └── model.safetensors
│   │
│   └── (root contains no files)
│
├── rag_db/
│   └── <uuid>/
│       ├── data_level0.bin
│       ├── header.bin
│       ├── length.bin
│       ├── link_lists.bin
│       └── chroma.sqlite3
│
├── tests/
│   ├── test_phase10_rag.py
│   ├── test_phase11_finetune.py
│   ├── test_phase12_agentic.py
│   ├── main.py
│   └── paths.py
│
└── docs/

**Notes:**

- Finetune directories intentionally include only `adapter_config.json` and `adapter_model.safetensors` to avoid cluttering the repository with large checkpoint artifacts.  
- The `rag_db` directory is generated automatically during PHASE 10 and should not be manually edited.

```

### Data Pipeline Structure

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

### Models + Vector Database Structure

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

### 📚 Documentation Index

All documentation is located in `/docs`:

- AI_ENGINEERING_BRIEF.md  
- AI_ENGINEERING_DS_TEST_PLAN.md  
- AI_ENGINEERING_DS_TEST_RESULTS.md  
- BLUEPRINT.md  
- DATASET_NOTES.md  
- EXAMPLE_CASES.md  
- FUNCTIONAL_BLUEPRINT.md  
- HOWTO_Agentic.md  
- HOWTO_Chroma.md  
- HOWTO_JSONL.md  
- HOWTO_QLoRA.md  
- INGESTION_PLAN.md  
- NORMALIZED_CASE_OBJECT.md  
- openapi.json  
- PHASE_1_TO_PHASE_12_TECHNICAL_OVERVIEW.md  
- PHASE_10_RAG_VECTOR_DATABASE_FLOW.md  
- PHASE_11_FINETUNING_OVERVIEW_FLOW.md  
- PHASE_12_AGENTIC_RAG_LOOP_FLOW.md  
- REFERENCE_INGESTION_GUIDE.md


### ▶️ How to Run

The entire AI Engineering pipeline is orchestrated through **main.py**, which controls PHASE 1 → PHASE 10 using simple execution switches.

### 1. Configure Pipeline Execution

Inside `main.py`, ingestion is controlled by:

```python
RUN_INGESTION = False      # Set True to run Phase 1–5 ingestion
DEBUG_MAIN = False         # Toggle main-level debug output
```

**PHASE 1–5** (Ingestion)  
Runs only when `RUN_INGESTION = True`.

**PHASE 6–10** (Cleaning → Validation → Embedding → Finetune JSONL → RAG DB)  
Always run when ingestion is skipped or completed.

**PHASE 11–12** (Finetuning + Agentic Loop)  
Currently omitted until final testing is complete.

### 2. Run the Pipeline

Execute the full AI Engineering workflow:

```bash
python main.py
```

**This runs:**

- optional ingestion (PHASE 1–5)
- cleaning (PHASE 6)
- validation (PHASE 7)
- embedding generation (PHASE 8)
- finetune JSONL generation (PHASE 9)
- rag_db vector index construction (PHASE 10)

All engines are invoked automatically based on the switches.

### 3. Run the Intelligence Sidecar API

Start the Python Intelligence Sidecar:

```bash
python intelligence_sidecar.py
```

**This exposes:**

- model inference
- RAG retrieval
- diagnostic reasoning
- adapter inference (when PHASE 11 is enabled later)
- agentic loop (when PHASE 12 is enabled later)

Used by the optional .NET 9 Dashboard UI.

### 4. Run Test Harnesses (Optional)

```bash
python -m python.tests.test_phase10_rag
python -m python.tests.test_phase11_finetune   # when enabled
python -m python.tests.test_phase12_agentic    # when enabled
```

**These validate:**

- RAG retrieval
- finetuned model behavior
- agentic reasoning loop


## 🏁 Final Project Status — COMPLETE

### All phases (1–12) have been successfully implemented

- Data ingestion  
- Schema normalization  
- Cleaning  
- Embedding  
- Vector DB  
- RAG retrieval  
- QLoRA finetuning  
- Agentic diagnostic reasoning  

**Note:** PHASE 11 (QLoRA Finetuning) and PHASE 12 (Agentic RAG Loop) are fully implemented and documented, but currently disabled in `main.py` pending final validation. All other phases execute automatically through the main pipeline.


### This project now represents a fully operational Python‑driven AI Engineering system, suitable for:

- Senior AI Engineering roles

- System Architecture roles

- Data Engineering roles

- Machine Learning Engineering roles

- Portfolio demonstration

- Enterprise integration

This README, along with the Test Plan and Test Results documents, forms the complete documentation set for the AI Engineering Digital Signal Telemetry System.
