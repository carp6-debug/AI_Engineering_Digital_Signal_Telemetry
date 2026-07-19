# test_retrieval.py
# Phase 10 Retrieval Sanity Test using paths.py

import os
os.environ["HF_HUB_DISABLE_RESUME_DOWNLOAD"] = "1"

# Disable for hugging face wrapper fetch
#ChromaDB 0.5+ requires an embedding function wrapper that:
#Accepts a list of strings, Returns a list of vectors,Uses .tolist(),
# Accepts a list of strings, Avoids numpy type confusion
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.api.types import EmbeddingFunction
from typing import List
import numpy as np

# FIXED IMPORT — correct when script is inside python/
import paths
RAG_DB_ROOT = paths.RAG_DB_ROOT


# ------------------------------------------------------------
# Embedding function wrapper (Chroma 0.5+ compliant)
# ------------------------------------------------------------
class MiniLMEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            cache_folder="C:/Users/carp6/.cache/huggingface",
            use_auth_token=False
        )

    def __call__(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []

        embeddings = np.asarray(self.model.encode(texts))
        return embeddings.tolist()


# Instantiate embedding function
embedding_fn = MiniLMEmbeddingFunction()

# ------------------------------------------------------------
# Connect to Chroma DB
# ------------------------------------------------------------
print(f"Connecting to Chroma at: {RAG_DB_ROOT}")
client = chromadb.PersistentClient(path=str(RAG_DB_ROOT))

try:
    collection = client.get_collection(name="radio_cases")
    print("Connected. Collection loaded:", collection.name)
except Exception as e:
    print("ERROR: Could not load collection 'radio_cases'")
    print("Exception:", e)
    raise SystemExit(1)

# ------------------------------------------------------------
# Query
# ------------------------------------------------------------
query = "audio dropouts when mobile unit is moving"
print("\nQuery:", query)

results = collection.query(
    query_texts=[query],
    n_results=3
)

# ------------------------------------------------------------
# Safe extraction of results
# ------------------------------------------------------------
ids_list = results.get("ids") or [[]]
dist_list = results.get("distances") or [[]]

ids = ids_list[0] if ids_list else []
distances = dist_list[0] if dist_list else []

# ------------------------------------------------------------
# Display results
# ------------------------------------------------------------
print("\nTop Matches:")
for idx, (doc_id, distance) in enumerate(zip(ids, distances), start=1):
    similarity = 1 - distance
    print(f"{idx}. CaseId: {str(doc_id)}  |  Similarity Score: {similarity:.4f}")

print("\nRetrieval test complete.")




