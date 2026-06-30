"""
PHASE 9 — FINETUNING JSONL CONSTRUCTION
Builds clean prompt/response pairs from validated case objects.
"""

import json
from pathlib import Path
import unicodedata

# ---------------------------------------------------------------------
# TEXT NORMALIZATION (fix artifacts like â€™, etc.)
# ---------------------------------------------------------------------
def normalize_text(s):
    if not isinstance(s, str):
        return s

    replacements = {
        "â€™": "'",
        "â€œ": '"',
        "â€": '"',
        "â€“": "-",
        "â€”": "-",
        "â€˜": "'",
        "â€¢": "*",
        "â€¦": "...",
    }

    for bad, good in replacements.items():
        s = s.replace(bad, good)

    s = unicodedata.normalize("NFC", s)
    return s


def debug_finetune(msg, DEBUG_FINETUNE):
    if DEBUG_FINETUNE:
        print(f"[PHASE 9 DEBUG] {msg}")


# ---------------------------------------------------------------------
# BUILD PROMPT/RESPONSE FOR A SINGLE CASE
# ---------------------------------------------------------------------
def build_prompt_response(case, DEBUG_FINETUNE=False):
    case_id = case.get("CaseId")

    print("\n------------------------------------------------------------")
    print(f"PHASE 9 — BUILDING FINETUNE ENTRY FOR CASE {case_id}")
    print("------------------------------------------------------------")

    # Normalize key text fields
    symptom = normalize_text(case.get("Symptom"))
    root_cause = normalize_text(case.get("RootCause"))
    notes = normalize_text(case.get("Notes"))

    ctx = case.get("Context", {})
    ctx_env = normalize_text(ctx.get("Environment"))
    ctx_hw = normalize_text(ctx.get("Hardware"))
    ctx_cfg = normalize_text(ctx.get("Configuration"))

    sig = case.get("ObservedSignals", {})
    # Normalize string-valued signals
    norm_signals = {}
    for k, v in sig.items():
        norm_signals[k] = normalize_text(v) if isinstance(v, str) else v

    resolution_steps = [normalize_text(step) for step in case.get("ResolutionSteps", [])]

    debug_finetune("Normalized case fields:", DEBUG_FINETUNE)
    debug_finetune(json.dumps(case, indent=4), DEBUG_FINETUNE)

    # Prompt: describe the situation
    prompt_lines = []
    prompt_lines.append(f"CaseId: {case_id}")
    prompt_lines.append(f"ProtocolFamily: {normalize_text(case.get('ProtocolFamily'))}")
    prompt_lines.append(f"Symptom: {symptom}")
    prompt_lines.append("Context:")
    prompt_lines.append(f"  Environment: {ctx_env}")
    prompt_lines.append(f"  Hardware: {ctx_hw}")
    prompt_lines.append(f"  Configuration: {ctx_cfg}")
    prompt_lines.append("ObservedSignals:")
    for key, value in norm_signals.items():
        prompt_lines.append(f"  {key}: {value}")

    prompt = "\n".join(prompt_lines)

    # Response: root cause + resolution + notes
    response_lines = []
    response_lines.append(f"RootCause: {root_cause}")
    response_lines.append("ResolutionSteps:")
    for step in resolution_steps:
        response_lines.append(f"  - {step}")
    response_lines.append(f"Notes: {notes}")

    response = "\n".join(response_lines)

    debug_finetune("FINAL PROMPT:", DEBUG_FINETUNE)
    debug_finetune(prompt, DEBUG_FINETUNE)
    debug_finetune("FINAL RESPONSE:", DEBUG_FINETUNE)
    debug_finetune(response, DEBUG_FINETUNE)

    return prompt, response


# ---------------------------------------------------------------------
# MAIN PHASE 9 EXECUTION FUNCTION
# ---------------------------------------------------------------------
def run_phase_9_finetune(input_path, output_path, DEBUG_FINETUNE=False):
    print("# =====================================================================")
    print("PHASE 9 — FINETUNING JSONL CONSTRUCTION")
    print("run_phase_9_finetune(input_path, output_path, DEBUG_FINETUNE=False):")
    print("# =====================================================================")

    print(f"Loading validated cases from: {input_path}")

    if not Path(input_path).exists():
        print(f"❌ ERROR: Validated cases file does not exist: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    print(f"Loaded {len(cases)} validated cases.")
    print("Building finetuning prompt/response pairs for each case...\n")

    with open(output_path, "w", encoding="utf-8") as out:
        for case in cases:
            prompt, response = build_prompt_response(case, DEBUG_FINETUNE)

            jsonl_entry = {
                "case_id": case.get("CaseId"),
                "prompt": prompt,
                "response": response
            }

            out.write(json.dumps(jsonl_entry) + "\n")

    print(f"\nPHASE 9 COMPLETE — Finetune JSONL written to:")
    print(f"{output_path}")
    print("# =====================================================================")
