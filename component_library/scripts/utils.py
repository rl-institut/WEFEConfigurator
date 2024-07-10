import logging
import os
import pandas as pd

# TODO here the facades should only be imported from otp, to make sure they have
# validate_datapackage and processing_raw_inputs methods
from oemof_industry.mimo_converter import MIMO
from oemof_tabular_plugins.wefe.facades import PVPanel
import datapackage as dp

COMPONENT_TEMPLATES_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"))


COMPONENTS_TYPEMAP = {
    "apv-system": MIMO,
    "pv_panel": PVPanel
}

def update_typemap(typemap, component_name):
    """Add the type of the component if existing in the list of components
    """

    if component_name in COMPONENTS_TYPEMAP:
        typemap[COMPONENTS_TYPEMAP[component_name]]
    else:
        # TODO check for oemof tabular builtin types
        logging.warning(f"The component {component_name} is not in the available component list {','.join([comp for comp in COMPONENTS_TYPEMAP])}")
    return typemap


def list_available_components():
    """browse all components in all csv files and link component name to csv file name"""

    path = COMPONENT_TEMPLATES_PATH
    p0 = dp.Package(base_path=path)
    p0.infer(os.path.join(path, "**" + os.sep + "*.csv"))
    p0.commit()
    component_to_csv_name_mappping = {}
    for r in p0.resources:
        category = r.name
        resource_data = pd.DataFrame.from_records(r.read(keyed=True))
        for component_name in resource_data.name.values:
            if component_name not in component_to_csv_name_mappping:
                component_to_csv_name_mappping[component_name] = category
            else:
                raise ValueError(
                    f"The component {component_name} is listed under several categories: {component_to_csv_name_mappping[component_name]} and {category}")

    return component_to_csv_name_mappping

AVAILABLE_COMPONENTS = list_available_components()
