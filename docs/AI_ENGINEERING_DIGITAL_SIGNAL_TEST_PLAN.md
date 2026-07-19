# 📘 AI Engineering Digital Signal Telemetry  
## Comprehensive Test Plan for 3B and 8B Models  
### Location: /docs/AI_ENGINEERING_DIGITAL_SIGNAL_TEST_PLAN.md

---

# 🧭 Overview

This document defines the **complete test plan** for validating the behavior, stability, and domain alignment of the **Llama‑3.2‑3B** and **Llama‑3.1‑8B** finetuned models used in the  
**AI_Engineering_Digital_Signal_Telemetry** project.

Testing is performed through:

- **Dashboard UI** (primary)
- **Python Test Harness** (secondary, regression or ambiguity resolution)

This plan includes:

- Baseline Use Cases  
- CPU‑aware Use Cases  
- Adapter‑verification Use Cases  
- RAG similarity Use Cases  
- Agentic reasoning Use Cases  
- Edge and “fall‑off‑cliff” Use Cases  
- Prompt‑driven domain alignment tests  

---

# 🧩 1. Model Selection Use Cases (3B vs 8B)

### **UC‑MS‑01 — Model Selection Validation**
**Purpose:** Ensure Dashboard UI → Sidecar → Model Loader selects correct model.

**Steps:**
- Select **3B** model  
- Select **8B** model  

**Expected:**
- Correct model metadata returned  
- Correct adapter name displayed  
- Correct token count  
- Correct latency range  
  - 3B: **3.5–5 minutes**  
  - 8B: **12–18 minutes**  

---

# 🧩 2. Adapter Loading Use Cases (DMR Troubleshooting LoRA)

### **UC‑AD‑01 — Adapter Merge Confirmation**
**Purpose:** Validate LoRA adapter loading despite misleading sidecar logs.

**Prompt:**  
DMR Tier II — High noise floor (CaseId 999)

**Expected (3B):**
- PeakBER  
- PeakRSSI  
- PeakSNR  
- PeakLatency  
- Signal Quality  

**Expected (8B):**
- ModulationType: 4FSK  
- SymbolRate_bps: 4800  
- BurstErrorRate fields  
- FrequencyOffset / PhaseNoise  
- Signal Quality  

**Pass Criteria:**  
Presence of domain‑specific telemetry fields proves adapter loaded.

---

# 🧩 3. Telemetry Interpretation Use Cases

### **UC‑TI‑01 — High Noise Floor Interpretation**
**Purpose:** Validate BER/SNR/RSSI interpretation.

**Expected:**
- BER numeric  
- RSSI negative  
- Multipath between 0–10  
- Signal Quality = MARGINAL or POOR  

---

# 🧩 4. RAG Retrieval Use Cases

### **UC‑RAG‑01 — Similarity Ranking Validation**
**Purpose:** Validate MiniLM + Chroma vector retrieval.

**Expected:**
- CaseId list non‑empty  
- Similarity scores between 0.5–0.9  
- 8B similarity > 3B similarity  
- ProtocolFamily and Symptom parsed correctly  

---

# 🧩 5. Agentic Reasoning Use Cases

### **UC‑AG‑01 — Diagnostic Reasoning Validation**
**Purpose:** Validate multi‑step agentic reasoning.

**Expected:**
- At least one diagnostic step  
- Evidence field present  
- Final diagnosis present  
- ConfidenceScore between 0–1  

---

# 🧩 6. CPU‑Aware Performance Use Cases

### **UC‑CPU‑01 — Latency Profiling**
**Purpose:** Validate CPU‑only inference stability.

**Expected:**
- 3B completes within **3.5–5 minutes**  
- 8B completes within **12–18 minutes**  
- >20 minutes = performance regression  

---

### **UC‑CPU‑02 — Prompt Complexity Sensitivity**
**Purpose:** Validate latency impact of prompt complexity.

**Expected:**
- Simple prompt:  
  - 3B < 3 minutes  
  - 8B < 10 minutes  
- Complex prompt:  
  - 3B ≈ 5 minutes  
  - 8B ≈ 15 minutes  

---

# 🧩 7. Baseline Use Cases

### **UC‑BL‑01 — Golden Baseline Case**
**Prompt:**  
DMR Tier II — High noise floor (CaseId 999)

**Expected (3B):**
- PeakBER, PeakRSSI, PeakSNR  
- Multipath  
- Signal Quality  

**Expected (8B):**
- ModulationType, SymbolRate  
- BurstErrorRate fields  
- FrequencyOffset / PhaseNoise  

**Expected (Both):**
- RAG similarity > 0.7  
- Agentic reasoning present  

---

# 🧩 8. Edge Use Cases

### **UC‑ED‑01 — Minimal Telemetry Edge Case**
**Prompt:**
RSSI_dBm: -120
SNR_dB: 0
BER_percent: 0.0

**Expected:**
- Domain telemetry still present  
- RAG similarity < 0.4  
- Agentic reasoning still produces final diagnosis  
- Signal Quality = POOR  

---

### **UC‑ED‑02 — Fall‑Off‑Cliff Case**
**Prompt:**

ProtocolFamily: None
Symptom: None
Environment: Fantasy
Hardware: Magic radio


**Expected:**
- No domain telemetry  
- No modulation type  
- RAG similarity < 0.2  
- Agentic reasoning generic  
- Demonstrates finetuning boundaries  

---

# 🧩 9. Prompt‑Driven Domain Alignment Use Cases

### **UC‑PD‑01 — Slightly Off‑Domain**
**Prompt:**  
Audio distortion at high volume.

**Expected:**  
- Partial domain telemetry  
- RAG similarity ~0.5  

---

### **UC‑PD‑02 — Moderately Off‑Domain**
**Prompt:**  
Battery drains quickly.

**Expected:**  
- Some domain telemetry  
- RAG similarity ~0.3  
- Agentic reasoning generic  

---

### **UC‑PD‑03 — Completely Off‑Domain**
**Prompt:**  
Radio smells like burning plastic.

**Expected:**  
- No domain telemetry  
- RAG similarity ~0.1  
- Agentic reasoning generic  
- Confirms domain boundary  

---

# 🧩 10. Python Test Harness Regression Use Cases

### **UC‑PY‑01 — Baseline Regression**
Run CaseId 999 through Python harness.

### **UC‑PY‑02 — Edge Regression**
Run minimal telemetry case.

### **UC‑PY‑03 — Fall‑Off‑Cliff Regression**
Run fantasy/magic radio case.

**Expected:**  
Python harness results must match Dashboard UI behavior.

---

# 🧩 11. Summary

This test plan provides:

- Full validation of 3B and 8B finetuned models  
- Confirmation of adapter loading  
- Confirmation of domain telemetry generation  
- Confirmation of RAG and agentic reasoning  
- CPU‑aware performance profiling  
- Baseline + edge + prompt‑driven Use Cases  
- Regression testing via Python harness  

This suite is sufficient for portfolio demonstration, architectural validation, and future GPU‑based expansion.

---

# ✔ End of Document
