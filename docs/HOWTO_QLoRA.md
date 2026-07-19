# 🧠 HOWTO — Local QLoRA Finetuning

### AI_Engineering_Digital_Signal_Telemetry  
### RAW Markdown Reference Guide

---

## 🎯 Purpose
Finetune a local LLM (7B–13B) using your `finetune_cases.jsonl` file.

This teaches the model **how to reason** about digital radio troubleshooting.

---

## 🔍 What QLoRA Actually Means
**QLoRA = Quantized Low‑Rank Adaptation**

It is a **parameter‑efficient finetuning method** that allows training large models on consumer GPUs by:

- Freezing the base model  
- Loading it in **4‑bit quantized mode**  
- Training only small **low‑rank adapter layers**  
- Producing a tiny, efficient finetuned checkpoint  

This is exactly what Phase 11 uses.

---

## 🧱 Requirements

### Install (Updated)
Your final working configuration **did NOT use bitsandbytes**.

Install:

```
pip install transformers accelerate datasets peft
```

### Hardware
- NVIDIA GPU (RTX 4070 SUPER — perfect)
- 16GB+ RAM (you have 32GB)
- 8GB+ VRAM (you have 12GB)

---

## 🛠️ Step‑by‑Step QLoRA Finetuning

### **1. Choose a base model**
Recommended (Phase 11 uses Mistral):

```
mistralai/Mistral-7B-Instruct-v0.2
```

Alternatives:

```
meta-llama/Llama-3.2-3B
meta-llama/Llama-3.2-8B
```

---

### **2. Load your finetune JSONL**
```
from datasets import load_dataset

dataset = load_dataset("json", data_files="finetune_cases.jsonl")
```

---

### **3. Format the dataset**
```
def format_example(example):
    return {
        "text": f"### Prompt:\n{example['prompt']}\n\n### Response:\n{example['response']}"
    }

dataset = dataset.map(format_example)
```

---

### **4. Configure QLoRA**
```
from peft import LoraConfig

lora_config = LoraConfig(
    r=64,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"]
)
```

---

### **5. Train**
```
from transformers import (
    TrainingArguments,
    Trainer,
    AutoModelForCausalLM,
    AutoTokenizer
)

base_model = "mistralai/Mistral-7B-Instruct-v0.2"

model = AutoModelForCausalLM.from_pretrained(
    base_model,
    load_in_4bit=True
)

tokenizer = AutoTokenizer.from_pretrained(base_model)

training_args = TrainingArguments(
    output_dir="./models/finetune_engine_phase11",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_steps=200
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"]
)

trainer.train()
```

---

### **6. Save the finetuned adapter**
```
trainer.save_model("./models/finetune_engine_phase11")
```

This produces:

```
models/finetune_engine_phase11/checkpoint-5/
    adapter_config.json
    adapter_model.safetensors
    training_args.bin
    trainer_state.json
    optimizer.pt
    scheduler.pt
    rng_state.pth
```

---

## 🏁 Output
A local folder:

```
models/finetune_engine_phase11/
```

This contains your **QLoRA adapter**, which Phase 12 loads to perform:

- domain‑specific reasoning  
- RF troubleshooting logic  
- structured diagnostic workflows  

This completes **Phase 11 Finetuning**.



