# 📘 HOWTO — JSONL Formats for RAG, Finetuning, and Agentic Systems  
### AI_Engineering_Digital_Signal_Telemetry  
### RAW Markdown Reference Guide

---

# 🎯 Purpose
Define the three JSONL formats used across:

- **PHASE 10** — RAG Vector DB  
- **PHASE 11** — QLoRA Finetuning  
- **PHASE 12** — Agentic Troubleshooting  

---

# 🧩 1. embedding_cases.jsonl (RAG)

### **Used in PHASE 10**

Format:
```
{"case_id": 1.0, "embedding_text": "CaseId: 1.0\nProtocolFamily: ..."}
```

Purpose:

- Dense semantic embedding  
- Stored in Chroma  
- Retrieved during agentic reasoning  

---

# 🧩 2. finetune_cases.jsonl (QLoRA)

### **Used in PHASE 11**

Format:
```
{
  "case_id": 1.0,
  "prompt": "CaseId: 1.0\nProtocolFamily: ...",
  "response": "RootCause: ...\nResolutionSteps: ..."
}
```

Purpose:

- Teaches the model domain reasoning  
- Produces LoRA adapter  
- Consumed by PHASE 12  

---

# 🧩 3. agentic_cases.jsonl (Optional)

### **Used in PHASE 12 (Extended)**

Format:
```
{
  "query": "Radio drops audio intermittently.",
  "expected_context": ["CaseId: 1.0 ...", "CaseId: 4.0 ..."]
}
```

Purpose:

- Optional agentic test harness  
- Validates multi-step reasoning  
- Ensures grounded responses  

---

# 🏁 Summary

### **PHASE 10 → embedding_cases.jsonl**  
### **PHASE 11 → finetune_cases.jsonl**  
### **PHASE 12 → agentic_cases.jsonl (optional)**

These formats complete the **data substrate** for the entire AI diagnostic pipeline.

