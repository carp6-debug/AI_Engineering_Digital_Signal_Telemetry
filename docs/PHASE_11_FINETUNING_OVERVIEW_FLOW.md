# 📘 Phase 11 — Finetuning Overview (QLoRA + Llama 3B/8B)
### AI_Engineering_Digital_Signal_Telemetry — Model Adaptation Phase  
### RAW Markdown — Single Fenced Block

# 🧭 Purpose

Phase 11 performs **QLoRA finetuning** on the Llama 3B or 8B base model using domain‑specific troubleshooting cases.  
**QLoRA (Quantized Low‑Rank Adaptation)** applies low‑rank adapter layers to a 4‑bit quantized model, enabling high‑quality finetuning on local hardware with significantly reduced VRAM requirements.

This phase loads the finetuning dataset, tokenizes prompt/response pairs, initializes the frozen base model, injects LoRA adapters, and trains only the adapter weights. The result is a specialized model capable of expert‑level reasoning in DMR, P25, and NXDN radio diagnostics.

# 🧱 Inputs

- `finetune_cases.jsonl`  
  Generated in Phase 9  
  Contains validated instruction‑response pairs.

- **Base Model**  
  - `Llama‑3B‑Instruct` (local)  
  - `Llama‑8B‑Instruct` (local)

# 🗂️ Output

- `models/finetune_engine_phase11/`  
  Contains:
  - QLoRA adapter weights  
  - tokenizer  
  - training configuration  
  - merged model (optional)

# ⚙️ Components

### **run_phase11_finetune()**
Primary entry point for Phase 11.  
Responsible for:

- loading `finetune_cases.jsonl`  
- formatting each example into a chat‑style training sample  
- tokenizing inputs and labels  
- initializing the frozen Llama model  
- applying LoRA configuration  
- training adapter weights with QLoRA  
- writing adapter checkpoints to disk

### **format_example(example)**
Converts each troubleshooting case into a structured prompt/response pair suitable for supervised finetuning.  
Produces tokenized tensors for:

- model input  
- training labels  
- attention masks  

### **AutoTokenizer.from_pretrained()**
Loads the tokenizer for the selected base model.  
Sets:

- `pad_token = eos_token`  
  Ensures safe batching and prevents misalignment during supervised training.

### **AutoModelForCausalLM.from_pretrained()**
Loads the **frozen** Llama‑3B or Llama‑8B model.  
Only LoRA adapter weights are trainable; the base model remains unchanged.

### **LoraConfig()**
Defines LoRA adapter parameters:

- rank  
- alpha  
- dropout  
- target modules (e.g., attention projections)

These parameters determine how low‑rank updates are applied to the quantized model.

### **get_peft_model()**
Injects LoRA adapter layers into the frozen base model.  
This produces the **PEFT‑enabled** model used for QLoRA training.

### **TrainingArguments()**
Configures training hyperparameters:

- batch size  
- learning rate  
- number of epochs  
- save steps  
- logging frequency  
- gradient checkpointing  

### **Trainer()**
Runs the QLoRA training loop.  
Handles:

- forward/backward passes  
- gradient accumulation  
- adapter weight updates  
- checkpoint saving  

Adapter weights are written to disk and later consumed by the Python sidecar and Dashboard UI.

# 🔧 Training Characteristics

- **QLoRA adapters** dramatically reduce VRAM requirements  
- **Low‑rank updates** preserve base model stability  
- **Frozen base model** ensures predictable behavior  
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

