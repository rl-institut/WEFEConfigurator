#!/usr/bin/env python
"""
Quick test to verify water pump mappings are correct
"""
import json
import os

# Load the mapping file
mapping_file = "app/survey_answer_component_mapping_in_use.json"
with open(mapping_file, "r") as f:
    mapping = json.load(f)

# Test all 12 water pump variations
pump_patterns = [
    "3_GW", "3_DS", "3_RC", "3_L",
    "3_GWa", "3_DSa", "3_RCa", "3_La",
    "3_GWb", "3_DSb", "3_RCb", "3_Lb"
]

print("=" * 60)
print("WATER PUMP MAPPING VERIFICATION")
print("=" * 60)

all_correct = True

for pattern in pump_patterns:
    print(f"\n{pattern}:")

    # Check 3.X.1 - Component mapping
    key_1 = f"{pattern}.1"
    if key_1 in mapping:
        yes_components = mapping[key_1].get("map_answer", {}).get("Yes", [])
        if "water-pump" in yes_components:
            print(f"  ✓ {key_1}: Maps to 'water-pump'")
        else:
            print(f"  ✗ {key_1}: MISSING 'water-pump' mapping! Has: {yes_components}")
            all_correct = False
    else:
        print(f"  ✗ {key_1}: KEY NOT FOUND!")
        all_correct = False

    # Check 3.X.1.1 - pump_height attribute
    key_1_1 = f"{pattern}.1.1"
    if key_1_1 in mapping:
        attr = list(mapping[key_1_1].get("map_answer", {}).keys())
        if attr == ["pump_height"]:
            print(f"  ✓ {key_1_1}: Maps to 'pump_height'")
        else:
            print(f"  ✗ {key_1_1}: WRONG attribute! Has: {attr}")
            all_correct = False
    else:
        print(f"  ✗ {key_1_1}: KEY NOT FOUND!")
        all_correct = False

    # Check 3.X.1.4 - capacity attribute
    key_1_4 = f"{pattern}.1.4"
    if key_1_4 in mapping:
        attr = list(mapping[key_1_4].get("map_answer", {}).keys())
        if attr == ["capacity"]:
            print(f"  ✓ {key_1_4}: Maps to 'capacity'")
        else:
            print(f"  ✗ {key_1_4}: WRONG attribute! Has: {attr}")
            all_correct = False
    else:
        print(f"  ✗ {key_1_4}: KEY NOT FOUND!")
        all_correct = False

print("\n" + "=" * 60)
if all_correct:
    print("✓ ALL WATER PUMP MAPPINGS ARE CORRECT!")
else:
    print("✗ SOME MAPPINGS HAVE ISSUES - SEE ABOVE")
print("=" * 60)
