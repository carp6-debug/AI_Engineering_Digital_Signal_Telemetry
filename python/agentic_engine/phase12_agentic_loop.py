# agentic_engine/phase12_agentic_loop.py
"""
PHASE 12 — Agentic RAG Loop
AI_Engineering_Digital_Signal_Telemetry

Basic standalone script:
- Direct model folder names
- Direct adapter paths
- RAG retrieval
- Agentic reasoning
- CPU-only execution
"""

# ---------------------------------------------------------------------------
# STANDARD LIBRARY IMPORTS
# ---------------------------------------------------------------------------
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# THIRD-PARTY IMPORTS
# ---------------------------------------------------------------------------
import torch
import chromadb
from chromadb.config import Settings

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# PYTHON PACKAGE ROOT / PATHS
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from python.paths import PROJECT_ROOT, RAG_DB_ROOT

# ---------------------------------------------------------------------------
# CPU-ONLY GLOBALS
# ---------------------------------------------------------------------------
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TRANSFORMERS_NO_CUDA"] = "1"
torch.cuda.is_available = lambda: False
torch.backends.mps.is_available = lambda: False

DEVICE = "cpu"

# ---------------------------------------------------------------------------
# SIMPLE MODEL SELECTOR (NO COLLISIONS)
# ---------------------------------------------------------------------------

MODEL_SELECT = "3B"      # options: "3B", "8B", "PHI3"

if MODEL_SELECT == "3B":
    SELECTED_MODEL = "llama-3.2-3b"
    SELECTED_ADAPTER = (
        PROJECT_ROOT / "models" / "finetune_engine_phase11_llama_3_2_3b" / "checkpoint-5"
    )

elif MODEL_SELECT == "8B":
    SELECTED_MODEL = "llama-3.1-8b-instruct"
    SELECTED_ADAPTER = (
        PROJECT_ROOT / "models" / "finetune_engine_phase11_llama_3_1_8b" / "checkpoint-8"
    )

elif MODEL_SELECT == "PHI3":
    SELECTED_MODEL = "phi3-mini"
    SELECTED_ADAPTER = None

else:
    raise ValueError(f"Unknown MODEL_SELECT value: {MODEL_SELECT}")


# ---------------------------------------------------------------------------
# MODEL LOADER (MINIMAL)
# ---------------------------------------------------------------------------
def load_model_and_adapter(model_name: str, adapter_path: str | None):
    model_path = PROJECT_ROOT / "models" / model_name
    print(f"[MODEL] Loading: {model_path}")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="cpu",
        dtype=torch.float32,
    )

    if adapter_path:
        print(f"[ADAPTER] Loading LoRA adapter: {adapter_path}")
        model = PeftModel.from_pretrained(
            model,
            adapter_path,
            device_map="cpu",
        )
        model = model.merge_and_unload()
    else:
        print("[ADAPTER] No adapter loaded.")

    model.eval()
    return tokenizer, model

# ---------------------------------------------------------------------------
# RAG RETRIEVAL
# ---------------------------------------------------------------------------
def run_rag_retrieval(query: str):
    print("\n[RAG] Loading ChromaDB...")

    client = chromadb.PersistentClient(
        path=str(RAG_DB_ROOT),
        settings=Settings(anonymized_telemetry=False),
    )

    collection = client.get_collection("radio_cases")

    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    q_embed = embedder.encode(query).tolist()

    rag = collection.query(query_embeddings=[q_embed], n_results=3)

    docs = rag["documents"][0]
    ids = rag["ids"][0]

    context = []
    for i in range(len(docs)):
        context.append(f"- Case {ids[i]}: {docs[i]}")

    return "\n".join(context)

# ---------------------------------------------------------------------------
# AGENTIC PROMPT
# ---------------------------------------------------------------------------
def build_agentic_prompt(query: str, rag_context: str):
    return (
        "You are a senior digital radio diagnostics engineer.\n"
        "Use the telemetry context and user prompt to perform a multi-step diagnostic reasoning process.\n\n"
        "Telemetry Context:\n"
        f"{rag_context}\n\n"
        "User Prompt:\n"
        f"{query}\n\n"
        "Format:\n"
        "Step 1: <description>\n"
        "Evidence: <evidence>\n"
        "Intermediate conclusion: <conclusion>\n"
        "Step 2: ...\n"
        "Final diagnosis: <diagnosis>\n"
        "Confidence: <0.0-1.0>\n"
    )

# ---------------------------------------------------------------------------
# MAIN PHASE 12 LOOP
# ---------------------------------------------------------------------------
def run_phase12_agentic(query: str):
    print("\n=== PHASE 12 — Agentic RAG Loop ===")

    # RAG
    rag_context = run_rag_retrieval(query)
    print("\n[RAG] Retrieved Context:")
    print(rag_context)

    # MODEL
    tokenizer, model = load_model_and_adapter(
        SELECTED_MODEL,
        str(SELECTED_ADAPTER) if SELECTED_ADAPTER else None
    )

    # PROMPT
    prompt = build_agentic_prompt(query, rag_context)
    print("\n[AGENTIC] Running agentic reasoning...")

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
    ).to(DEVICE)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.2,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    generated = output[0][inputs["input_ids"].shape[1]:]
    answer = tokenizer.decode(generated, skip_special_tokens=True)

    print("\n=== AGENTIC RESULT ===")
    print(answer)
    print("\nPHASE 12 COMPLETE.\n")







