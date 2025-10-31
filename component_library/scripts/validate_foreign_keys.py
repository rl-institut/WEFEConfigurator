import os
import pandas as pd
import json

COMPONENT_TEMPLATES_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "WIP_components"))

# Paths
dp_json_path = os.path.join(COMPONENT_TEMPLATES_PATH, "datapackage.json")
profiles_csv_path = os.path.join(COMPONENT_TEMPLATES_PATH, "data", "sequences", "profiles.csv")

# Load datapackage.json
with open(dp_json_path, "r", encoding="utf-8") as f:
    dp_data = json.load(f)

# Load profile headers (first row) from profiles.csv
profiles_df = pd.read_csv(profiles_csv_path, sep=";", nrows=0)  # Read only headers
profile_headers = set(profiles_df.columns)  # Get column names (profile names)

print(f"Found {len(profile_headers)} profile headers in profiles.csv")

# Process each resource
for resource in dp_data.get("resources", []):
    resource_name = resource.get("name", "unknown")
    resource_path = os.path.join(COMPONENT_TEMPLATES_PATH, resource["path"])

    if not os.path.exists(resource_path):
        print(f"Skipping {resource_name}: file not found")
        continue

    # Skip the profiles resource itself
    if resource_name == "profiles":
        print(f"Skipping profiles resource (no self-reference needed)")
        continue

    df = pd.read_csv(resource_path, sep=";", dtype=str)

    if "schema" not in resource:
        resource["schema"] = {}
    if "foreignKeys" not in resource["schema"]:
        resource["schema"]["foreignKeys"] = []

    foreign_keys = resource["schema"]["foreignKeys"]

    # Track columns that already have foreign keys to profiles
    existing_profile_fks = {fk["fields"] for fk in foreign_keys
                           if fk.get("reference", {}).get("resource") == "profiles"}

    # Scan all columns in the CSV
    columns_with_matches = {}
    for col in df.columns:
        # Check if any value in this column matches a profile header
        for val in df[col].dropna():
            if str(val) in profile_headers:
                if col not in columns_with_matches:
                    columns_with_matches[col] = []
                columns_with_matches[col].append(str(val))

    # Add foreign keys for columns with matches
    for col, matched_profiles in columns_with_matches.items():
        if col not in existing_profile_fks:
            new_fk = {
                "fields": col,
                "reference": {
                    "resource": "profiles"
                }
            }
            foreign_keys.append(new_fk)
            print(f"✓ Added foreign key for '{resource_name}.{col}' → profiles (matched: {matched_profiles[0]})")
        else:
            print(f"  Skipped '{resource_name}.{col}' → already has foreign key to profiles")

# Save updated datapackage.json
with open(dp_json_path, "w", encoding="utf-8") as f:
    json.dump(dp_data, f, indent=4)

print("\n✓ Finished updating datapackage.json with foreign keys")


