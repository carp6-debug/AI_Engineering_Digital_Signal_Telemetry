"""
PHASE 8 — EMBEDDING TEXT CONSTRUCTION
Builds AI‑optimized embedding strings from validated case objects.
"""

import json
from pathlib import Path

def debug_embed(msg, DEBUG_EMBED):
    if DEBUG_EMBED:
        print(f"[PHASE 8 DEBUG] {msg}")


def build_embedding_text(case, DEBUG_EMBED=False):
    print("\n------------------------------------------------------------")
    print(f"PHASE 8 — BUILDING EMBEDDING TEXT FOR CASE {case.get('CaseId')}")
    print("------------------------------------------------------------")

    debug_embed(f"Validated Case Object:\n{json.dumps(case, indent=4)}", DEBUG_EMBED)

    embedding_lines = []

    # REQUIRED FIELDS
    embedding_lines.append(f"CaseId: {case.get('CaseId')}")
    embedding_lines.append(f"ProtocolFamily: {case.get('ProtocolFamily')}")
    embedding_lines.append(f"Symptom: {case.get('Symptom')}")
    embedding_lines.append(f"RootCause: {case.get('RootCause')}")
    embedding_lines.append(f"Notes: {case.get('Notes')}")

    # CONTEXT BLOCK
    ctx = case.get("Context", {})
    embedding_lines.append("Context:")
    embedding_lines.append(f"  Environment: {ctx.get('Environment')}")
    embedding_lines.append(f"  Hardware: {ctx.get('Hardware')}")
    embedding_lines.append(f"  Configuration: {ctx.get('Configuration')}")

    # OBSERVED SIGNALS BLOCK
    sig = case.get("ObservedSignals", {})
    embedding_lines.append("ObservedSignals:")
    for key, value in sig.items():
        embedding_lines.append(f"  {key}: {value}")

    # RESOLUTION STEPS
    embedding_lines.append("ResolutionSteps:")
    for step in case.get("ResolutionSteps", []):
        embedding_lines.append(f"  - {step}")

    embedding_text = "\n".join(embedding_lines)

    debug_embed("FINAL EMBEDDING TEXT:", DEBUG_EMBED)
    debug_embed(embedding_text, DEBUG_EMBED)

    return embedding_text


def run_embedding(input_path, output_path, DEBUG_EMBED=False):
    print("# =====================================================================")
    print("PHASE 8 — EMBEDDING TEXT CONSTRUCTION")
    print("run_embedding(input_path, output_path, DEBUG_EMBED=False):")
    print("# =====================================================================")

    print(f"Loading validated cases from: {input_path}")

    if not Path(input_path).exists():
        print(f"❌ ERROR: Validated cases file does not exist: {input_path}")
        return

    with open(input_path, "r") as f:
        cases = json.load(f)

    print(f"Loaded {len(cases)} validated cases.")
    print("Building embedding text for each case...\n")

    with open(output_path, "w") as out:
        for case in cases:
            embedding_text = build_embedding_text(case, DEBUG_EMBED)

            # NEW — Extract metadata for PHASE 10 (matching validated_cases.json EXACTLY)
            ctx = case.get("Context", {})

            jsonl_entry = {
                "case_id": case.get("CaseId"),
                "protocolFamily": case.get("ProtocolFamily"),
                "symptom": case.get("Symptom"),
                "context": {
                    "environment": ctx.get("Environment"),
                    "hardware": ctx.get("Hardware")
                },
                "embedding_text": embedding_text
            }

            out.write(json.dumps(jsonl_entry) + "\n")

    print(f"\nPHASE 8 COMPLETE — Embedding JSONL written to:")
    print(f"{output_path}")
    print("# =====================================================================")


