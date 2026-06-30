# 🧠 HOWTO — Local QLoRA Finetuning

### AI_Engineering_Digital_Signal_Telemetry

### RAW Markdown Reference Guide

---

## 🎯 Purpose
Finetune a local LLM (7B–13B) using your `finetune_cases.jsonl` file.

This teaches the model **how to reason** about digital radio troubleshooting.

---

## 🧱 Requirements

Install:

```
pip install transformers accelerate bitsandbytes datasets peft
```

Hardware:

- NVIDIA GPU (your RTX 4070 SUPER is perfect)
- 16GB+ RAM (you have 32GB)
- 8GB+ VRAM (you have 12GB)

---

## 🛠️ Step‑by‑Step QLoRA Finetuning

### **1. Choose a base model**
Recommended:

```
meta-llama/Llama-3.2-3B
meta-llama/Llama-3.2-8B
mistralai/Mistral-7B-v0.3
```

### **2. Load your finetune JSONL**
```
from datasets import load_dataset

dataset = load_dataset("json", data_files="finetune_cases.jsonl")
```

### **3. Format the dataset**
```
def format_example(example):
    return {
        "text": f"### Prompt:\n{example['prompt']}\n\n### Response:\n{example['response']}"
    }

dataset = dataset.map(format_example)
```

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

### **5. Train**
```
from transformers import TrainingArguments, Trainer, AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(base_model, load_in_4bit=True)
tokenizer = AutoTokenizer.from_pretrained(base_model)

training_args = TrainingArguments(
    output_dir="./finetuned_model",
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

### **6. Save the finetuned model**
```
trainer.save_model("./finetuned_model")
```

---

## 🏁 Output
A local folder:

```
finetuned_model/
```

This is your **local troubleshooting LLM**.

