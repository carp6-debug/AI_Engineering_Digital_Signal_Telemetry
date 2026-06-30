# 📦 HOWTO — Chroma Vector DB Ingestion
### AI_Engineering_Digital_Signal_Telemetry  
### RAW Markdown Reference Guide

---

# 🎯 Purpose
Convert `embedding_cases.jsonl` into a **local vector database** for RAG.

---

# 🧱 Requirements

Install:

```
pip install chromadb sentence-transformers
```

---

# 🛠️ Step‑by‑Step Chroma Ingestion

## **1. Load SentenceTransformers**
```
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
```

## **2. Initialize Chroma**
```
import chromadb
client = chromadb.Client()
collection = client.get_or_create_collection("radio_cases")
```

## **3. Load embedding_cases.jsonl**
```
import json

entries = []
with open("embedding_cases.jsonl", "r") as f:
    for line in f:
        entries.append(json.loads(line))
```

## **4. Generate embeddings**
```
ids = []
docs = []
metas = []

for e in entries:
    ids.append(str(e["case_id"]))
    docs.append(e["embedding_text"])
    metas.append({"case_id": e["case_id"]})
```

## **5. Add to Chroma**
```
collection.add(
    ids=ids,
    documents=docs,
    metadatas=metas
)
```

---

# 🧪 Test Retrieval
```
query = "Why does my P25 radio show INVALID NAC?"
results = collection.query(query_texts=[query], n_results=3)
print(results)
```

---

# 🏁 Output
A persistent local vector DB containing all cases, ready for RAG.

