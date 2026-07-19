# python/finetune_engine/phase11_qlora.py

import os
import torch

# FORCE CPU-ONLY FINETUNING (Transformers 5.x)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TRANSFORMERS_NO_CUDA"] = "1"

torch.cuda.is_available = lambda: False
torch.backends.mps.is_available = lambda: False

from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    DataCollatorForSeq2Seq,
    Trainer,
)
from peft import LoraConfig, get_peft_model
#from python.paths import EMBEDDING_DATA, PROJECT_ROOT
import paths
EMBEDDING_DATA = paths.EMBEDDING_DATA
PROJECT_ROOT = paths.PROJECT_ROOT
from pathlib import Path

# ---------------------------------------------------------------------------
# GLOBALS — SINGLE SOURCE OF TRUTH (Phase 11 Finetuning)
# ---------------------------------------------------------------------------

FINETUNE_PATH = str(EMBEDDING_DATA / "finetune_cases.jsonl")

# Select which base model to finetune:
#   "llama-3.2-3b"
#   "llama-3.1-8b"
BASE_MODEL_KEY = "llama-3.1-8b"   # use 8B; switch to "llama-3.2-3b" if needed

# ---------------------------------------------------------------------------
# ABSOLUTE MODEL PATHS (HF-formatted, non-blob)
# ---------------------------------------------------------------------------

MODEL_PATHS = {
    # Llama‑3.2‑3B‑Instruct
    "llama-3.2-3b": str(
        Path(r"D:\DEVELOPMENT\Projects\AI_Engineering_Digital_Signal_Telemetry\models")
        / "llama-3.2-3b"
    ),

    # Llama‑3.1‑8B‑Instruct
    "llama-3.1-8b": str(
        Path(r"D:\DEVELOPMENT\Projects\AI_Engineering_Digital_Signal_Telemetry\models")
        / "llama-3.1-8b-instruct"
    ),
}

# ---------------------------------------------------------------------------
# OUTPUT DIRECTORIES FOR FINETUNED ADAPTERS
# ---------------------------------------------------------------------------

OUTPUT_DIRS = {
    "llama-3.2-3b": PROJECT_ROOT / "models" / "finetune_engine_phase11_llama_3_2_3b",
    "llama-3.1-8b": PROJECT_ROOT / "models" / "finetune_engine_phase11_llama_3_1_8b",
}

# ---------------------------------------------------------------------------
# OPTIONAL OFFLOAD DIRECTORIES (if you later add CPU offload logic)
# ---------------------------------------------------------------------------

OFFLOAD_DIRS = {
    "llama-3.2-3b": Path(__file__).parent / "offload" / "offload_llama_3_2_3b",
    "llama-3.1-8b": Path(__file__).parent / "offload" / "offload_llama_3_1_8b",
}

# ---------------------------------------------------------------------------
# DEVICE / DTYPE
# ---------------------------------------------------------------------------

DEVICE = "cpu"
DTYPE = torch.float32  # CPU‑friendly, no fp16

# ---------------------------------------------------------------------------
# RESOLVED MODEL + OUTPUT DIR
# ---------------------------------------------------------------------------

MODEL_NAME = MODEL_PATHS[BASE_MODEL_KEY]
OUTPUT_DIR = OUTPUT_DIRS[BASE_MODEL_KEY]
# If you plan to use offload later:
# OFFLOAD_DIR = OFFLOAD_DIRS[BASE_MODEL_KEY]
# OFFLOAD_DIR.mkdir(parents=True, exist_ok=True)


def run_phase11_finetune():
    print(f"\n=== PHASE 11 — QLoRA Finetuning ({BASE_MODEL_KEY}) ===")

    # -----------------------------------------------------------------------
    # Dataset
    # -----------------------------------------------------------------------
    dataset = load_dataset("json", data_files=FINETUNE_PATH, split="train")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def format_example(example):
        prompt = example["prompt"]
        response = example["response"]
        text = f"<s>[USER]\n{prompt}\n[/USER]\n[ASSISTANT]\n{response}\n</s>"
        enc = tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=1024,
        )
        enc["labels"] = enc["input_ids"].copy()
        return enc

    tokenized = dataset.map(format_example, remove_columns=dataset.column_names)

    # -----------------------------------------------------------------------
    # Base model (CPU‑only)
    # -----------------------------------------------------------------------
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=DTYPE,
        device_map={"": DEVICE},
    )

    # -----------------------------------------------------------------------
    # LoRA config (works for Llama 3B and 8B)
    # -----------------------------------------------------------------------
    lora_cfg = LoraConfig(
        r=64,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    peft_model = get_peft_model(model, lora_cfg)

    # -----------------------------------------------------------------------
    # Training arguments — stronger CPU QLoRA
    # -----------------------------------------------------------------------
    args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),

        # CPU-friendly batch simulation
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,   # stronger, smoother learning

        # Stronger domain imprint
        learning_rate=4e-4,             # more aggressive LoRA updates
        num_train_epochs=8,             # critical: makes the adapter actually learn

        # Logging / checkpointing
        logging_steps=1,
        save_steps=20,                  # cleaner checkpointing

        # CPU-only settings
        fp16=False,
        optim="adamw_torch",
    )

    collator = DataCollatorForSeq2Seq(tokenizer, model=peft_model)

    trainer = Trainer(
        model=peft_model,
        args=args,
        train_dataset=tokenized,
        data_collator=collator,
    )

    trainer.train()

    print(f"\n[Phase 11] Finetune complete → {OUTPUT_DIR}")










