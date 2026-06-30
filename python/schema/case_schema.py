"""
PHASE 7 — SCHEMA VALIDATION
Validate cleaned case dictionaries against the canonical schema.
"""

# Canonical schema definition for a cleaned case object (pure Python)
CASE_SCHEMA = {
    "CaseId": (str, float),  # cleaned version converts to float
    "ProtocolFamily": str,
    "Symptom": str,
    "Context": {
        "Environment": str,
        "Hardware": str,
        "Configuration": str,
    },
    "ObservedSignals": {
        # REQUIRED FIELDS
        "RSSI_dBm": int,
        "SNR_dB": int,
        "BER_percent": float,
        "CRC_Errors": str,

        # OPTIONAL FIELDS (protocol-specific)
        "Jitter": (str, type(None)),
        "BER_peak_percent": (float, type(None)),
        "NAC_Mismatch": (bool, type(None)),
        "CableLoss_dB": (float, type(None)),
        "SlotTimingOffset_ms": (float, type(None)),
        "VocoderMismatch": (bool, type(None)),
    },
    "RootCause": str,
    "ResolutionSteps": [str],
    "Notes": str,
}


def validate_case_schema(case, schema, path="root"):
    print("# =====================================================================")
    print("PHASE 7 — SCHEMA VALIDATION")
    print('validate_case_schema(case, schema, path="root"):')
    print("# =====================================================================")
    print()    
    #Recursively validate a case dictionary against the provided schema.
    print(f"\nVALIDATING SCHEMA AT: {path}")
    print(f"Current CASE segment: {case}")
    print(f"Current SCHEMA segment: {schema}")

    # Iterate through each key/value pair in the canonical schema
    for key, expected_type in schema.items():

        print("\n------------------------------------------------------------")
        print(f"Checking key: {key}")
        print(f"Expected type definition: {expected_type}")
        print(f"Value present in case? {'YES' if key in case else 'NO'}")
        print("------------------------------------------------------------")

        # --------------------------------------------------------------
        # REQUIRED KEYS
        # --------------------------------------------------------------
        print(f"[DEBUG] REQUIRED KEY CHECK for {path}.{key}")
        print(f"  - isinstance(expected_type, dict)? {isinstance(expected_type, dict)}")
        print(f"  - isinstance(expected_type, list)? {isinstance(expected_type, list)}")
        print(f"  - not isinstance(expected_type, tuple)? {not isinstance(expected_type, tuple)}")

        if isinstance(expected_type, dict) or isinstance(expected_type, list) or not isinstance(expected_type, tuple):
            if key not in case:
                print(f"❌ Missing key: {path}.{key}")
                return False

        # --------------------------------------------------------------
        # OPTIONAL KEYS
        # --------------------------------------------------------------
        print(f"[DEBUG] OPTIONAL KEY CHECK for {path}.{key}")
        print(f"  - isinstance(expected_type, tuple)? {isinstance(expected_type, tuple)}")

        if isinstance(expected_type, tuple):
            if key not in case:
                print(f"✔ Optional key missing (allowed): {path}.{key}")
                continue

        # Retrieve the actual value from the case
        value = case.get(key)
        print(f"[DEBUG] Retrieved value for {path}.{key}: {value} (type: {type(value).__name__})")

        # --------------------------------------------------------------
        # NESTED DICTIONARY VALIDATION
        # --------------------------------------------------------------
        if isinstance(expected_type, dict):
            print(f"[DEBUG] NESTED DICT CHECK for {path}.{key}")
            print(f"  - isinstance(value, dict)? {isinstance(value, dict)}")

            if not isinstance(value, dict):
                print(f"❌ Expected dict at {path}.{key}, got {type(value).__name__}")
                return False

            print(f"[DEBUG] Recursing into nested dict at {path}.{key}")
            if not validate_case_schema(value, expected_type, path=f"{path}.{key}"):
                return False

        # --------------------------------------------------------------
        # LIST VALIDATION
        # --------------------------------------------------------------
        elif isinstance(expected_type, list):
            print(f"[DEBUG] LIST CHECK for {path}.{key}")
            print(f"  - isinstance(value, list)? {isinstance(value, list)}")

            if not isinstance(value, list):
                print(f"❌ Expected list at {path}.{key}, got {type(value).__name__}")
                return False

            element_type = expected_type[0]
            print(f"[DEBUG] Expected list element type: {element_type}")

            for idx, item in enumerate(value):
                print(f"[DEBUG] Checking list item {idx}: {item} (type: {type(item).__name__})")
                if not isinstance(item, element_type):
                    print(
                        f"❌ List element type mismatch at {path}.{key}[{idx}]: "
                        f"expected {element_type.__name__}, got {type(item).__name__}"
                    )
                    return False

        # --------------------------------------------------------------
        # SIMPLE TYPES (REQUIRED OR OPTIONAL)
        # --------------------------------------------------------------
        else:
            print(f"[DEBUG] SIMPLE TYPE CHECK for {path}.{key}")
            print(f"  - isinstance(expected_type, tuple)? {isinstance(expected_type, tuple)}")

            # OPTIONAL SIMPLE TYPE
            if isinstance(expected_type, tuple):
                print(f"[DEBUG] OPTIONAL SIMPLE TYPE for {path}.{key}")
                print(f"  - value is None? {value is None}")

                if value is None:
                    print(f"✔ Optional None allowed at {path}.{key}")
                    continue

                print(f"  - isinstance(value, expected_type)? {isinstance(value, expected_type)}")
                if not isinstance(value, expected_type):
                    print(
                        f"❌ Type mismatch at {path}.{key}: "
                        f"expected {expected_type}, got {type(value).__name__}"
                    )
                    return False

            # REQUIRED SIMPLE TYPE
            else:
                print(f"[DEBUG] REQUIRED SIMPLE TYPE for {path}.{key}")
                print(f"  - isinstance(value, expected_type)? {isinstance(value, expected_type)}")

                if not isinstance(value, expected_type):
                    print(
                        f"❌ Type mismatch at {path}.{key}: "
                        f"expected {expected_type.__name__}, got {type(value).__name__}"
                    )
                    return False

        print(f"✔ Valid: {path}.{key}")

    print(f"✅ Schema valid at: {path}")
    return True









