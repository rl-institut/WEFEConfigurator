from .utils import AVAILABLE_COMPONENTS

def create_scenario(destination_folder):
    """Create a folder with the datapackage structure, the components and timeseries will be filled later on"""
    pass
def add_component(component_name, destination_folder):
    """Add a component to a new scenario"""
    if component_name in AVAILABLE_COMPONENTS:
        # TODO copy the component template in the destination folder
        pass
    else:
        raise ValueError(f"The component {component_name} is not in the available component list {','.join([comp for comp in AVAILABLE_COMPONENTS])}")
