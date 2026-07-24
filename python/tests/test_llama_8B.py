import requests
import json

DIGITAL_MODE = "NXDN"   # "DMR", "P25", or "NXDN"

DMR_PROMPT = """You are performing a DMR Tier II diagnostic analysis.
Explicitly reference “DMR Tier II” in your response.

DMR Tier II troubleshooting case.
CaseId 201.
High noise floor and audio dropouts during mobile operation.
Urban canyon environment using a Hytera MD782i mobile radio.
Repeater-linked system with 12.5 kHz channel spacing.
RSSI -98 dBm, SNR 10 dB, BER 6%, peak BER 12%.
Slot timing offset 3.2 microseconds.

Provide a detailed DMR Tier II telemetry interpretation including:
- DMR modulation type
- DMR burst error behavior
- DMR slot timing
- DMR signal quality
- DMR root cause analysis
"""

P25_PROMPT = """You are performing a P25 Phase I diagnostic analysis.
Explicitly reference “P25 Phase I” in your response.

P25 Phase I troubleshooting case.
CaseId 305.
Garbled voice frames and repeated NAC mismatches on a trunked system.
Suburban environment using a Motorola APX6000 portable radio.
Operating at 9600 bps C4FM modulation.
RSSI -102 dBm, SNR 8 dB, frame error rate 4.5%.
NAC mismatch count 12, C4FM symbol deviation 4800 Hz.

Provide a detailed P25 Phase I telemetry interpretation including:
- P25 modulation type
- P25 frame error behavior
- P25 NAC mismatch analysis
- P25 symbol deviation
- P25 signal quality
- P25 root cause analysis
"""


NXDN_PROMPT = """You are performing an NXDN 4800 diagnostic analysis.
Explicitly reference “NXDN 4800” in your response.

NXDN 4800 troubleshooting case.
CaseId 412.
Intermittent RAN mismatches and slow call setup in an industrial facility.
Icom F5061 mobile radio using a 6.25 kHz FDMA channel.
RSSI -95 dBm, SNR 14 dB, RAN mismatch count 7.
Symbol rate 4800 bps, frequency error -85 Hz.

Provide a detailed NXDN 4800 telemetry interpretation including:
- NXDN modulation type
- NXDN RAN behavior
- NXDN symbol rate analysis
- NXDN signal quality
- NXDN root cause analysis
"""


ADAPTER_MAP = {
    "DMR": "DMR Troubleshooting",
    "P25": "P25 adapter",
    "NXDN": "NXDN adapter"
}

PROMPT_MAP = {
    "DMR": DMR_PROMPT,
    "P25": P25_PROMPT,
    "NXDN": NXDN_PROMPT
}

payload = {
    "prompt": PROMPT_MAP[DIGITAL_MODE],
    "modelName": "Llama-3.1-8B (Instruct)",
    "adapterName": ADAPTER_MAP[DIGITAL_MODE],
    "temperature": 0.2,
    "topK": 40,
    "topP": 0.9,
    "useRag": False,
    "useAgentic": False
}

response = requests.post(
    "http://localhost:8000/api/v1/inference",
    json=payload
)

print("STATUS:", response.status_code)
try:
    print("RESPONSE:", json.dumps(response.json(), indent=2))
except Exception:
    print("RAW RESPONSE:", response.text)




