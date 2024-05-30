import os
from oemof.solph import EnergySystem, Model
from oemof.solph.processing import parameter_as_dict

# ---- imports to be used when the package has been installed ----
from oemof.tabular import datapackage  # noqa
from oemof.tabular.facades import TYPEMAP

# ---- imports from oemof-tabular-plugins package ----
from oemof_tabular_plugins.general import (
    post_processing,
    CONSTRAINT_TYPE_MAP,
    pre_processing,
    logger,
)
from oemof_tabular_plugins.wefe.facades import PVPanel


# -------------- RELEVANT PATHS --------------
# get the project directory by navigating up one level from the current script file
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# -------------- USER INPUTS --------------
# list of scenarios to be evaluated
scenarios = ["general_basic"]
# weighted average cost of capital (WACC) - might move later
# this parameter is needed if CAPEX, OPEX fix and lifetime are included
wacc = 0.06

# -------------- ADDITIONAL FUNCTIONALITIES (OEMOF-TABULAR-PLUGINS) --------------
# include the custom attribute parameters to be included in the model
custom_attributes = ["emission_factor", "renewable_factor", "land_requirement"]
# set whether the multi-objective optimization should be performed
moo = False
# add PV Panel (from oemof-tabular-plugins) to facades type map (from oemof-tabular) - might move later
TYPEMAP["pv-panel"] = PVPanel

# -------------- RUNNING THE SCENARIOS --------------
for scenario in scenarios:
    print("Running scenario with datapackage {}".format(scenario))
    # set paths for scenario and result directories
    scenario_dir = os.path.join(project_dir, "scenarios", scenario)
    results_path = os.path.join(project_dir, "results", scenario, "output")
    # create results directory if it doesn't already exist
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    # pre-processing to update input csv files based on cost parameters: CAPEX, OPEX fix, lifetime, WACC
    pre_processing(scenario_dir, wacc, custom_attributes, moo)

    # create energy system object from the datapackage
    es = EnergySystem.from_datapackage(
        os.path.join(scenario_dir, "datapackage.json"),
        attributemap={},
        typemap=TYPEMAP,
    )
    logger.info("Energy system created from datapackage")

    # create model from energy system (this is just oemof.solph)
    m = Model(es)
    logger.info("Model created from energy system")

    # add constraints from datapackage to the model
    m.add_constraints_from_datapackage(
        os.path.join(scenario_dir, "datapackage.json"),
        constraint_type_map=CONSTRAINT_TYPE_MAP,
    )
    logger.info("Constraints added to model")

    # if you want dual variables / shadow prices uncomment line below
    # m.receive_duals()

    # select solver 'gurobi', 'cplex', 'glpk' etc
    m.solve("cbc")

    # extract parameters and results
    params = parameter_as_dict(es)
    results = m.results()

    post_processing(params, results, results_path)

print("done")
