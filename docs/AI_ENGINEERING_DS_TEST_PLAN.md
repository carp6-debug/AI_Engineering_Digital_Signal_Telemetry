# 📘 AI Engineering Digital Signal Telemetry

## Operational Test Plan (Dashboard + Sidecar)

### Location: /docs/AI_ENGINEERING_DIGITAL_SIGNAL_TEST_PLAN.md

---

## 🧭 Overview

### This Test Plan validates the complete AI Engineering pipeline:

* Model loading (3B / 8B)

* Adapter loading (DMR Troubleshooting LoRA)

* Telemetry generation

* RAG retrieval

* Agentic reasoning

* CPU‑only performance

* Domain boundary behavior

### The Dashboard UI only needs to be configured once per test, using:

* Model

* Adapter

* Prompt

* RAG toggle

* Agentic toggle

The Sidecar test harnesses mirror the same configuration.

## ⭐ Standard Dashboard Configuration for Most Tests

Unless otherwise stated, all tests use:

* Model: Llama‑3.2‑3B

* Adapter: DMR Troubleshooting

* Use RAG: Enabled

* Use Agentic: Enabled

* This configuration exercises the full pipeline.

* The 8B model is used only for performance comparison and telemetry richness tests.

## 🧩 Test Case 1 — Model Selection Validation

### Purpose

Ensure Dashboard → Sidecar → Model Loader selects correct model.

### Prompt

None

### Dashboard Settings

Select 3B

Select 8B

### Expected

Correct model name returned

Correct adapter name

Correct token count

Latency ranges:

3B: 3.5–5 minutes

8B: 12–18 minutes

## 🧩 Test Case 2 — Adapter Loading Validation

### Purpose

Verify LoRA adapter is applied and domain telemetry appears.

### Prompt

DMR Tier II — High noise floor (CaseId 999)

### Expected (3B)

PeakBER

PeakRSSI

PeakSNR

Multipath

Signal Quality

Expected (8B)

ModulationType

SymbolRate

BurstErrorRate fields

FrequencyOffset / PhaseNoise

## 🧩 Test Case 3 — Telemetry Interpretation Validation

### Purpose

Validate BER/SNR/RSSI interpretation logic.

### Prompt

DMR Tier II — High noise floor (CaseId 999)

### Expected

BER numeric

RSSI negative

Multipath 0–10

Signal Quality = MARGINAL or POOR

## 🧩 Test Case 4 — RAG Retrieval Validation

### Purpose

Validate MiniLM + Chroma similarity ranking.

### Prompt

DMR Tier II — High noise floor (CaseId 999)

### Expected

CaseId list non‑empty

Similarity scores 0.5–0.9

ProtocolFamily + Symptom parsed

8B similarity > 3B similarity

## 🧩 Test Case 5 — Agentic Reasoning Validation

### Purpose

Validate multi‑step diagnostic reasoning.

### Prompt

DMR Tier II — High noise floor (CaseId 999)

### Expected

Step 1, Step 2, etc.

Evidence field present

Intermediate conclusion

Final diagnosis

ConfidenceScore 0–1

## 🧩 Test Case 6 — CPU Performance Validation

### Purpose

Validate CPU‑only inference stability.

### Prompt

DMR Tier II — High noise floor (CaseId 999)

**Expected

3B: 3.5–5 minutes

8B: 12–18 minutes

20 minutes = regression

## 🧩 Test Case 7 — Prompt Complexity Sensitivity

### Purpose

Validate latency impact of prompt complexity.

### Prompts

Simple:

Hello radio.

Complex:

DMR Tier II — High noise floor (CaseId 999)

### Expected

Simple prompt:

3B < 3 minutes

8B < 10 minutes

Complex prompt:

3B ≈ 5 minutes

8B ≈ 15 minutes

## 🧩 Test Case 8 — Minimal Telemetry Edge Case

### Purpose

Validate behavior with extremely low signal values.

### Prompt

RSSI_dBm: -120

SNR_dB: 0

BER_percent: 0.0

### Expected

Domain telemetry still present

RAG similarity < 0.4

Agentic reasoning still produces final diagnosis

Signal Quality = POOR

## 🧩 Test Case 9 — Domain Boundary Validation

Validate behavior outside domain boundaries.

### Prompt

ProtocolFamily: None

Symptom: None

Environment: Fantasy

Hardware: Magic radio

### Expected

No domain telemetry

RAG similarity < 0.2

Agentic reasoning generic

Demonstrates finetuning boundaries

## 🧩 Test Case 10 — Off‑Domain Alignment Tests

### Purpose

Validate partial → moderate → complete domain drift.

### Prompts

Slightly Off‑Domain:

Audio distortion at high volume.

Moderately Off‑Domain:

Battery drains quickly.

Completely Off‑Domain:

Radio smells like burning plastic.

### Expected

Slightly off‑domain → partial telemetry, similarity ~0.5

Moderately off‑domain → some telemetry, similarity ~0.3

Completely off‑domain → no telemetry, similarity ~0.1

## 🧩 Test Case 11 — Python Harness Regression

### Purpose

Ensure Sidecar harness matches Dashboard UI.

### Prompts

Use the same prompts from Test Cases 2,3,6,7.

### Expected

Harness output matches Dashboard output

Telemetry fields identical

RAG similarity identical

Agentic reasoning identical

## 🧩 Test Case 12 — Domain—Prompt Simialrities

### Purpose

Using the same Domain Specific Adapter [Finetune] and Prompt compare AI Response(s), RAG Similarities [%] and Agentic Diagostic Flows [Steps]

### Prompt

* DMR High Noise Floor
  
* P25 High Noise Floor
  
* NXDN High Noise Floor

### Expected (3B)

**For Each:**

* References to DMR Noise Floor and DMR Noise Floor Telemetry

* References to P25 Noise Floor and P25 Noise Floor Telemetry

* References to NXDN Noise Floor and NXDN Noise Floor Telemetry

### Expected (8B)

**For Each:**

* Comprehensive References to DMR Noise Floor and DMR Noise Floor Telemetry

* Comprehensive References to P25 Noise Floor and P25 Noise Floor Telemetry

* Comprehensive References to NXDN Noise Floor and NXDN Noise Floor Telemetry

## 🧩 Test Case 13 — Domain—Prompt Simialrities

### Purpose

Using the same Domain Specific Adapter [Finetune] and Prompt compare AI Response(s), RAG Similarities [%] and Agentic Diagostic Flows [Steps]

### Prompt

**For Each:**

* DMR BER/SNR/RSSI

* P25 BER/SNR/RSSI

* NXDN BER/SNR/RSSI

### Expected (3B)

**For Each:**

* Applicable references to DMR BER/SNR/RSSI and Telemetry

* Applicable references to P25 BER/SNR/RSSI and Telemetry

* Applicable references to NXDN BER/SNR/RSSI and Telemetry

### Expected (8B)

**For Each:**

* Comprehensive applicable references to DMR BER/SNR/RSSI and Telemetry

* Comprehensive applicable references to P25 BER/SNR/RSSI and Telemetry

* Comprehensive applicable references to NXDN BER/SNR/RSSI and Telemetry

