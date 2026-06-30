# python/finetune_engine/phase11_qlora.py

from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    DataCollatorForSeq2Seq,
    Trainer
)
from peft import LoraConfig, get_peft_model
from python.paths import EMBEDDING_DATA, PROJECT_ROOT
import torch

FINETUNE_PATH = EMBEDDING_DATA / "finetune_cases.jsonl"
FINETUNE_PATH = str(FINETUNE_PATH)

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

def run_phase11_finetune():
    print("\n=== PHASE 11 — QLoRA Finetuning ===")

    dataset = load_dataset("json", data_files=FINETUNE_PATH, split="train")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    def format_example(example):
        prompt = example["prompt"]
        response = example["response"]
        text = f"<s>[USER]\n{prompt}\n[/USER]\n[ASSISTANT]\n{response}\n</s>"
        enc = tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=1024
        )
        enc["labels"] = enc["input_ids"].copy()
        return enc

    tokenized = dataset.map(format_example, remove_columns=dataset.column_names)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16
    )
    model.to("cuda")

    lora_cfg = LoraConfig(
        r=64,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    peft_model = get_peft_model(model, lora_cfg)

    args = TrainingArguments(
        output_dir=str(PROJECT_ROOT / "models" / "finetune_engine_phase11"),
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        learning_rate=2e-4,
        num_train_epochs=1,
        logging_steps=1,
        save_steps=5,
        fp16=False,
        optim="adamw_torch"
    )

    collator = DataCollatorForSeq2Seq(tokenizer, model=peft_model)

    trainer = Trainer(
        model=peft_model,
        args=args,
        train_dataset=tokenized,
        data_collator=collator
    )

    trainer.train()

    output_dir = PROJECT_ROOT / "models" / "finetune_engine_phase11"
    output_dir








