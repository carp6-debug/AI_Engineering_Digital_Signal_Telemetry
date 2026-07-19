"""
PHASE 10 — VECTOR DB INGESTION
Builds a local vector index from embedding_cases.jsonl.
"""

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings


def debug_rag(msg, DEBUG_RAG):
    if DEBUG_RAG:
        print(f"[PHASE 10 DEBUG] {msg}")


def run_phase_vector_ingestion(
    embedding_path,
    db_root,
    collection_name="radio_cases",
    DEBUG_RAG=False
):
    print("# =====================================================================")
    print("PHASE 10 — VECTOR DB INGESTION (RAG INDEX BUILD)")
    print("# =====================================================================")

    embedding_path = Path(embedding_path)
    db_root = Path(db_root)

    if not embedding_path.exists():
        print(f"❌ ERROR: embedding_cases.jsonl not found at: {embedding_path}")
        return

    # Load local embedding model
    print("Loading SentenceTransformer model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Initialize Chroma
    print(f"Initializing Chroma at: {db_root}")

    client = chromadb.PersistentClient(path=str(db_root))

    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )

    print(f"Using Chroma collection: {collection_name}")
    print("Ingesting embeddings...\n")

    with open(embedding_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            entry = json.loads(line)

            # REQUIRED FIELDS FROM embedding_cases.jsonl
            case_id = str(entry["case_id"])
            text = entry["embedding_text"]

            # NEW: Extract metadata fields
            protocol = entry.get("protocolFamily", "Unknown")
            symptom = entry.get("symptom", "Unknown")

            context = entry.get("context", {})
            environment = context.get("environment", "Unknown")
            hardware = context.get("hardware", "Unknown")

            debug_rag(f"Embedding case_id={case_id}", DEBUG_RAG)

            vector = model.encode(text).tolist()

            # NEW: Store full metadata
            metadata = {
                "case_id": case_id,
                "protocolFamily": protocol,
                "symptom": symptom,
                "environment": environment,
                "hardware": hardware
            }

            collection.add(
                ids=[case_id],
                documents=[text],
                metadatas=[metadata],
                embeddings=[vector]
            )

    print("\nPHASE 10 COMPLETE — Vector DB populated.")
    print(f"Persisted at: {db_root}")
    print("# =====================================================================")


