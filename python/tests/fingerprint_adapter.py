import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

#BASE = r"D:\DEVELOPMENT\Projects\AI_Engineering_Digital_Signal_Telemetry\models\llama-3.2-3b"
BASE = r"D:\DEVELOPMENT\Projects\AI_Engineering_Digital_Signal_Telemetry\models\mistral-7b"
#ADAPTER = r"D:\DEVELOPMENT\Projects\AI_Engineering_Digital_Signal_Telemetry\models\finetune_engine_phase11_llama_3_2_3b\checkpoint-5"
ADAPTER = r"D:\DEVELOPMENT\Projects\AI_Engineering_Digital_Signal_Telemetry\models\finetune_engine_phase11_7b\checkpoint-8"

tokenizer = AutoTokenizer.from_pretrained(BASE)
tokenizer.padding_side = "left"
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("\n=== Loading BASE model ===")
base_model = AutoModelForCausalLM.from_pretrained(
    BASE,
    device_map={"": "cpu"},
    torch_dtype=torch.float32,
).eval()

print("\n=== Loading ADAPTER model ===")
adapter_model = PeftModel.from_pretrained(
    base_model,
    ADAPTER,
    device_map={"": "cpu"},
).eval()

def run(model, prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        ids = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.2,
            top_k=40,
            top_p=0.9,
            do_sample=True,
        )
    return tokenizer.decode(ids[0], skip_special_tokens=True)

#prompt = "DMR radio has high noise floor on transmit. Diagnose the issue."

prompt = """CaseId: 999.0
ProtocolFamily: DMR Tier II
Symptom: High noise floor on transmit.
Context:
  Environment: Urban
  Hardware: Mobile DMR radio
  Configuration: Repeater-linked
ObservedSignals:
  RSSI_dBm: -90
  SNR_dB: 12
  BER_percent: 4.0
  BER_peak_percent: 8.0
  CRC_Errors: Moderate
  Jitter: Low
"""


print("\n=== BASE MODEL OUTPUT ===")
print(run(base_model, prompt))

print("\n=== ADAPTER MODEL OUTPUT ===")
print(run(adapter_model, prompt))
