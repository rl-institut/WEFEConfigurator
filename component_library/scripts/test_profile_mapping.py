import os

import pandas as pd

scen_id = 1

# RELEVANT PATHS
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(script_dir))
scenario_dir = os.path.join(project_dir, "scenarios")
lib_dir = os.path.join(project_dir, "component_library")

# READ in DATA

# 1. weather data as downloaded
weather_df = pd.read_csv("weather_data.csv", sep=",")

# 2. component library profile mapping
lib_profiles_path = os.path.join(lib_dir, "WIP_components", "data", "sequences", "profiles.csv")
lib_profiles_df = pd.read_csv(lib_profiles_path, sep=";")

# 3. scenario profiles (final csv to be exported)
scen_profiles_path = os.path.join(scenario_dir, f"scenario_{scen_id}", "data", "sequences", "profiles.csv")
scen_profiles_df = pd.read_csv(scen_profiles_path, sep=";")


# Obtain necessary profiles from scenario profiles csv
profiles_to_add = list(scen_profiles_df.columns)

# Reindex scenario profiles according to weather data
scen_profiles_df = scen_profiles_df.reindex(range(len(weather_df)))

# Compare with profiles from library profiles csv and in case of a match, populate with mapped data from weather df
for profile in profiles_to_add:
    if profile in lib_profiles_df.columns:
        weather_data_match = lib_profiles_df[profile]
        scen_profiles_df[profile] = weather_df[weather_data_match]





