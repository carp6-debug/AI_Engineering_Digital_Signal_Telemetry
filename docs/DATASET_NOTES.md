# 🗂️ Dataset Notes

### **Case‑Based Troubleshooting Dataset for Digital Radio Communications**

---

## 📡 Dataset Type

**Case‑based troubleshooting dataset** focused on digital radio communication systems, including **DMR**, **P25**, and **NXDN** protocol families.

This dataset captures real‑world and synthetic diagnostic scenarios involving signal integrity issues, protocol‑level failures, and multi‑step troubleshooting workflows.

---

## 🎯 Purpose

This dataset is designed to support:

- **RAG (Retrieval‑Augmented Generation)**
- **Finetuning** of a domain‑specific model
- **Agentic multi‑step diagnostic workflows**
- **Signal integrity and failure analysis reasoning**
- **End‑to‑end AI Engineering system development**

It serves as the foundational knowledge base for the  
**AI_Engineering_Digital_Signal_Telemetry** project.

---

## 🧩 Core Fields

Each troubleshooting case includes the following fields:

- **CaseId** — Unique identifier for the diagnostic case  
- **ProtocolFamily** — DMR, P25, NXDN, or related digital radio protocol  
- **Symptom** — Short description of the observed issue  
- **Context** — Environment, hardware, configuration, or operating conditions  
- **ObservedSignals** — Metrics such as RSSI, SNR, BER, CRC counts, jitter, dropouts  
- **RootCause** — Identified underlying cause of the failure  
- **ResolutionSteps** — Ordered steps taken to resolve the issue  
- **Notes** — Free‑form technical commentary, insights, or additional observations  

---

## 🧱 Canonical Case Object (Post‑Ingestion, Phase 5)

After Phase 5 of the ingestion pipeline, each troubleshooting case is represented as a **normalized Python dictionary** with the following structure:

```text
Case (dict)
│
├── CaseId (str)
├── ProtocolFamily (str)
├── Symptom (str)
│
├── Context (dict)
│     ├── Environment (str)
│     ├── Hardware (str)
│     └── Configuration (str)
│
├── ObservedSignals (dict)
│     ├── RSSI_dBm (int)
│     ├── SNR_dB (int)
│     ├── BER_percent (float)
│     ├── BER_peak_percent (float)
│     ├── CRC_Errors (str)
│     └── Jitter (str)
│
├── RootCause (str)
│
├── ResolutionSteps (list[str])
│
└── Notes (str)
```

**Example Raw JSON Case object:**
```code
{
 'CaseId': '001',
 'ProtocolFamily': 'DMR Tier II',
 'Symptom': 'Intermittent audio dropouts...',
 'Context': {
      'Environment': 'Urban area with reflective surfaces',
      'Hardware': 'Handheld DMR radio, 4W output',
      'Configuration': 'Repeater-linked, 12.5 kHz channel spacing'
 },
 'ObservedSignals': {
      'RSSI_dBm': -92,
      'SNR_dB': 14,
      'BER_percent': 5.0,
      'BER_peak_percent': 10.0,
      'CRC_Errors': 'Frequent',
      'Jitter': 'Moderate'
 },
 'RootCause': 'Multipath reflections...',
 'ResolutionSteps': [
      'Enabled receiver equalization mode.',
      'Adjusted antenna orientation...',
      'Relocated repeater antenna...'
 ],
 'Notes': 'DMR’s 4-FSK modulation...'
}
```

**This canonical structure is the foundation for:**

Phase 6 — Cleaning

Phase 7 — Schema enforcement

Phase 8 — Embedding preparation

Phase 9 — RAG retrieval

Phase 10 — Agentic diagnostic workflows

All downstream components assume this exact structure.

## 📘 Notes

This dataset will be expanded incrementally as part of the project’s tutorial‑style development process.
Initial cases will be manually curated to ensure clarity, realism, and alignment with the project’s AI Engineering objectives.

