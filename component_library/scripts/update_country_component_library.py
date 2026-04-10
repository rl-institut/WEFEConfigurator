import os
import logging
import pandas as pd

def update_component_library(component_lib_dir, country):
    """
    Update component library CSVs with country-specific parameter values.

    For each entry in the country params dict, opens the corresponding CSV,
    finds the row matching the component name, and updates the specified columns.

    :param component_lib_dir: path to the folder containing component CSV files
    :param country: filename prefix of the country params python dictionary
                    (expects {country}_params.py)
    """
    from importlib.util import spec_from_file_location, module_from_spec
    logging.getLogger().setLevel(logging.INFO)

    country_params_path = os.path.join(component_lib_dir, "Country Specific Data", f"{country}_params.py")
    elements_dir = os.path.join(component_lib_dir, "data", "elements")

    # Load the user's country_params.py file

    if not os.path.exists(country_params_path):
        logging.warning(f"No country params file found at '{country_params_path}'. Skipping update.")
        return

    spec = spec_from_file_location("country_params", country_params_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    country_params = module.generic_country

    if hasattr(module, 'generic_country'):
        logging.info(f"Loaded country params successfully: {len(country_params)} CSV groups")
    else:
        logging.error("No 'generic_country' dict found in the params file!")
        return

    def _values_differ(old_value, new_value):
        """Compare two values robustly across all pandas/CSV data types."""
        if pd.isna(old_value) or old_value is None:
            return True
        if isinstance(new_value, (int, float)):
            return float(old_value) != float(new_value)
        if isinstance(new_value, str):
            return str(old_value).strip() != new_value.strip()
        if isinstance(new_value, bool):
            return bool(old_value) != new_value
        if isinstance(new_value, dict):
            return str(old_value) != str(new_value)
        return old_value != new_value

    # Update Component Library CSVs with Parameters from the Country File/Template

    for csv_name, components in country_params.items():
        logging.info(f"Processing CSV: {csv_name}.csv")

        csv_path = os.path.join(elements_dir, f"{csv_name}.csv")

        if not os.path.exists(csv_path):
            logging.warning(f"CSV '{csv_name}.csv' not found. Skipping.")
            continue

        df = pd.read_csv(csv_path, sep=";")
        logging.info(f"Loaded CSV with {len(df)} rows")

        for component_name, columns in components.items():
            logging.debug(f"Checking component: {component_name}")

            mask = df["name"] == component_name

            if not mask.any():
                logging.warning(f"Component '{component_name}' not found. Skipping.")
                continue

            logging.debug(f"Found {mask.sum()} matching rows for '{component_name}'")

            num_columns = len(columns)
            num_updated = 0

            for col, value in columns.items():
                logging.debug(f"Column: {col} = {value}")

                if col not in df.columns:
                    logging.warning(f"Column '{col}' not in CSV. Skipping.")
                    continue

                old_value = df.loc[mask, col].iloc[0]

                if _values_differ(old_value, value):
                    df.loc[mask, col] = value
                    num_updated += 1
                    logging.info(f"Updated {col}: {old_value} → {value}")
                else:
                    logging.debug(f"No change needed for {col}")

            logging.info(f"Updated {num_updated}/{num_columns} columns for '{component_name}'")

        df.to_csv(csv_path, sep=";", index=False)
        logging.info(f"Completed '{csv_name}.csv'")

    logging.info("Component library update complete.")