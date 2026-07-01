# 📦 HOWTO — Chroma Vector DB Ingestion  
### AI_Engineering_Digital_Signal_Telemetry  
### RAW Markdown Reference Guide

---

# 🎯 Purpose
Convert `embedding_cases.jsonl` into a **local vector database** for RAG retrieval.

This is **PHASE 10**.

---

# 🧱 Requirements

Install:

```
pip install chromadb sentence-transformers
```

Artifacts required:

```
embedding_cases.jsonl
```

---

# 🛠️ Step-by-Step Chroma Ingestion

### **1. Load MiniLM Embedding Model**
```
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")
```

### **2. Initialize ChromaDB**
```
import chromadb

client = chromadb.PersistentClient(path="rag_db")
collection = client.get_or_create_collection("cases")
```

### **3. Load JSONL**
```
import json

records = []
with open("embedding_cases.jsonl", "r") as f:
    for line in f:
        records.append(json.loads(line))
```

### **4. Insert into Chroma**
```
for r in records:
    text = r["embedding_text"]
    emb = embedder.encode(text).tolist()

    collection.add(
        ids=[str(r["case_id"])],
        documents=[text],
        embeddings=[emb]
    )
```

---

# 🧪 Verify DB Contents
```
collection.count()
collection.peek()
```

---

# 🏁 Output
A persistent local vector database:

```
rag_db/
```

This database is consumed by **PHASE 12** during agentic troubleshooting.


