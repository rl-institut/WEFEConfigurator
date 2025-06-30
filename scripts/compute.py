import os
from oemof.solph import EnergySystem, Model
from oemof.solph import processing
from oemof.solph.processing import parameter_as_dict

# TODO this should be with from oemof.tabular.datapackage import building when https://github.com/oemof/oemof-tabular/pull/173 is merged
from oemof_tabular_plugins.script import compute_scenario

# ---- imports to be used when the package has been installed ----
from oemof.tabular import datapackage  # noqa

from oemof_tabular_plugins.wefe import WEFE_TYPEMAP as TYPEMAP



parameters_units = {
    "drinking-water-storage": "[m³]",
    "total_annual_cost_moo": "[USD/a]",
    "rainwater-harvesting": "[m²]",
    "service-water-storage": "[m³]",
    "sw-ro": "[m³/h]",
    "seawater-reverse-osmosis": "[m³/h]",
    "electricity-grid": "[kWh]",
    "seawater": "[m³]",
    "seawater-source": "[m³]",
    "water-truck": "[m³]",
    "battery-storage": "[kWh]",
    "inverter": "[kW]",
    "water-filtration": "[m³/h]",
    "water-filtration-system": "[m³/h]",
    "water-pump": "[m³/h]",
    "river-water-uptake": "[m³/h]",
    "crop": "[m²]",
    "banana": "[m²]",
    "banana-production": "[kg/a]",
    "groundwater": "[m³]",
    "bottled-water": "[m³]",
    "diesel-generator": "[kW]",
    "photovoltaics": "[kWp]",
    "wind-turbine": "[kW]",
    "hydropower": "[kW]",
    "pv-panel": "[kW]",
    "water-storage": "[m³]",
    "mimo": "[m³/h]",
    "annuity_total": "[USD/a]",
    "variable_costs_total": "[USD/a]",
    "ghg_emission_total": "[kgCO2e/a]",
    "ghg_emissions_total": "[kgCO2e/a]",
    "system_cost_total": "[USD/a]",
    "land_requirement_additional": "[m²]",
    "total_upfront_investments": "[USD]",
    "land_requirement_total": "[m²]",
    "total_water_footprint": "[m³]",
    "system_opex_total": "[USD/a]",
    "total_variable_cost_moo": "[USD/a]",
    "total_water_consumption": "[m³/a]",
    "total_indirect_water_consumption": "[m³/a]",
    "ac-elec": "[kWh]",
    "water_scarcity_footprint": "[m³]",
}

# -------------- RELEVANT PATHS --------------
# get the project directory by navigating up one level from the current script file
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# -------------- USER INPUTS --------------
# list of scenarios to be evaluated
scenarios = [
    # "general_add_cost_inputs",
    # "general_basic",
    # "general_constraints",
    # "general_custom_attributes",
    # "wefe_custom_attributes",
    # "wefe_pv_panel",
    # "wefe_reverse_osmosis",
    # "aiwa"
    "aiwa_vivek"
    #"aiwa_8760"
    # "arusi_8760"
    # "arusi_24"
]
# Regionalized Characterisation Factor for Available water remaining (AWARE) - might move later;
# this parameter is needed to calculate the regionalized water scarcity footprint in moo.
# weighted average cost of capital (WACC) - might move later
# this parameter is needed if CAPEX, OPEX fix and lifetime are included
wacc = 0.06

# -------------- ADDITIONAL FUNCTIONALITIES (OEMOF-TABULAR-PLUGINS) --------------
# include the custom attribute parameters to be included in the model
# this can be moved somewhere and included in a dict or something similar with all possible additional attributes
custom_attributes = [
    "ghg_emission_factor",
    "renewable_factor",
    "land_requirement_factor",
    "water_consumption_factor",
    "indirect_water_consumption_factor" "land_requirement",
    "water_footprint",
    "ghg_emissions",
    "resource_cost",
    "annuity",
]
# set whether the multi-objective optimization should be performed
moo = False

# -------------- RUNNING THE SCENARIOS --------------
for scenario in scenarios:
    print("Running scenario with datapackage {}".format(scenario))
    # set paths for scenario and result directories
    scenario_dir = os.path.join(project_dir, "scenarios", scenario)
    results_path = os.path.join(project_dir, "results", scenario, "output")

    calculator = compute_scenario(
        scenario_dir,
        results_path,
        wacc,
        scenario_name=scenario,
        custom_attributes=custom_attributes,
        typemap=TYPEMAP,
        moo=moo,
        dash_app=True,
        parameters_units=parameters_units,
    )
    df = calculator.df_results
    print(df)
    print(calculator.raw_outputs)
    print(calculator.calculated_outputs)
    print(calculator.raw_inputs)
    import pdb

    pdb.set_trace()


print("done")
