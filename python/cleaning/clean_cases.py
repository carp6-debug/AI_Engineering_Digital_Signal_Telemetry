"""
CLEANING MODULE — clean_cases.py
PROJECT: AI_ENGINEERING_DIGITAL_SIGNAL_TELEMETRY
PURPOSE: Clean normalized case dictionaries to prepare for schema validation
         and embedding generation.
"""

from typing import Any, Dict


def clean_case(case: Dict[str, Any]) -> Dict[str, Any]:
    print("# =====================================================================")
    print("PHASE 6 - CLEANING")
    print('clean_case(case)')
    print("# =====================================================================")
    new_case: Dict[str, Any] = {}

    for key, value in case.items():

        # 1. Clean numeric strings (must come before generic string handling)
        if isinstance(value, str) and value.replace(".", "", 1).isdigit():
            print("Clean Numeric Strings", value)
            new_case[key] = float(value)
            continue

        # 2. Clean strings
        if isinstance(value, str):
            cleaned = value.strip()
            print("Clean Strings", value)
            if cleaned == "":
                continue
            new_case[key] = cleaned
            continue

        # 3. Clean nested dictionaries
        if isinstance(value, dict):
            print("Clean Nested Dictionaries", value)
            new_case[key] = clean_case(value)
            continue

        # 4. Clean lists
        if isinstance(value, list):
            print("Clean Lists", value)
            new_list = []
            for item in value:
                print("Clean Item Value", value)
                if isinstance(item, str):
                    print("Clean Item String", value)
                    new_list.append(item.strip())
                else:
                    print("Append Item", value)
                    new_list.append(item)
            new_case[key] = new_list
            continue

        # 5. Default: copy unchanged
        new_case[key] = value

    return new_case




