# 🤖 HOWTO — Agentic Troubleshooting Loop  
### AI_Engineering_Digital_Signal_Telemetry  
### RAW Markdown Reference Guide

---

# 🎯 Purpose
Implement the **Agentic RAG Loop** that combines:

- **RAG retrieval** (ChromaDB + MiniLM)
- **Finetuned model reasoning** (QLoRA adapter from Phase 11)
- **Multi-step diagnostic workflows**

This is the **runtime engine** of the entire system.

---

# 🧱 Requirements

Install:

```
pip install transformers accelerate sentence-transformers chromadb peft
```

Artifacts required:

```
rag_db/                               ← from PHASE 10
models/finetune_engine_phase11/       ← from PHASE 11
mistralai/Mistral-7B-Instruct-v0.2    ← base model
```

---

# 🛠️ Agentic Loop Components

### **1. Load the RAG Vector DB**
```
import chromadb

client = chromadb.PersistentClient(path="rag_db")
collection = client.get_collection("cases")
```

### **2. Load the Finetuned Model + LoRA Adapter**
```
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base = "mistralai/Mistral-7B-Instruct-v0.2"

model = AutoModelForCausalLM.from_pretrained(base, load_in_4bit=True)
model = PeftModel.from_pretrained(model, "models/finetune_engine_phase11")

tokenizer = AutoTokenizer.from_pretrained(base)
```

### **3. RAG Retrieval Function**
```
def retrieve(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    return results["documents"]
```

### **4. Agentic Prompt Template**
```
def build_prompt(query, retrieved):
    context = "\n\n".join(retrieved)
    return f"""
### Diagnostic Query:
{query}

### Retrieved Context

