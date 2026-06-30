# python/tests/test_phase12_agentic.py
# =====================================================================
# TEST — PHASE 12 AGENTIC LOOP
# AI_Engineering_Digital_Signal_Telemetry
# =====================================================================

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from agentic_engine.phase12_agentic_loop import run_phase12_agentic

def main():
    print("\n=== TEST: Phase 12 Agentic Loop ===")
    query = "DMR radio audio dropouts while mobile — diagnose."
    run_phase12_agentic(query)
    print("\nPhase 12 test complete.")

if __name__ == "__main__":
    main()

