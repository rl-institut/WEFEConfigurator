from oemof.tabular.datapackage import building
import datapackage as dp
import os

COMPONENT_TEMPLATES_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "WIP_components"))

building.infer_metadata_from_data(
    package_name="WEFE component library",
    path=COMPONENT_TEMPLATES_PATH,
)
