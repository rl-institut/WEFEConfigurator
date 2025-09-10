import os

import numpy as np
import pandas as pd

scen_id = 1

# ------------ RELEVANT PATHS -------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(script_dir))
scenario_dir = os.path.join(project_dir, "scenarios")
lib_dir = os.path.join(project_dir, "component_library")

# ------------ CONVERSION COEFFICIENTS -------------------
c_j_to_kwh = 1 / 3600000

# ------------ READ IN DATA -------------------

# 1. weather data as downloaded
weather_df = pd.read_csv("weather_data.csv", sep=",")

# 2. component library profile mapping
lib_profiles_path = os.path.join(lib_dir, "WIP_components", "data", "sequences", "profiles.csv")
lib_profiles_df = pd.read_csv(lib_profiles_path, sep=";")

# 3. scenario profiles (final csv to be exported)
scen_profiles_path = os.path.join(scenario_dir, f"scenario_{scen_id}", "data", "sequences", "profiles.csv")
scen_profiles_df = pd.read_csv(scen_profiles_path, sep=";")


# ------------ PROCESS WEATHER DATA -------------------
# df["delta_i50b"] = df.apply(
#         lambda row: delta_i50b(
#             cum_temp=row["cum_temp"],
#             f_heat=row["f_heat"],
#             f_water=row["f_water"],
#             i50maxh=i50maxh,
#             i50maxw=i50maxw,
#         ),
#         axis=1,
#     ).cumsum()

weather_df["ghi"] = weather_df.apply(
    lambda row: row["ssrd"] * c_j_to_kwh, axis=1
)

weather_df["windspeed10"] = weather_df.apply(
    lambda row: np.sqrt(row["u10"]**2 + row["v10"]**2), axis=1
)

weather_df["windspeed100"] = weather_df.apply(
    lambda row: np.sqrt(row["u100"]**2 + row["v100"]**2), axis=1
)
# ------------ ADD WEATHER DATA TO SCENARIO -------------------

# Reindex scenario profiles according to weather data
weather_data_len = len(weather_df)
scen_profiles_df = scen_profiles_df.reindex(range(weather_data_len))

# If timeindex col exists: extract year (of first entry), else: set year to 2022 (according to weather data)
if "timeindex" in scen_profiles_df.columns:
    scen_profiles_df["timeindex"] = pd.to_datetime(scen_profiles_df["timeindex"])
    scen_profiles_year = int(scen_profiles_df["timeindex"].dt.year.iloc[0])
else:
    scen_profiles_year = int(2022)

# Add timeindex column in right format and length
timeindex = pd.date_range(
    start=f"{scen_profiles_year}-01-01",
    periods=weather_data_len,
    freq="h",
    tz="UTC"
)
scen_profiles_df["timeindex"] = timeindex.strftime("%Y-%m-%dT%H:%M:%SZ")

# Obtain necessary profiles from scenario profiles csv (ignore timeindex column)
profiles_to_add = [col for col in scen_profiles_df.columns if col != "timeindex"]

# Compare with profiles from library profiles csv and in case of a match, populate with mapped data from weather df
for profile in profiles_to_add:
    if profile in lib_profiles_df.columns:
        weather_data_match = str(lib_profiles_df[profile].iloc[0])
        if weather_data_match in weather_df.columns:
            scen_profiles_df[profile] = weather_df[weather_data_match]
        else:
            print(f"Profile '{profile}' is not in the available weather data. A dummy profile (series of 1) will be used.")
            dummy_series = pd.Series([1] * weather_data_len)
            scen_profiles_df[profile] = dummy_series
    else:
        print(f"Profile '{profile}' is not in the profile library. A dummy profile (series of 1) will be used.")
        scen_profiles_df[profile] = pd.Series([1] * weather_data_len)
debug = 13





