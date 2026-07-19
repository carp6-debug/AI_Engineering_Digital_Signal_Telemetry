# =====================================================================
# AI_Engineering_Digital_Signal_Telemetry — EXECUTION CONTROL PANEL
# =====================================================================

from pathlib import Path

from paths import RAW_DATA, CLEANED_DATA, VALIDATED_DATA, EMBEDDING_DATA, RAG_DB_ROOT
from ingestion.load_cases import run_ingestion, load_json_dataset,save_json_dataset
from cleaning.clean_cases import clean_case
from schema.case_schema import CASE_SCHEMA, validate_case_schema
from embedding.embedding_builder import run_embedding
from rag_engine.vector_ingestion import run_phase_vector_ingestion

# ---------------------------------------------------------------------
# EXECUTION SWITCHES
# ---------------------------------------------------------------------
RUN_INGESTION = False      # Set to False to skip Phase 1–5
DEBUG_MAIN = False         # Toggle main-level debug output

print("====================================================================")
print("AI ENGINEERING — PYTHON TIER EXECUTION CONTROL")
print("====================================================================")
print("Set RUN_INGESTION to [False] to skip Phase 1–5")
print("OR delete data files and set RUN_INGESTION to [True] to rebuild pipeline.")
print("--------------------------------------------------------------------")
print(f"DO NOT DELETE baseline RAW file: {RAW_DATA / 'cases_raw.json'}")
print(f"DELETE to rebuild: {RAW_DATA / 'cases_normalized.json'}")
print(f"DELETE to rebuild: {CLEANED_DATA / 'cases_clean.json'}")
print(f"DELETE to rebuild: {VALIDATED_DATA / 'validated_cases.json'}")
print("--------------------------------------------------------------------")
print(f"RUN_INGESTION = {RUN_INGESTION}")
print(f"DEBUG_MAIN    = {DEBUG_MAIN}")
print("====================================================================")

# ---------------------------------------------------------------------
# FILE STATUS REPORTING
# ---------------------------------------------------------------------
def report_file_status(label, path: Path):
    print(f"\n[FILE CHECK] {label}")
    if not path.exists():
        print(f"  - Status: DOES NOT EXIST")
        return
    size = path.stat().st_size
    if size == 0:
        print(f"  - Status: EXISTS but EMPTY")
    else:
        print(f"  - Status: EXISTS and NOT EMPTY ({size} bytes)")
    print(f"  - Path: {path}")

print("\n================ FILE STATUS SUMMARY ================")
report_file_status("RAW: cases_raw.json", RAW_DATA / "cases_raw.json")
report_file_status("RAW: cases_normalized.json", RAW_DATA / "cases_normalized.json")
report_file_status("PROCESSED: cases_clean.json", CLEANED_DATA / "cases_clean.json")
report_file_status("VALIDATED: validated_cases.json", VALIDATED_DATA / "validated_cases.json")
print("=====================================================\n")

# ---------------------------------------------------------------------
# DEBUG PRINT WRAPPER
# ---------------------------------------------------------------------
def debug(msg: str):
    if DEBUG_MAIN:
        print(f"[MAIN DEBUG] {msg}")

# =====================================================================
# MAIN EXECUTION ENTRY POINT
# =====================================================================
def main():

    print("# =====================================================================")
    print("PHASE 1 - PHASE 5 INGESTION")
    print("# =====================================================================")

if RUN_INGESTION:
    debug("Running Phase 1–5 ingestion pipeline...")
    run_ingestion(
        RAW_DATA / "cases_raw.json",
        RAW_DATA / "cases_normalized.json"
    )
    debug("Ingestion complete.\n")
else:
    # Always show this message, even when DEBUG_MAIN = False
    print("Skipping ingestion (RUN_INGESTION = False).\n")


    print("# =====================================================================")
    print("\nPHASE 6 - CLEANING")
    print("# =====================================================================")
    print("PHASE 6 — FUNCTION: clean_case(case)")
    debug("Loading normalized dataset...")

    cases = load_json_dataset(RAW_DATA / "cases_normalized.json")
    print("Cases loaded:", len(cases))

    cleaned_cases = []

    for idx, case in enumerate(cases, start=1):
        print(f"\n--- Cleaning Case {idx} (CaseId: {case.get('CaseId')}) ---")
        cleaned = clean_case(case)
        cleaned_cases.append(cleaned)

    print("\nAll cases cleaned.")

    # Save cleaned cases
    save_json_dataset(CLEANED_DATA / "cases_clean.json", cleaned_cases)

    # ---------------------------------------------------------------------
    # Phase 7 — Schema Validation
    # ---------------------------------------------------------------------
    print("# =====================================================================")
    print("\nPHASE 7 — SCHEMA VALIDATION")
    print("# =====================================================================")

    validated_cases = []

    for idx, case in enumerate(cleaned_cases, start=1):
        case_id = case.get("CaseId")
        print(f"\n--- Validating Case {idx} (CaseId: {case_id}) ---")

        is_valid = validate_case_schema(case, CASE_SCHEMA)

        if is_valid:
            print(f"✅ Case {idx} (CaseId: {case_id}) PASSED schema validation.")
            validated_cases.append(case)
        else:
            print(f"❌ Case {idx} (CaseId: {case_id}) FAILED schema validation.")

    print(f"\nSchema validation complete. Valid cases: {len(validated_cases)} / {len(cleaned_cases)}")

    # Save validated cases
    save_json_dataset(VALIDATED_DATA / "validated_cases.json", validated_cases)

    print("# =====================================================================")
    print("PHASE 8 — EMBEDDING TEXT CONSTRUCTION")
    print("# =====================================================================")  

    EMBED_DEBUG = False  # toggle Phase 8 verbose output

    run_embedding(
        VALIDATED_DATA / "validated_cases.json",
        VALIDATED_DATA / "embedding_cases.jsonl",
        DEBUG_EMBED=EMBED_DEBUG
    )

    from embedding.finetune_builder import run_phase_9_finetune

    print("# =====================================================================")
    print("PHASE 9 — FINETUNING JSONL CONSTRUCTION")
    print("# =====================================================================")

    FINETUNE_DEBUG = False  # toggle Phase 9 verbose output

    run_phase_9_finetune(
        VALIDATED_DATA / "validated_cases.json",
        EMBEDDING_DATA / "finetune_cases.jsonl",
        DEBUG_FINETUNE=FINETUNE_DEBUG
    )
    
    print("# =====================================================================")
    print("PHASE 10 — VECTOR DB INGESTION (RAG INDEX BUILD)")
    print("# =====================================================================")

    run_phase_vector_ingestion(
    embedding_path=VALIDATED_DATA / "embedding_cases.jsonl",
    db_root=RAG_DB_ROOT,
    collection_name="radio_cases",
    DEBUG_RAG=False
    )

    print("# =====================================================================")
    print("PHASE 11 — QLoRA FINETUNING ENGINE")
    print("# =====================================================================")
"""
    from finetune_engine.phase11_qlora import run_phase11_finetune

    print("PHASE 11 — FUNCTION: run_phase11_finetune()")
    print("Using finetune_cases.jsonl from Phase 9...")

    run_phase11_finetune()

    print("\nPHASE 11 COMPLETE — Finetuned model saved to models/finetune_engine_phase11")

    # main.py (Phase 12 block)

print("# =====================================================================")
print("PHASE 12 — AGENTIC RAG LOOP")
print("# =====================================================================")

from agentic_engine.phase12_agentic_loop import run_phase12_agentic

test_q = "DMR radio audio dropouts while mobile — diagnose."
run_phase12_agentic(test_q)
"""


if __name__ == "__main__":
    main()



