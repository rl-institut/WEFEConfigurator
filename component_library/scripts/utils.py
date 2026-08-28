import logging
import os
import pandas as pd

# TODO here the facades should only be imported from otp, to make sure they have
# validate_datapackage and processing_raw_inputs methods
from oemof_industry.mimo_converter import MIMO
from oemof_tabular_plugins.wefe.facades import PVPanel, MimoCrop
import datapackage as dp
import tableschema


COMPONENT_TEMPLATES_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "WIP_components"))
print(COMPONENT_TEMPLATES_PATH)

COMPONENTS_TYPEMAP = {
    "apv-system": MIMO,
    "pv_panel": PVPanel,
    "mimo-crop": MimoCrop
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
    dp_json = os.path.join(path, "datapackage.json")
    if os.path.exists(dp_json) is False:
        raise FileNotFoundError("The component library datapackage is not there, please generate it using 'python validate_component_lib.py' ")
    else:
        p0 = dp.Package(dp_json)


    component_to_csv_name_mappping = {}
    for r in p0.resources:
        logging.info(r.name)
        if "/elements/" in r.descriptor["path"]:
            category = r.name
            try:
                resource_data = pd.DataFrame.from_records(r.read(keyed=True))
            except tableschema.exceptions.CastError as err:
                if err.errors:
                    logging.error(f"The resource {category} has the following casting errors: {','.join([str(e) for e in err.errors])}")
                else:
                    logging.error(f"The resource {category} has the following casting error: {err}")
                resource_data = pd.DataFrame()

            if resource_data.empty is False:
                if len(resource_data.columns) == 1:
                    logging.warning(f"The resource {category} has only one field detected, this is usually the case when there is a mismatch of number of values between the headers row and the data rows, please check your file.")

                if category == "profiles":
                    import pdb;pdb.set_trace()

                for component_name in resource_data.name.values:
                    if component_name not in component_to_csv_name_mappping:
                        component_to_csv_name_mappping[component_name] = category
                    else:
                        raise ValueError(
                            f"The component {component_name} is listed under several categories: {component_to_csv_name_mappping[component_name]} and {category}")
            else:
                logging.warning(f"The resource {category} is empty")
    return component_to_csv_name_mappping

AVAILABLE_COMPONENTS = list_available_components()

def list_available_timeseries():
    """browse all components in all csv files and link component name to csv file name"""

    path = COMPONENT_TEMPLATES_PATH
    dp_json = os.path.join(path, "datapackage.json")
    if os.path.exists(dp_json) is False:
        raise FileNotFoundError("The component library datapackage is not there, please generate it using 'python validate_component_lib.py' ")
    else:
        p0 = dp.Package(dp_json)


    sequence_to_csv_name_mappping = {}
    for r in p0.resources:
        logging.info(r.name)
        if "/sequences/" in r.descriptor["path"]:
            category = r.name
            try:
                resource_data = pd.DataFrame.from_records(r.read(keyed=True))
            except tableschema.exceptions.CastError as err:
                if err.errors:
                    logging.error(f"The resource {category} has the following casting errors: {','.join([str(e) for e in err.errors])}")
                else:
                    logging.error(f"The resource {category} has the following casting error: {err}")
                resource_data = pd.DataFrame()

            if resource_data.empty is False:
                if len(resource_data.columns) == 1:
                    logging.warning(f"The resource {category} has only one field detected, this is usually the case when there is a mismatch of number of values between the headers row and the data rows, please check your file.")

                for component_name in resource_data.columns[1:]:
                    if component_name not in sequence_to_csv_name_mappping:
                        sequence_to_csv_name_mappping[component_name] = category
                    else:
                        raise ValueError(
                            f"The component {component_name} is listed under several categories: {sequence_to_csv_name_mappping[component_name]} and {category}")
            else:
                logging.warning(f"The resource {category} is empty")
    return sequence_to_csv_name_mappping

AVAILABLE_SEQUENCES = list_available_timeseries()

if __name__ == "__main__":
    print(AVAILABLE_COMPONENTS)
    print(AVAILABLE_SEQUENCES)
