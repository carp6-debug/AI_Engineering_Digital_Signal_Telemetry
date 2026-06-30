# 📘 Phase 11 — Finetuning Overview (QLoRA + Mistral‑7B)
### AI_Engineering_Digital_Signal_Telemetry — Model Adaptation Phase

Phase 11 introduces **domain finetuning**, where a base language model is trained to understand the semantics, terminology, workflows, and diagnostic reasoning patterns of **Digital Radio Communications (DMR / P25 / NXDN)** troubleshooting.

This phase uses:

- **Mistral‑7B‑Instruct‑v0.2** as the base model  
- **QLoRA** for parameter‑efficient finetuning  
- **finetune_cases.jsonl** as supervised data  
- **rag_db** as the retrieval layer (unchanged)

The goal is to produce a model that understands *why* cases match, not just *what words* match.

---

## 1. Purpose of Finetuning

Finetuning teaches the model:

- RF propagation behavior  
- multipath fading  
- motion‑induced signal degradation  
- repeater timing issues  
- DMR/P25/NXDN protocol quirks  
- structured troubleshooting workflows  

After finetuning, the model can:

- interpret symptoms accurately  
- generate domain‑specific explanations  
- produce correct root‑cause reasoning  
- provide actionable resolution steps  
- understand context beyond word overlap  

This transforms the model into a **domain expert assistant**.

---

## 2. Input Dataset — finetune_cases.jsonl

Each line contains:

- **prompt**: Symptom + Context + ObservedSignals  
- **response**: RootCause + ResolutionSteps  

### **Example Structure**

```json
{
  "case_id": "001",
  "prompt": "Intermittent audio dropouts... mobile unit in motion...",
  "response": "Likely multipath fading... recommend antenna relocation..."
}
```

This dataset is used for **supervised finetuning**, not RAG.

---

## 3. Finetuning Method — QLoRA

QLoRA enables finetuning on consumer hardware by:

- freezing base model weights  
- injecting low‑rank adapters (LoRA layers)  
- training only the adapters  
- preserving the original model  
- producing a small, efficient finetuned checkpoint  

### **Benefits**
- low VRAM usage  
- fast training  
- minimal storage  
- high domain accuracy  

### **Output**
The final adapter is stored in:

```
models/finetune_engine_phase11/checkpoint-5/
    adapter_config.json
    adapter_model.safetensors
    training_args.bin
    trainer_state.json
    optimizer.pt
    scheduler.pt
    rng_state.pth
```

---

## 4. Training Flow

### **Step 1 — Load Base Model**
Mistral‑7B‑Instruct‑v0.2

### **Step 2 — Attach LoRA Adapters**
Adapters inserted into attention projection layers.

### **Step 3 — Train on finetune_cases.jsonl**
Model learns:

- symptom → root cause mapping  
- RF troubleshooting patterns  
- structured diagnostic reasoning  

### **Step 4 — Save Adapter Weights**
Only LoRA weights are saved.

### **Step 5 — Merge or Load at Inference**
At inference:

- load base model  
- load LoRA adapter from `checkpoint-5`  
- run domain‑specific reasoning  

---

## 5. Relationship to rag_db (Important)

Finetuning **does not modify** rag_db.

rag_db remains:

- MiniLM embeddings  
- Chroma vector store  
- cosine similarity search  

Finetuning affects:

- LLM reasoning  
- diagnostic accuracy  
- domain understanding  

RAG affects:

- retrieval quality  
- semantic similarity  
- case ranking  

Together they form:

**RAG (retrieval) + Finetuned LLM (reasoning)**

---

## 6. Before vs After Finetuning

### **Before Finetuning**
- MiniLM drives similarity  
- matches based on general semantics  
- model lacks RF engineering knowledge  
- reasoning is generic  

### **After Finetuning**
- model understands RF domain deeply  
- reasoning becomes structured and accurate  
- explanations reference correct protocol behavior  
- retrieval + reasoning becomes domain‑aligned  

### **Example**

Query:  
“audio dropouts when mobile unit is moving”

Before:  
“Case 1 is similar because words match.”

After:  
“Case 1 is similar because motion causes multipath fading in DMR Tier II environments.”

---

## 7. Output of Phase 11

The final deliverables are:

- **LoRA adapter weights**  
- **training metadata**  
- **checkpoint‑5 directory**  

This finetuned model is used in **Phase 12 Agentic RAG**, where retrieval + reasoning + action form a complete diagnostic loop.

---

## 8. Summary

Phase 11 transforms the system from:

- general semantic reasoning  
- to domain‑specific diagnostic expertise  

### **Key Points**
- Uses QLoRA for efficient finetuning  
- Uses finetune_cases.jsonl as supervised data  
- Produces LoRA adapters for Mistral‑7B  
- Does not modify rag_db  
- Greatly improves diagnostic accuracy  

This completes the finetuning stage of the AI_Engineering_Digital_Signal_Telemetry pipeline.









