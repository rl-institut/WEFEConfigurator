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

# Load actual profile values from profiles.csv
profiles_df = pd.read_csv(profiles_csv_path, sep=";")
profile_values = set(profiles_df.values.ravel())

# Process each resource
for resource in dp_data.get("resources", []):
    resource_path = os.path.join(COMPONENT_TEMPLATES_PATH, resource["path"])
    if not os.path.exists(resource_path):
        continue

    df = pd.read_csv(resource_path, sep=";", dtype=str)

    if "schema" not in resource:
        resource["schema"] = {}
    if "foreignKeys" not in resource["schema"]:
        resource["schema"]["foreignKeys"] = []

    foreign_keys = resource["schema"]["foreignKeys"]

    # Scan all columns in the CSV
    for col in df.columns:
        for val in df[col]:
            if str(val) in profile_values:
                print(f"Found match in column '{col}': {val}")
                break

# Save updated datapackage.json
with open(dp_json_path, "w", encoding="utf-8") as f:
    json.dump(dp_data, f, indent=4)

print("Finished (BUGGY) updating datapackage.json with foreign keys")


