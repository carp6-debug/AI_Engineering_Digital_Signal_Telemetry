# 📘 Phase 10 — Local RAG Vector Database Workflow (MiniLM + Chroma)
### AI_Engineering_Digital_Signal_Telemetry — RAG Architecture Overview

This document describes the complete workflow for building and querying the **local RAG vector database**, using:

- **SentenceTransformers MiniLM** — embedding engine  
- **ChromaDB** — persistent local vector database  
- **rag_db/** — on‑disk vector store  
- **test_retrieval.py** — query + similarity search harness  

This phase establishes the retrieval foundation used by Phase 12’s Agentic RAG Loop.

---

## 1. Phase 10 — Vector Write Operation (Building rag_db)

### **Input**
`embedding_cases.jsonl`  
Each entry contains the full case text:

- Symptom  
- Context  
- ObservedSignals  
- RootCause  
- ResolutionSteps  

### **Process**
1. Load each case’s text.  
2. Convert text → vector using MiniLM (`all-MiniLM-L6-v2`).  
3. Store the vector in a persistent Chroma collection:

```
rag_db/
└── radio_cases
```

### **Code Concept**

```python
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode(case_text)

collection.add(
    documents=[case_text],
    embeddings=[embedding],
    ids=[case_id]
)
```

### **Result**
A persistent local vector database containing:

- CaseId  
- Original text  
- Embedding vector  

This completes the **write** phase.

---

## 2. test_retrieval.py — Vector Read Operation (Querying rag_db)

### **Input**
Plain text query:

```
audio dropouts when mobile unit is moving
```

### **Process**
1. Chroma receives the query text.  
2. Chroma embeds the query using MiniLM.  
3. Chroma compares the query vector to stored case vectors.  
4. Chroma computes cosine similarity.  
5. Chroma returns the closest matches.

### **Code Concept**

```python
results = collection.query(
    query_texts=[query],
    n_results=3
)
```

### **Example Result**

```
Top Matches:
1. CaseId: 1.0  |  Similarity Score: 0.4576
2. CaseId: 5.0  |  Similarity Score: 0.3744
3. CaseId: 2.0  |  Similarity Score: 0.2710
```

These scores represent **semantic similarity**, not probability.

---

## 3. Meaning of Similarity Scores

Cosine similarity measures how close two vectors are:

- **1.0** → identical meaning  
- **0.0** → unrelated  
- **negative** → opposite meaning (rare for embeddings)

Example:

**Case 1 Symptom**  
“Intermittent audio dropouts… mobile unit… in motion.”

**Query**  
“audio dropouts when mobile unit is moving”

Strong semantic overlap → highest similarity score.

---

## 4. Summary of the Entire RAG Flow

### **Write (Phase 10)**  
case text → MiniLM → case vector → rag_db

### **Read (test_retrieval.py)**  
query text → MiniLM → query vector → compare → top matches

### **Output**  
A ranked list of cases based on semantic similarity.

---

## 5. Key Points

- MiniLM is used for both writing and reading.  
- Chroma stores vectors locally in `rag_db`.  
- Queries are embedded automatically.  
- Similarity scores reflect semantic closeness.  
- A score of 1.0 is a perfect vector match.

This completes the **local RAG pipeline** for vector search.

---




