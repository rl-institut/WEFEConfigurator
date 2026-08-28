"""
Generic country parameter template for WEFE component library updates.

NOTE:
Units for values in this template and the component library CSVs can be found in
the WEFEConfigurator documentation:
https://github.com/rl-institut/WEFEConfigurator

QUICK CUSTOMIZATION GUIDE:
1. COPY & SAVE AS: `{your_country}_params.py` (e.g., `kenya_params.py`, `germany_params.py`)
2. PLACE IN: `WEFEConfigurator/component_library/WIP_components/Country Specific Data/`
3. MODIFY: Change the numeric values below to match your country's data
4. CALL: In build_scenario.py → `update_component_library(COMPONENT_TEMPLATES_PATH, country="your_country")`

EXAMPLE:
- For Kenya: save as `kenya_params.py`, set `capex: 800.0` (local prices), call `country="kenya"`

The update script will:
- Update matching columns in `WIP_components/data/elements/*.csv`
- Skip missing CSVs/components/columns with warnings
- Log what changed (INFO level)

Structure: {csv_filename: {component_name: {column: value}}}
- csv_filename = name of CSV in elements/ folder
- component_name = value in CSV's 'name' column
- column/value = exact CSV column to update
"""

generic_country = {                         # ← RENAME to your_country (e.g., kenya)
    "composting_toilet": {
        "composting_toilet": {
            "carrier_cost": 0.,
            "annuity": 550.0,               # ← MODIFY THESE VALUES
            "capex": 1050.0,                # ← e.g., lower for local manufacturing
            "opex_fix": 40.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.15,
            "ghg_emission_factor": 0.065,
            "water_consumption_factor": 0.0
        }
    },

# ADVANCED: Add additional {column: value} entries ONLY if you understand
# the downstream impact on the model, using exact column names
# from the corresponding CSV in WIP_components/data/elements/.
# Example: "capacity_potential": float("inf"), "expandable": True, etc.

    "dry_toilet": {
        "dry_toilet": {
            "carrier_cost": 0.,
            "annuity": 400.0,
            "capex": 750.0,
            "opex_fix": 27.5,
            "lifetime": 15.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.20,
            "ghg_emission_factor": 0.06,
            "water_consumption_factor": 0.0
        }
    },
    "flush_toilet": {
        "flush_toilet": {
            "carrier_cost": 0.,
            "annuity": 800.0,
            "capex": 800.0,
            "opex_fix": 200.0,
            "lifetime": 15.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.15,
            "ghg_emission_factor": 0.075,
            "water_consumption_factor": 0.009
        }
    },
    "latrine": {
        "latrine": {
            "carrier_cost": 0.,
            "annuity": 175.0,
            "capex": 375.0,
            "opex_fix": 20.0,
            "lifetime": 10.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 1.0,
            "ghg_emission_factor": 0.35,
            "water_consumption_factor": 0.0
        }
    },
    "open_field": {
        "open_field": {
            "carrier_cost": 0.,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": None,
            "resource_cost": 0.0,
            "land_requirement_factor": 3.0,
            "ghg_emission_factor": 0.8,
            "water_consumption_factor": 0.0
        }
    },
    "wind_turbine": {
        "wind-turbine": {
            "carrier_cost": 0.,
            "resource_cost": 0.,
            "annuity": 0.0,
            "capex": 1600.0,
            "opex_fix": 35.0,
            "lifetime": 22.5,
            "land_requirement_factor": 2.5,
            "ghg_emission_factor": 0.02,
            "water_consumption_factor": 0.0,
            "ref_height": 100.0,
            "turbine_type": "aeolos-h_50kw"
        }
    },
    "pv_panel": {
        "pv-panel": {
            "carrier_cost": 0.0,
            "resource_cost": 0.0,
            "annuity": 0.0,
            "capex": 1500.0,
            "opex_fix": 15.0,
            "lifetime": 30.0,
            "land_requirement_factor": 1.5,
            "ghg_emission_factor": 0.04,
            "water_consumption_factor": 0.0,
            "pv_type": "boviet_450",
            "latitude": 30.0
        }
    },
    "energy_conversion": {
        "inverter": {
            "carrier_cost": 0.,
            "efficiency": 0.94,
            "annuity": 0.0,
            "capex": 350.0,
            "opex_fix": 15.0,
            "lifetime": 12.5,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.15,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "diesel-generator": {
            "carrier_cost": 0.,
            "efficiency": 0.35,
            "annuity": 0.0,
            "capex": 750.0,
            "opex_fix": 15.0,
            "lifetime": 17.5,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.075,
            "ghg_emission_factor": 0.7,
            "water_consumption_factor": 0.0
        },
        "biomass-cogeneration": {
            "carrier_cost": 0.,
            "efficiency": 0.25,
            "annuity": 0.0,
            "capex": 5500.0,
            "opex_fix": 80.0,
            "lifetime": 22.5,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.15,
            "ghg_emission_factor": 0.15,
            "water_consumption_factor": 0.0
        },
        "electrolyzer": {
            "carrier_cost": 0.,
            "efficiency": 0.7,
            "annuity": 0.0,
            "capex": 1750.0,
            "opex_fix": 45.0,
            "lifetime": 15.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.75,
            "ghg_emission_factor": 0.55,
            "water_consumption_factor": 0.0
        },
        "fuel-cell": {
            "carrier_cost": 0.,
            "efficiency": 0.5,
            "annuity": 0.0,
            "capex": 3500.0,
            "opex_fix": 60.0,
            "lifetime": 7.5,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.4,
            "ghg_emission_factor": 0.03,
            "water_consumption_factor": 0.0
        }
    },
    "water_pumps": {
        "groundwater-pump": {
            "annuity": 0.0,
            "capex": 400.0,
            "opex_fix": 15.0,
            "age": 0.0,
            "lifetime": 20.0,
            "carrier_cost": 0.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.2,
            "water_consumption_factor": 0.0,
            "land_requirement": 0.0,
            "ghg_emissions": 0.0,
            "water_footprint": 0.0
        },
        "seawater-pump": {
            "annuity": 0.0,
            "capex": 400.0,
            "opex_fix": 15.0,
            "age": 0.0,
            "lifetime": 20.0,
            "carrier_cost": 0.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.2,
            "water_consumption_factor": 0.0,
            "land_requirement": 0.0,
            "ghg_emissions": 0.0,
            "water_footprint": 0.0
        },
        "lake-water-pump": {
            "annuity": 0.0,
            "capex": 400.0,
            "opex_fix": 15.0,
            "age": 0.0,
            "lifetime": 20.0,
            "carrier_cost": 0.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.2,
            "water_consumption_factor": 0.0,
            "land_requirement": 0.0,
            "ghg_emissions": 0.0,
            "water_footprint": 0.0
        },
        "river-water-pump": {
            "annuity": 0.0,
            "capex": 400.0,
            "opex_fix": 15.0,
            "age": 0.0,
            "lifetime": 20.0,
            "carrier_cost": 0.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.2,
            "water_consumption_factor": 0.0,
            "land_requirement": 0.0,
            "ghg_emissions": 0.0,
            "water_footprint": 0.0
        }
    },
    "water_treatment_without": {
        "cartridge_filter": {
            "carrier_cost": 0.,
            "annuity": 300.0,
            "capex": 600.0,
            "opex_fix": 30.0,
            "lifetime": 15.0,
            "specific_energy_consumption": 0.06,
            "efficiency": 0.97,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.08,
            "ghg_emission_factor": 0.04,
            "water_consumption_factor": 0.0
        },
        "activated_carbon_filter": {
            "carrier_cost": 0.,
            "annuity": 400.0,
            "capex": 600.0,
            "opex_fix": 20.0,
            "lifetime": 10.0,
            "specific_energy_consumption": 0.05,
            "efficiency": 0.97,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.08,
            "ghg_emission_factor": 0.04,
            "water_consumption_factor": 0.008
        },
        "chlorination": {
            "carrier_cost": 0.,
            "annuity": 250.0,
            "capex": 700.0,
            "opex_fix": 35.0,
            "lifetime": 15.0,
            "specific_energy_consumption": 0.06,
            "efficiency": None,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.12,
            "ghg_emission_factor": 0.06,
            "water_consumption_factor": 0.008
        },
        "ceramic_filter": {
            "carrier_cost": 0.,
            "annuity": 200.0,
            "capex": 150.0,
            "opex_fix": 15.0,
            "lifetime": 8.0,
            "specific_energy_consumption": 0.02,
            "efficiency": 0.97,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.04,
            "ghg_emission_factor": 0.03,
            "water_consumption_factor": 0.0
        },
        "slow_sand_filter": {
            "carrier_cost": 0.,
            "annuity": 300.0,
            "capex": 700.0,
            "opex_fix": 20.0,
            "lifetime": 25.0,
            "specific_energy_consumption": 0.015,
            "efficiency": 0.98,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.5,
            "ghg_emission_factor": 0.06,
            "water_consumption_factor": 0.0
        },
        "uv_disinfection": {
            "carrier_cost": 0.,
            "annuity": 300.0,
            "capex": 700.0,
            "opex_fix": 40.0,
            "lifetime": 12.0,
            "specific_energy_consumption": 0.06,
            "efficiency": None,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.10,
            "ghg_emission_factor": 0.06,
            "water_consumption_factor": 0.005
        },
        "adsorption": {
            "carrier_cost": 0.,
            "annuity": 400.0,
            "capex": 700.0,
            "opex_fix": 30.0,
            "lifetime": 12.0,
            "specific_energy_consumption": 0.06,
            "efficiency": None,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.10,
            "ghg_emission_factor": 0.06,
            "water_consumption_factor": 0.008
        },
        "ion_exchange": {
            "carrier_cost": 0.,
            "annuity": 450.0,
            "capex": 1000.0,
            "opex_fix": 50.0,
            "lifetime": 12.0,
            "specific_energy_consumption": 0.06,
            "efficiency": 0.96,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.12,
            "ghg_emission_factor": 0.08,
            "water_consumption_factor": 0.04
        },
        "simple_oxidation": {
            "carrier_cost": 0.,
            "annuity": 250.0,
            "capex": 700.0,
            "opex_fix": 35.0,
            "lifetime": 15.0,
            "specific_energy_consumption": 0.07,
            "efficiency": None,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.08,
            "ghg_emission_factor": 0.06,
            "water_consumption_factor": 0.008
        },
        "ozonation": {
            "carrier_cost": 0.,
            "annuity": 700.0,
            "capex": 1200.0,
            "opex_fix": 50.0,
            "lifetime": 15.0,
            "specific_energy_consumption": None,
            "efficiency": None,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.12,
            "ghg_emission_factor": 0.08,
            "water_consumption_factor": 0.008
        },
        "photocatalysis": {
            "carrier_cost": 0.,
            "annuity": 600.0,
            "capex": 1200.0,
            "opex_fix": 45.0,
            "lifetime": 10.0,
            "specific_energy_consumption": 0.12,
            "efficiency": None,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.10,
            "ghg_emission_factor": 0.07,
            "water_consumption_factor": 0.008
        },
        "intake_structure": {
            "carrier_cost": 0.,
            "annuity": 200.0,
            "capex": 1000.0,
            "opex_fix": 20.0,
            "lifetime": 40.0,
            "specific_energy_consumption": 0.008,
            "efficiency": 0.98,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.20,
            "ghg_emission_factor": 0.01,
            "water_consumption_factor": 0.0
        },
        "coarse_bar_screen": {
            "carrier_cost": 0.,
            "annuity": 200.0,
            "capex": 700.0,
            "opex_fix": 20.0,
            "lifetime": 25.0,
            "specific_energy_consumption": 0.04,
            "efficiency": 0.90,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.12,
            "ghg_emission_factor": 0.03,
            "water_consumption_factor": 0.0
        },
        "coagulation_flocculation": {
            "carrier_cost": 0.,
            "annuity": 300.0,
            "capex": 700.0,
            "opex_fix": 20.0,
            "lifetime": 25.0,
            "specific_energy_consumption": 0.04,
            "efficiency": 0.95,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.3,
            "ghg_emission_factor": 0.05,
            "water_consumption_factor": 0.008
        },
        "boiling": {
            "carrier_cost": 0.,
            "annuity": 600.0,
            "capex": 1200.0,
            "opex_fix": 50.0,
            "lifetime": 15.0,
            "specific_energy_consumption": 0.80,
            "efficiency": 0.70,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.3,
            "ghg_emission_factor": 0.12,
            "water_consumption_factor": 0.02
        },
        "fine_screen": {
            "carrier_cost": 0.,
            "annuity": 250.0,
            "capex": 800.0,
            "opex_fix": 20.0,
            "lifetime": 25.0,
            "specific_energy_consumption": 0.04,
            "efficiency": 0.99,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.12,
            "ghg_emission_factor": 0.03,
            "water_consumption_factor": 0.0
        },
        "grit_chamber": {
            "carrier_cost": 0.,
            "annuity": 150.0,
            "capex": 700.0,
            "opex_fix": 20.0,
            "lifetime": 30.0,
            "specific_energy_consumption": 0.015,
            "efficiency": 0.98,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.20,
            "ghg_emission_factor": 0.03,
            "water_consumption_factor": 0.0
        }
    },
    "water_treatment_with_N2": {
        "biological_denitrification": {
            "carrier_cost": 0.,
            "annuity": 300.0,
            "capex": 1000.0,
            "opex_fix": 35.0,
            "lifetime": 20.0,
            "specific_energy_consumption": 0.008,
            "efficiency": None,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.8,
            "ghg_emission_factor": 0.04,
            "water_consumption_factor": 0.0
        }
    },
    "water_treatment_with_biomass": {
        "biofiltration": {
            "carrier_cost": 0.,
            "annuity": 300.0,
            "capex": 1000.0,
            "opex_fix": 40.0,
            "lifetime": 25.0,
            "specific_energy_consumption": 0.12,
            "efficiency": 0.85,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.06,
            "water_consumption_factor": 0.005
        }
    },
    "water_treatment_with_brine": {
        "microfiltration": {
            "carrier_cost": 0.,
            "annuity": 600.0,
            "capex": 1200.0,
            "opex_fix": 50.0,
            "lifetime": 12.0,
            "specific_energy_consumption": 0.20,
            "efficiency": 0.97,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.12,
            "ghg_emission_factor": 0.07,
            "water_consumption_factor": 0.04
        },
        "ultrafiltration": {
            "carrier_cost": 0.,
            "annuity": 700.0,
            "capex": 1300.0,
            "opex_fix": 50.0,
            "lifetime": 12.0,
            "specific_energy_consumption": 0.25,
            "efficiency": 0.98,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.12,
            "ghg_emission_factor": 0.07,
            "water_consumption_factor": 0.04
        },
        "nanofiltration": {
            "carrier_cost": 0.,
            "annuity": 1000.0,
            "capex": 2000.0,
            "opex_fix": 60.0,
            "lifetime": 12.0,
            "specific_energy_consumption": 0.50,
            "efficiency": 0.90,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.12,
            "ghg_emission_factor": 0.10,
            "water_consumption_factor": 0.08
        },
        "electrodialysis": {
            "carrier_cost": 0.,
            "annuity": 700.0,
            "capex": 1400.0,
            "opex_fix": 40.0,
            "lifetime": 15.0,
            "specific_energy_consumption": 0.90,
            "efficiency": 0.75,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.10,
            "ghg_emission_factor": 0.10,
            "water_consumption_factor": 0.008
        },
        "distillation": {
            "carrier_cost": 0.,
            "annuity": 700.0,
            "capex": 1400.0,
            "opex_fix": 55.0,
            "lifetime": 20.0,
            "specific_energy_consumption": 0.80,
            "efficiency": 0.70,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.3,
            "ghg_emission_factor": 0.12,
            "water_consumption_factor": 0.02
        },
        "membrane_distillation": {
            "carrier_cost": 0.,
            "annuity": 700.0,
            "capex": 1400.0,
            "opex_fix": 70.0,
            "lifetime": 15.0,
            "specific_energy_consumption": 5.0,
            "efficiency": 0.75,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.3,
            "ghg_emission_factor": 0.12,
            "water_consumption_factor": 0.01
        },
        "reverse_osmosis": {
            "carrier_cost": 0.,
            "annuity": 700.0,
            "capex": 1400.0,
            "opex_fix": 55.0,
            "lifetime": 12.0,
            "specific_energy_consumption": 1.2,
            "efficiency": 0.55,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.10,
            "ghg_emission_factor": 0.12,
            "water_consumption_factor": 0.5
        }
    },
    "storage": {
        "battery-storage": {
            "efficiency": 0.9,
            "annuity": 0.0,
            "capex": 850.0,
            "opex_fix": 20.0,
            "lifetime": 12.5,
            "resource_cost": 0.0,
            "land_requirement_factor": 3.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0,
            "invest_relation_output_capacity": 1.0,
            "invest_relation_input_output": 1.0
        },
        "drinking-water-storage": {
            "efficiency": 0.98,
            "annuity": 0.0,
            "capex": 300.0,
            "opex_fix": 7.5,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 1.5,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0,
            "invest_relation_output_capacity": 0.02,
            "invest_relation_input_output": 1.0
        },
        "service-water-storage": {
            "efficiency": 0.98,
            "annuity": 0.0,
            "capex": 186.0,
            "opex_fix": 2.5,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 1.7,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0,
            "invest_relation_output_capacity": 0.02,
            "invest_relation_input_output": 1.0
        }
    },
    "wastewater_treatment": {
        "constructed_wetland": {
            "carrier_cost": 0.,
            "annuity": 300.0,
            "capex": 600.0,
            "opex_fix": 25.0,
            "lifetime": 35.0,
            "specific_energy_consumption": 0.07,
            "efficiency": 0.90,
            "resource_cost": 0.0,
            "land_requirement_factor": 3.0,
            "ghg_emission_factor": 0.2,
            "water_consumption_factor": 0.02
        },
        "water_reuse_system": {
            "carrier_cost": 0.,
            "annuity": 1000.0,
            "capex": 2000.0,
            "opex_fix": 60.0,
            "lifetime": 25.0,
            "specific_energy_consumption": 0.90,
            "efficiency": 0.90,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.2,
            "ghg_emission_factor": 0.5,
            "water_consumption_factor": 0.04
        }
    },
    "wastewater_treatment_with_biomass": {
        "septic_system": {
            "carrier_cost": 0.,
            "annuity": 100.0,
            "capex": 200.0,
            "opex_fix": 30.0,
            "lifetime": 35.0,
            "specific_energy_consumption": 0.13,
            "efficiency": 0.70,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.1,
            "ghg_emission_factor": 0.050,
            "water_consumption_factor": 0.02
        },
        "centralized_WWTP": {
            "carrier_cost": 0.,
            "annuity": 625.0,
            "capex": 1400.0,
            "opex_fix": 50.0,
            "lifetime": 30.0,
            "specific_energy_consumption": 1.0,
            "efficiency": 0.92,
            "resource_cost": 0.0,
            "land_requirement_factor": 0.14,
            "ghg_emission_factor": 0.4,
            "water_consumption_factor": 0.02
        },
        "decentralized_WWTP": {
            "carrier_cost": 0.,
            "annuity": 275.0,
            "capex": 650.0,
            "opex_fix": 35.0,
            "lifetime": 25.0,
            "specific_energy_consumption": 0.35,
            "efficiency": 0.80,
            "resource_cost": 0.0,
            "land_requirement_factor": 1.0,
            "ghg_emission_factor": 0.1,
            "water_consumption_factor": 0.02
        }
    },
    "water_pipes": {
        "groundwater-pipe": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "seawater-pipe": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "lake-water-pipe": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "river-water-pipe": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "tap-water-pipe_DW": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "truck-water-pipe_DW": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "rain-water-pipe_DW": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "bottled-water-pipe_DW": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "tap-water-pipe_SW": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "truck-water-pipe_SW": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "rain-water-pipe_SW": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        },
        "bottled-water-pipe_SW": {
            "carrier_cost": 0.0,
            "efficiency": 1.0,
            "annuity": 0.0,
            "capex": 0.0,
            "opex_fix": 0.0,
            "lifetime": 20.0,
            "resource_cost": 0.0,
            "land_requirement_factor": 2.0,
            "ghg_emission_factor": 0.0,
            "water_consumption_factor": 0.0
        }
    }
}