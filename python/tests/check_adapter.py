import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig

BASE = r"D:\DEVELOPMENT\Projects\AI_Engineering_Digital_Signal_Telemetry\models\llama-3.2-3b"
ADAPTER = r"D:\DEVELOPMENT\Projects\AI_Engineering_Digital_Signal_Telemetry\models\finetune_engine_phase11_llama_3_2_3b\checkpoint-5"

print("\n=== Loading base model ===")
model = AutoModelForCausalLM.from_pretrained(BASE, device_map={"": "cpu"}, torch_dtype=torch.float32)

print("\n=== Loading adapter config ===")
try:
    cfg = PeftConfig.from_pretrained(ADAPTER)
    print("Adapter type:", cfg.peft_type)
    print("Target modules:", cfg.target_modules)
except Exception as e:
    print("ERROR: Cannot load adapter config:", e)
    exit()

print("\n=== Attaching adapter ===")
try:
    model = PeftModel.from_pretrained(model, ADAPTER, device_map={"": "cpu"})
    print("Adapter attached successfully.")
except Exception as e:
    print("ERROR attaching adapter:", e)
    exit()

print("\n=== Checking active adapter layers ===")
active = [n for n, p in model.named_parameters() if "lora" in n.lower()]
print("Active LoRA layers:", len(active))
for name in active[:20]:
    print(" -", name)

print("\n=== Checking if LoRA modifies weights ===")
modified = []
for name, p in model.named_parameters():
    if "lora" in name.lower():
        if torch.sum(torch.abs(p.data)) > 0:
            modified.append(name)

print("Modified LoRA layers:", len(modified))
for name in modified[:20]:
    print(" -", name)

print("\n=== DONE ===")
