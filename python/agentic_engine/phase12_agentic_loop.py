# agentic_engine/phase12_agentic_loop.py
"""
PHASE 12 — Agentic RAG Loop
AI_Engineering_Digital_Signal_Telemetry

This module loads the frozen Mistral‑7B model, merges the Phase 11 LoRA
adapter, loads the rag_db vector database, retrieves relevant cases, builds
a structured agentic troubleshooting prompt, and generates a grounded answer.

Function Summary
----------------
load_model_and_adapter():
    Loads base model and merges LoRA adapter for domain-specific reasoning.

load_tokenizer():
    Loads tokenizer used during finetuning for consistent inference.

load_rag_db():
    Initializes ChromaDB and loads the “cases” collection for retrieval.

retrieve(query):
    Embeds the user query and returns top-N relevant documents from rag_db.

build_prompt(query, retrieved_docs):
    Constructs agentic troubleshooting prompt using query + RAG context.

agentic_answer(query):
    Runs full agentic loop: retrieval → prompt → inference → decoded answer.
"""

import torch
import chromadb
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
from peft import PeftModel
from python.paths import (
    RAG_DB_ROOT,
    FINETUNE_MODEL_ROOT,
    PROJECT_ROOT
)

def run_phase12_agentic(query: str):
    print("\n=== PHASE 12 — Agentic RAG Loop ===")

    # ------------------------------------------------------------
    # Load RAG DB (Phase 10 output)
    # ------------------------------------------------------------
    client = chromadb.PersistentClient(path=str(RAG_DB_ROOT))

    collection = client.get_collection("radio_cases")

    # ------------------------------------------------------------
    # Embed query
    # ------------------------------------------------------------
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    q_embed = embedder.encode(query).tolist()

    rag = collection.query(query_embeddings=[q_embed], n_results=3)
    ctx = "\n".join(rag["documents"][0])

    # ------------------------------------------------------------
    # Load base model + LoRA adapter (Phase 11 output)
    # ------------------------------------------------------------
    BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16
    ).to("cuda")

    adapter_dir = FINETUNE_MODEL_ROOT / "checkpoint-5"

    model = PeftModel.from_pretrained(
    base,
    str(adapter_dir.resolve()),
    is_local=True
    )

    model = model.merge_and_unload()

    # ------------------------------------------------------------
    # Agentic loop prompt
    # ------------------------------------------------------------
    prompt = (
        f"<s>[USER]\n{query}\n"
        f"Context:\n{ctx}\n"
        f"Provide diagnostic reasoning and next actions.\n"
        f"[/USER]\n[ASSISTANT]\n"
    )

    inp = tok(prompt, return_tensors="pt").to("cuda")

    out = model.generate(
        **inp,
        max_new_tokens=300,
        temperature=0.2
    )

    ans = tok.decode(out[0], skip_special_tokens=True)

    print(ans)
    print("\nPHASE 12 COMPLETE.")


