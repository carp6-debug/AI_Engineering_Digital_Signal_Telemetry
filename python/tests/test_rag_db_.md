(rad_ai_env) D:\DEVELOPMENT\Projects\AI_Engineering_Digital_Signal_Telemetry\python>python test_rag_db_endpoint.py

```code
STATUS: 200
RESPONSE: {
  "retrievedChunks": [
    {
      "chunkText": "CaseId: 1.0\nProtocolFamily: DMR Tier II\nSymptom: Intermittent audio dropouts during voice transmission, especially when mobile unit is in motion.\nRootCause: Multipath reflections causing symbol timing errors and elevated BER.\nNotes: DMR\u00c3\u00a2\u00e2\u201a\u00ac\u00e2\u201e\u00a2s 4-FSK modulation is sensitive to multipath in dense urban environments. BER > 5% typically results in audible artifacts or dropouts.\nContext:\n  Environment: Urban area with reflective surfaces\n  Hardware: Handheld DMR radio, 4W output\n  Configuration: Repeater-linked, 12.5 kHz channel spacing\nObservedSignals:\n  RSSI_dBm: -92\n  SNR_dB: 14\n  BER_percent: 5.0\n  BER_peak_percent: 10.0\n  CRC_Errors: Frequent\n  Jitter: Moderate\nResolutionSteps:\n  - Enabled receiver equalization mode.\n  - Adjusted antenna orientation to reduce reflective path dominance.\n  - Relocated repeater antenna to improve line-of-sight coverage.",
      "caseId": "1.0"
    },
    {
      "chunkText": "CaseId: 4.0\nProtocolFamily: DMR Tier II\nSymptom: Subscriber radios unable to access Slot 2; Slot 1 operates normally.\nRootCause: Repeater\u00c3\u00a2\u00e2\u201a\u00ac\u00e2\u201e\u00a2s internal clock drifted, causing TDMA slot boundary misalignment.\nNotes: DMR TDMA requires strict 30 ms slot timing; drift >1 ms can cause slot access failures.\nContext:\n  Environment: Rural repeater site\n  Hardware: Dual-slot DMR repeater\n  Configuration: GPS timing disabled\nObservedSignals:\n  RSSI_dBm: -70\n  SNR_dB: 25\n  BER_percent: 1.0\n  CRC_Errors: Low\n  SlotTimingOffset_ms: 1.8\nResolutionSteps:\n  - Enabled GPS-disciplined timing.\n  - Recalibrated internal oscillator.\n  - Verified slot alignment using service monitor.",
      "caseId": "4.0"
    },
    {
      "chunkText": "CaseId: 3.0\nProtocolFamily: NXDN 4800\nSymptom: Frequent CRC failures and dropped frames on repeater uplink.\nRootCause: Excessive feedline loss causing marginal signal levels at repeater input.\nNotes: NXDN\u00c3\u00a2\u00e2\u201a\u00ac\u00e2\u201e\u00a2s narrowband 4-level FSK is highly sensitive to SNR degradation from cable loss.\nContext:\n  Environment: Industrial facility\n  Hardware: NXDN repeater with remote antenna\n  Configuration: 150 ft LMR-400 coaxial feedline\nObservedSignals:\n  RSSI_dBm: -85\n  SNR_dB: 18\n  BER_percent: 3.5\n  CRC_Errors: High\n  CableLoss_dB: 6.5\nResolutionSteps:\n  - Replaced LMR-400 with LDF4-50A hardline.\n  - Installed lightning arrestor with lower insertion loss.\n  - Re-measured feedline loss (reduced to 2.1 dB).",
      "caseId": "3.0"
    },
    {
      "chunkText": "CaseId: 2.0\nProtocolFamily: P25 Phase I\nSymptom: Receiver fails to decode voice frames; displays 'INVALID NAC' error.\nRootCause: Subscriber radios programmed with mismatched Network Access Code (NAC).\nNotes: P25 NAC mismatches prevent frame acceptance even when RF conditions are excellent.\nContext:\n  Environment: Dispatch center\n  Hardware: P25 base station receiver\n  Configuration: Mixed fleet of subscriber radios\nObservedSignals:\n  RSSI_dBm: -78\n  SNR_dB: 22\n  BER_percent: 1.0\n  CRC_Errors: None\n  NAC_Mismatch: True\nResolutionSteps:\n  - Verified NAC on base station (0x293).\n  - Reprogrammed subscriber radios to match.\n  - Performed system-wide configuration audit.",
      "caseId": "2.0"
    },
    {
      "chunkText": "CaseId: 5.0\nProtocolFamily: P25 Phase I\nSymptom: Voice transmissions sound garbled or robotic on receiving units.\nRootCause: Subscriber radios using incompatible IMBE vocoder parameter sets.\nNotes: P25 vocoder mismatches often manifest as 'robotic' or 'underwater' audio despite good RF conditions.\nContext:\n  Environment: Public safety fleet\n  Hardware: Mixed vendor radios\n  Configuration: Some units using legacy IMBE parameters\nObservedSignals:\n  RSSI_dBm: -82\n  SNR_dB: 20\n  BER_percent: 1.5\n  CRC_Errors: Low\n  VocoderMismatch: True\nResolutionSteps:\n  - Updated firmware on legacy radios.\n  - Standardized vocoder settings across fleet.\n  - Performed interoperability test.",
      "caseId": "5.0"
    }
  ],
  "similarityScores": [
    {
      "value": 0.6943125620246501,
      "isHighConfidence": false
    },
    {
      "value": 0.6723900374697219,
      "isHighConfidence": false
    },
    {
      "value": 0.6479927777370516,
      "isHighConfidence": false
    },
    {
      "value": 0.6097676712226802,
      "isHighConfidence": false
    },
    {
      "value": 0.5954107436594026,
      "isHighConfidence": false
    }
  ],
  "caseMetadata": [
    {
      "caseId": "1.0",
      "protocolFamily": "DMR Tier II",
      "symptom": "Intermittent audio dropouts during voice transmission, especially when mobile unit is in motion.",
      "environment": "Urban area with reflective surfaces",
      "hardware": "Handheld DMR radio, 4W output"
    },
    {
      "caseId": "4.0",
      "protocolFamily": "DMR Tier II",
      "symptom": "Subscriber radios unable to access Slot 2; Slot 1 operates normally.",
      "environment": "Rural repeater site",
      "hardware": "Dual-slot DMR repeater"
    },
    {
      "caseId": "3.0",
      "protocolFamily": "NXDN 4800",
      "symptom": "Frequent CRC failures and dropped frames on repeater uplink.",
      "environment": "Industrial facility",
      "hardware": "NXDN repeater with remote antenna"
    },
    {
      "caseId": "2.0",
      "protocolFamily": "P25 Phase I",
      "symptom": "Receiver fails to decode voice frames; displays 'INVALID NAC' error.",
      "environment": "Dispatch center",
      "hardware": "P25 base station receiver"
    },
    {
      "caseId": "5.0",
      "protocolFamily": "P25 Phase I",
      "symptom": "Voice transmissions sound garbled or robotic on receiving units.",
      "environment": "Public safety fleet",
      "hardware": "Mixed vendor radios"
    }
  ]
}
```

(rad_ai_env) D:\DEVELOPMENT\Projects\AI_Engineering_Digital_Signal_Telemetry\python>