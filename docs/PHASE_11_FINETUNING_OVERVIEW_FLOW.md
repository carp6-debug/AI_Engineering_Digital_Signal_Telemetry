# 📘 Phase 11 — Finetuning Overview (QLoRA + Llama 3B/8B)
### AI_Engineering_Digital_Signal_Telemetry — Model Adaptation Phase  
### RAW Markdown — Single Fenced Block

# 🧭 Purpose

Phase 11 performs **QLoRA finetuning** on the Llama 3B or 8B base model using domain‑specific troubleshooting cases.  
**QLoRA (Quantized Low‑Rank Adaptation)** is a memory‑efficient finetuning method that applies low‑rank updates to a 4‑bit quantized model, enabling high‑quality training on local hardware with significantly reduced VRAM requirements.

The result is a specialized model capable of expert‑level reasoning in DMR, P25, and NXDN radio diagnostics.

# 🧱 Inputs

- `finetune_cases.jsonl`  
  Generated in Phase 9  
  Contains instruction‑response pairs derived from validated cases.

- **Base Model**  
  - `Llama-3B-Instruct` (local)  
  - `Llama-8B-Instruct` (local)

# 🗂️ Output

- `models/finetune_engine_phase11/`  
  Contains:
  - QLoRA adapter weights  
  - tokenizer  
  - training configuration  
  - merged model (optional)

# ⚙️ Components

### **run_phase11_finetune()**
Responsible for:

- loading the base model  
- applying QLoRA configuration  
- training on `finetune_cases.jsonl`  
- saving adapter weights  
- validating loss curves  
- exporting the final finetuned model

# 🔧 Training Characteristics

- **QLoRA adapters** reduce VRAM requirements  
- **Low‑rank updates** preserve base model stability  
- **Domain‑specific reasoning** improves:
  - symptom interpretation  
  - RF propagation logic  
  - BER/SNR/RSSI analysis  
  - protocol‑specific troubleshooting  

# 🧠 Model Behavior After Finetuning

The finetuned model becomes:

- more deterministic  
- more domain‑aware  
- more accurate in multi‑step reasoning  
- better aligned with RAG retrieval context  

It is used directly by:

- Python sidecar  
- Dashboard UI  
- Agentic Loop (Phase 12)

# 🧩 Summary

Phase 11 produces the **domain‑specialized Llama model** that powers the entire diagnostic workflow.  
It is one of the core reusable components when switching models or refreshing the Agentic Loop.
