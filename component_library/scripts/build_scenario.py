import os

from utils import AVAILABLE_COMPONENTS
from analyse_survey import create_components_list



def create_scenario_folder(destination_folder):
    """Create a folder with the datapackage structure, the components and timeseries will be filled later on"""
    if os.path.exists(destination_folder):
        pass
    else:
        os.makedirs(destination_folder)
        os.makedirs(os.path.join(destination_folder,"scripts"))
        os.makedirs(os.path.join(destination_folder,"data","elements"))
        os.makedirs(os.path.join(destination_folder,"data","sequences"))


def add_component(component_name, scenario_folder, timeseries=None):
    """Add a component in the corresponding data/elements csv file.

    If timeseries is provided, then they will be append to related the data/sequences csv file
    (the file will be created if not existing yet)
    """

    scenario_component_folder = os.path.join(scenario_folder, "data", "elements")

    if component_name in AVAILABLE_COMPONENTS:
        # TODO copy the component template in the scenario_component_folder
        if timeseries is not None:
            add_component_timeseries(component_name, scenario_folder, timeseries)
    else:
        raise ValueError(f"The component {component_name} is not in the available component list {','.join([comp for comp in AVAILABLE_COMPONENTS])}")

def add_component_timeseries(component_name, scenario_folder, timeseries):
    """Timeseries will be append to related the data/sequences csv file under the destination folder

    The file will be created if not existing yet
    """
    # TODO check the foreign keys between timeseries and component attributes are valid
    # i.e. that each of the component attribute value correspond to a timeseries header
    pass

def create_scenario_from_survey_data(survey_data, scenario_name, scenario_path):
    component_list = create_components_list(survey_data)
    scenario_folder = os.path.join(scenario_path, scenario_name)

    create_scenario_folder(scenario_folder)


    for component in component_list:
        add_component(component, scenario_folder)

if __name__=="__main__":
    repo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "scenarios")
    create_scenario_from_survey_data({}, "test_scenario", repo_path)
