import logging
from oemof_industry.mimo_converter import MIMO

COMPONENTS_TYPEMAP = {
    "apv-system": MIMO,
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