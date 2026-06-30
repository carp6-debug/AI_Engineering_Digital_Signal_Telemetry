"""
INGESTION MODULE — load_cases.py
PROJECT: AI_ENGINEERING_DIGITAL_SIGNAL_TELEMETRY
PURPOSE: Load raw JSON cases, validate required fields, normalize names,
         and prepare for cleaning and schema validation.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

# -------------------------------------------------------------------------
# PHASE 1 — Global constants available to all functions in this module
# -------------------------------------------------------------------------
REQUIRED = ["CaseId", "ProtocolFamily", "Symptom", "Context", "ObservedSignals"]
REQUIRED_SNAKE = ["case_id", "protocol_family", "symptom", "context", "observed_signals"]

print("# =====================================================================")
print("PHASE 1 - Global Constants Declarations")    
print(f"REQUIRED: {REQUIRED}")
print(f"REQUIRED_SNAKE: {REQUIRED_SNAKE}")
print("# =====================================================================")
print()

# -------------------------------------------------------------------------
# PHASE 1 — load_json_dataset(path)
# -------------------------------------------------------------------------
print("# =====================================================================")
print("PHASE 1 — LOAD JSON UTILITY")  
print("load_json_dataset(path)")    
print("# =====================================================================")
print()
def load_json_dataset(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# -------------------------------------------------------------------------
# PHASE 1 — save_json_dataset(path, data)
# -------------------------------------------------------------------------
print("# =====================================================================")
print("PHASE 1 — SAVE JSON UTILITY")  
print("save_json_dataset(path)")    
print("# =====================================================================")
print()
def save_json_dataset(path: Path, data: List[Dict[str, Any]]) -> None:
    """
    Save a list of case dictionaries to a JSON file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved JSON dataset to: {path}")


# -------------------------------------------------------------------------
# PHASE 2 — validate_required_fields(case)
# -------------------------------------------------------------------------
print("# =====================================================================")
print("PHASE 2 — REQUIRED FIELDS VALIDATION")  
print("validate_required_fields(case)")    
print("# =====================================================================")
print()
def validate_required_fields(case: Dict[str, Any]) -> bool:
    for key in REQUIRED:
        if key not in case:
            return False
    return True

# -------------------------------------------------------------------------
# PHASE 3 — normalize_field_names(case)
# -------------------------------------------------------------------------
print("# =====================================================================")
print("PHASE 3 — FIELD NAMES NORMALIZATION")  
print("normalize_field_names(case)")    
print("# =====================================================================")
print()
def normalize_field_names(case: Dict[str, Any]) -> Dict[str, Any]:
    new_case: Dict[str, Any] = {}

    for key, value in case.items():
        if key in REQUIRED_SNAKE:
            idx = REQUIRED_SNAKE.index(key)
            canonical = REQUIRED[idx]
            new_case[canonical] = value
        else:
            new_case[key] = value

    return new_case


# -------------------------------------------------------------------------
# PHASE 4 — save_raw_copy(cases, output_path)
# -------------------------------------------------------------------------
print("# =====================================================================")
print("PHASE 4 — SAVE CASES RAW COPY AS NORMALIZED")  
print("save_raw_copy(cases, output_path)") 
print("")  
print("# =====================================================================")
print()
def save_raw_copy(cases: List[Dict[str, Any]], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(cases, f, indent=4, ensure_ascii=False)


# -------------------------------------------------------------------------
# PHASE 5 (PHASE 1 - PHASE 4) — run_ingestion(input_path, output_path)
# -------------------------------------------------------------------------    
def run_ingestion(input_path: Path, output_path: Path) -> None:
    print("# =====================================================================")
    print("PHASE 5 - INGESTION - (PHASE 1 - PHASE 4)")
    print("PHASE 1 - Global Constants Declarations")
    print("PHASE 1 — LOAD JSON UTILITY")
    print("PHASE 1 — SAVE JSON UTILITY")
    print("PHASE 3 — FIELD NAMES NORMALIZATION")
    print("PHASE 4 — SAVE CASES RAW COPY AS NORMALIZED")  
    print('run_ingestion(input_path: Path, output_path: Path) -> None:')
    print("# =====================================================================")
    # Phase 1
    cases = load_json_dataset(input_path)

    # Phase 3 + Phase 2
    normalized_cases: List[Dict[str, Any]] = []
    for case in cases:
        norm = normalize_field_names(case)
        if validate_required_fields(norm):
            normalized_cases.append(norm)

    # Phase 4
    save_raw_copy(normalized_cases, output_path)
