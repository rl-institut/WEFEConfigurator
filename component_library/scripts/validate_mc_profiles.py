import pandas as pd
import os
import numpy as np

lib_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(lib_dir)

import os
import pandas as pd

csv_dir = os.path.join(lib_dir, "WIP_components", "data", "elements")

mc_names = []

base_profile_path = os.path.join(lib_dir, "WIP_components", "data", "sequences", "mc_profiles.csv")
base_profile_df = pd.DataFrame()

profile_path = os.path.join(lib_dir, "WIP_components", "data", "sequences", "profiles.csv")
profile_df = pd.read_csv(profile_path, sep=";")

possible_files = [
    "conversion.csv",
    "energy_conversion.csv",
    "hydropower.csv",
    "mimo.csv",
    "pv_panel.csv",
    "storage.csv",
    "toilets.csv",
    "volatile.csv",
    "wastewater_treatment.csv",
    "water_filtration.csv",
    "water_pumps.csv",
    "water_treatment.csv",
    "wind_turbine.csv",
    "dispatchable.csv",
    "energy_sources.csv",
    "water_sources.csv",
]

existing_files = [f for f in os.listdir(csv_dir) if f in possible_files]

for file in existing_files:
    file_path = os.path.join(csv_dir, file)
    df = pd.read_csv(file_path, sep=";")

    for i, name in enumerate(df["name"]):
        name_str = str(name).strip()
        if name_str.lower() == "name" or not name_str:
            continue
        mc_name = f"{name_str}_mc_profile"
        df.loc[i, "marginal_cost"] = mc_name
        mc_names.append(mc_name)

        profile_name = f"{name_str}_mc"
        profile_df[mc_name] = profile_name

        base_profile_df[profile_name] = pd.Series([0] * 8760, dtype=float)


    # df.to_csv(file_path, sep=";", index=False)
print(mc_names)

profile_df.to_csv(profile_path, sep=";", index=False)







