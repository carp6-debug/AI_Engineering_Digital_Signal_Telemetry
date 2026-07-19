import requests
import json

#"prompt": "Low noise",
payload = {
    "prompt": """CaseId: 999.0
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
""",
    "modelName": "Llama-3.1-8B (Instruct)",
    "adapterName": "None",
    "temperature": 0.2,
    "topK": 40,
    "topP": 0.9,
    "useRag": False,
    "useAgentic": False
}

#  "prompt": """CaseId: 999.0
#  ProtocolFamily: DMR Tier II
#  Symptom: High noise floor on transmit.
#  Context:
#  Environment: Urban
#  Hardware: Mobile DMR radio
#  Configuration: Repeater-linked
#  ObservedSignals:
#  RSSI_dBm: -90
#  SNR_dB: 12
#  BER_percent: 4.0
#  BER_peak_percent: 8.0
#  CRC_Errors: Moderate
#  Jitter: Low


response = requests.post(
    "http://localhost:8000/api/v1/inference",
    json=payload
)

print("STATUS:", response.status_code)
print("RESPONSE:", json.dumps(response.json(), indent=2))
