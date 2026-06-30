# =====================================================================
# TEST — PHASE 11 FINETUNING
# AI_Engineering_Digital_Signal_Telemetry
# =====================================================================

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from finetune_engine.phase11_qlora import run_phase11_finetune

def main():
    print("\n=== TEST: Phase 11 Finetuning ===")
    run_phase11_finetune()
    print("\nPhase 11 test complete.")

if __name__ == "__main__":
    main()
