# 📡 Example Troubleshooting Cases

## **Digital Radio Communications (DMR / P25 / NXDN)**

## Seed Dataset for AI_Engineering_Digital_Signal_Telemetry

These initial cases form the foundation of the ingestion pipeline, embedding generation, RAG retrieval, finetuning, and agentic diagnostic workflows.

---

## 🧩 Case 001 — DMR: Intermittent Audio Dropouts at High BER

**CaseId:** 001  
**ProtocolFamily:** DMR Tier II  
**Symptom:**  
Intermittent audio dropouts during voice transmission, especially when mobile unit is in motion.

**Context:**

- Environment: Urban area with reflective surfaces  
- Hardware: Handheld DMR radio, 4W output  
- Configuration: Repeater‑linked, 12.5 kHz channel spacing  

**ObservedSignals:**

- RSSI: –92 dBm  
- SNR: 14 dB  
- BER: 5–7% (spiking to 10%)  
- CRC Errors: Frequent  
- Jitter: Moderate  

**RootCause:**  
Multipath reflections causing symbol timing errors and elevated BER.

**ResolutionSteps:**

1. Enabled receiver equalization mode.  
2. Adjusted antenna orientation to reduce reflective path dominance.  
3. Relocated repeater antenna to improve line‑of‑sight coverage.  

**Notes:**  
DMR’s 4‑FSK modulation is sensitive to multipath in dense urban environments. BER > 5% typically results in audible artifacts or dropouts.

---

## 🧩 Case 002 — P25: Decode Failures Due to Incorrect NAC

**CaseId:** 002  
**ProtocolFamily:** P25 Phase I  
**Symptom:**  
Receiver fails to decode voice frames; displays “INVALID NAC” error.

**Context:**

- Environment: Dispatch center  
- Hardware: P25 base station receiver  
- Configuration: Mixed fleet of subscriber radios  

**ObservedSignals:**

- RSSI: –78 dBm  
- SNR: 22 dB  
- BER: <1%  
- CRC Errors: None  
- NAC Mismatch: Observed  

**RootCause:**  
Subscriber radios programmed with mismatched Network Access Code (NAC).

**ResolutionSteps:**

1. Verified NAC on base station (0x293).  
2. Reprogrammed subscriber radios to match.  
3. Performed system‑wide configuration audit.  

**Notes:**  
P25 NAC mismatches prevent frame acceptance even when RF conditions are excellent.

---

## 🧩 Case 003 — NXDN: Excessive CRC Errors on Long Coax Run

**CaseId:** 003  
**ProtocolFamily:** NXDN 4800  
**Symptom:**  
Frequent CRC failures and dropped frames on repeater uplink.

**Context:**

- Environment: Industrial facility  
- Hardware: NXDN repeater with remote antenna  
- Configuration: 150 ft LMR‑400 coaxial feedline  

**ObservedSignals:**

- RSSI: –85 dBm  
- SNR: 18 dB  
- BER: 3–4%  
- CRC Errors: High  
- Cable Loss: ~6.5 dB measured  

**RootCause:**  
Excessive feedline loss causing marginal signal levels at repeater input.

**ResolutionSteps:**

1. Replaced LMR‑400 with LDF4‑50A hardline.  
2. Installed lightning arrestor with lower insertion loss.  
3. Re‑measured feedline loss (reduced to 2.1 dB).  

**Notes:**  
NXDN’s narrowband 4‑level FSK is highly sensitive to SNR degradation from cable loss.

---

## 🧩 Case 004 — DMR: Slot Timing Misalignment on Repeater

**CaseId:** 004  
**ProtocolFamily:** DMR Tier II  
**Symptom:**  
Subscriber radios unable to access Slot 2; Slot 1 operates normally.

**Context:**

- Environment: Rural repeater site  
- Hardware: Dual‑slot DMR repeater  
- Configuration: GPS timing disabled  

**ObservedSignals:**

- RSSI: –70 dBm  
- SNR: 25 dB  
- BER: <1%  
- Slot Timing Offset: ~1.8 ms  

**RootCause:**  
Repeater’s internal clock drifted, causing TDMA slot boundary misalignment.

**ResolutionSteps:**

1. Enabled GPS‑disciplined timing.  
2. Recalibrated internal oscillator.  
3. Verified slot alignment using service monitor.  

**Notes:**  
DMR TDMA requires strict 30 ms slot timing; drift >1 ms can cause slot access failures.

---

## 🧩 Case 005 — P25: Voice Garbling from IMBE Vocoder Mismatch

**CaseId:** 005  
**ProtocolFamily:** P25 Phase I  
**Symptom:**  
Voice transmissions sound garbled or robotic on receiving units.

**Context:**

- Environment: Public safety fleet  
- Hardware: Mixed vendor radios  
- Configuration: Some units using legacy IMBE parameters  

**ObservedSignals:**

- RSSI: –82 dBm  
- SNR: 20 dB  
- BER: 1–2%  
- CRC Errors: Low  
- Vocoder Mode: Mismatch detected  

**RootCause:**  
Subscriber radios using incompatible IMBE vocoder parameter sets.

**ResolutionSteps:**
 
1. Updated firmware on legacy radios.  
2. Standardized vocoder settings across fleet.  
3. Performed interoperability test.  

**Notes:**  
P25 vocoder mismatches often manifest as “robotic” or “underwater” audio despite good RF conditions.

---
