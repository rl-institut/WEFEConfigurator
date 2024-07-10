from .utils import AVAILABLE_COMPONENTS

def create_scenario(destination_folder):
    """Create a folder with the datapackage structure, the components and timeseries will be filled later on"""
    pass
def add_component(component_name, destination_folder, timeseries=None):
    """Add a component in the corresponding data/elements csv file.

    If timeseries is provided, then they will be append to related the data/sequences csv file
    (the file will be created if not existing yet)
    """
    if component_name in AVAILABLE_COMPONENTS:
        # TODO copy the component template in the destination folder
        if timeseries is not None:
            add_component_timeseries(component_name, destination_folder, timeseries)
    else:
        raise ValueError(f"The component {component_name} is not in the available component list {','.join([comp for comp in AVAILABLE_COMPONENTS])}")

 def add_component_timeseries(component_name, destination_folder, timeseries):
     """Timeseries will be append to related the data/sequences csv file under the destination folder

    The file will be created if not existing yet

     """
     pass