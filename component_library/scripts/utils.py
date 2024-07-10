import logging
import os
from oemof_industry.mimo_converter import MIMO
from oemof_tabular_plugins.wefe.facades import PVPanel
import datapackage as dp

COMPONENT_TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data","elements")


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
    component_to_csv_name_mappping = {}

    # TODO collect all component names and their types

    # TODO fill the mapping

    return component_to_csv_name_mappping

AVAILABLE_COMPONENTS = list_available_components()

if __name__=="__main__":
    path = os.path.abspath(COMPONENT_TEMPLATES_PATH)
    print(path)
    p0 = dp.Package(base_path=path)
    p0.infer(os.path.join(path, "**" + os.sep + "*.csv"))
    p0.commit()
    p0.save(os.path.join(path, "datapackage.json"))


