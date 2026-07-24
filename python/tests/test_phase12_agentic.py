# python/tests/test_phase12_agentic.py
# =====================================================================
# TEST — PHASE 12 AGENTIC LOOP
# AI_Engineering_Digital_Signal_Telemetry
# =====================================================================

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from agentic_engine.phase12_agentic_loop import (
    run_phase12_agentic,
    SELECTED_MODEL,
)

def print_header():
    print("\n============================================================")
    print("              PHASE 12 — AGENTIC RAG LOOP TEST")
    print("============================================================")
    print(f"Model:   {SELECTED_MODEL}")
    print("============================================================\n")

def main():
    print_header()

    query = "DMR radio audio dropouts while mobile — diagnose."
    print(f"[TEST] Query: {query}\n")

    start = time.time()
    run_phase12_agentic(query)
    end = time.time()

    print(f"\n[TEST] Phase 12 completed in {end - start:.2f} seconds.")
    print("\n============================================================")
    print("                PHASE 12 TEST COMPLETE")
    print("============================================================\n")

if __name__ == "__main__":
    main()


