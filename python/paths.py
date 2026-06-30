# python/paths.py

from pathlib import Path

# Anchor: project root = parent of this file's directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Sub-roots for Python modules
CLEANING_ROOT = PROJECT_ROOT / "cleaning"
INGESTION_ROOT = PROJECT_ROOT / "ingestion"
SCHEMA_ROOT = PROJECT_ROOT / "schema"
EMBEDDING_ROOT = PROJECT_ROOT / "embedding"

# RAG engine (Python code)
RAG_ENGINE_ROOT = PROJECT_ROOT / "rag_engine"

# Agentic engine (Phase 12 Python code)
AGENTIC_ENGINE_ROOT = PROJECT_ROOT / "agentic_engine"

# Vector DB root (Phase 10 output)
RAG_DB_ROOT = PROJECT_ROOT / "rag_db"             # Chroma DB lives here

# Data root
DATA_ROOT = PROJECT_ROOT / "data"

# Phase 1–5 input/output
RAW_DATA = DATA_ROOT / "raw"              # cases_raw.json + cases_normalized.json

# Phase 6 output
CLEANED_DATA = DATA_ROOT / "processed"    # cases_clean.json

# Phase 7 output
VALIDATED_DATA = DATA_ROOT / "validated"  # validated_cases.json

# Phase 8 output
EMBEDDING_DATA = DATA_ROOT / "embedding"

# Phase 11 finetune adapter output
FINETUNE_MODEL_ROOT = PROJECT_ROOT / "models" / "finetune_engine_phase11"







