# 🧱 NORMALIZED CASE OBJECT

### AI_Engineering_Digital_Signal_Telemetry
---

This document defines the **canonical normalized case object** produced at the end of **Phase 5 (Ingestion)** and explains how it is interpreted during **Phase 6 (Cleaning)**, **schema design**, and **finetuning preparation**.

It serves as a reference for:

* Data engineering
* Schema enforcement  
* Embedding/vector preparation  
* RAG retrieval  
* Agentic diagnostic workflows  

---

## ⭐ 1. Canonical Case Object (Post‑Ingestion, Phase 5)

After Phase 5, each troubleshooting case is a **normalized Python dictionary** with the following structure:

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

## ⭐ 2. Characteristics of the normalized case object

* **Hierarchical —** nested dictionaries

* **Mixed‑type —** strings, ints, floats, lists

* **Semi‑structured —** consistent keys, flexible values

* **Schema‑ready —** predictable top‑level fields

This is the **exact structure** consumed by the cleaning layer.

## ⭐ 3. How Cleaning Relates to PostgreSQL + Finetuning Vectors

**PostgreSQL wants:**

* Flat tables

* Predictable column types

* No nested dicts

* No lists

* No inconsistent strings

The cleaning layer prepares the data for schema flattening.

**Finetuning / Embedding wants:**

* Clean text

* No weird characters

* No whitespace noise

* No malformed numbers

* No inconsistent casing

The cleaning layer prepares the data for vectorization.

**Cleaning is the bridge between:**

Raw JSON → Structured SQL / Embedding‑ready text

## ⭐ 4. Understanding the Parsing / Delimiting of the Case Object

Breaking CaseId "001" example into chunks the way a human (and Python) sees it.

**Here is the raw object:**

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

Top-level “chunks” (delimited by commas)

**Think of these as columns in a relational schema:**

* CaseId

* ProtocolFamily

* Symptom

* Context

* ObservedSignals

* RootCause

* ResolutionSteps

### Notes

#### **Nested chunks**

Context and ObservedSignals are sub‑tables in relational terms.

#### **List chunks**

ResolutionSteps is a one‑to‑many relationship.

## ⭐ 5. How clean_case() interprets this structure

**When Python runs:**

```python
for key, value in case.items():
```

**It sees:**

| **Key**            | **Value Type** |
|--------------------|----------------|
| CaseId             | str            |
| ProtocolFamily     | str            |
| Symptom            | str            |
| Context            | dict           |
| ObservedSignals    | dict           |
| RootCause          | str            |
| ResolutionSteps    | list           |
| Notes              | str            |
