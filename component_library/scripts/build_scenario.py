import os
import pandas as pd
import logging

from app.survey.survey import SURVEY_ANSWER_COMPONENT_MAPPING
from utils import AVAILABLE_COMPONENTS, COMPONENT_TEMPLATES_PATH
from analyse_survey import create_components_list

# TODO this needs to work standalone as well as a service


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

    scenario_component_folder = os.path.join(scenario_folder, "data")

    if component_name in AVAILABLE_COMPONENTS:
        fname = f"{AVAILABLE_COMPONENTS[component_name]}.csv"
        path = os.path.join(COMPONENT_TEMPLATES_PATH, "elements", fname)
        df = pd.read_csv(path, delimiter=";") # TODO change this to , instead of ;

        ofname = os.path.join(scenario_component_folder, "elements", fname)

        #strip the component documentation columns
        selected_columns = [col for col in df.columns if col not in ['verbose_name', 'description']]
        component_params = df.loc[df.name == component_name]
        component_params = component_params[selected_columns]

        if os.path.exists(ofname):
            category_df = pd.read_csv(ofname)
            if component_name not in category_df.name.values:
                category_df = pd.concat([category_df, component_params])
                category_df.to_csv(ofname, index=False)
            else:
                logging.warning(f"The component {component_name} was already defined in the target scenario {ofname}, not overwriting")
        else:
            component_params.to_csv(ofname, index=False)

        if timeseries is not None:
            add_component_timeseries(component_name, scenario_folder, timeseries)
    else:
        raise ValueError(f"The component {component_name} is not in the available component list {', '.join([comp for comp in AVAILABLE_COMPONENTS])}")


def add_component_timeseries(component_name, scenario_folder, timeseries):
    """Timeseries will be append to related the data/sequences csv file under the destination folder

    The file will be created if not existing yet
    """
    # TODO check the foreign keys between timeseries and component attributes are valid
    # i.e. that each of the component attribute value correspond to a timeseries header
    pass


def create_scenario_from_survey_data(survey_data, scenario_name, scenario_path):
    #component_list = create_components_list(survey_data) TODO update after survey data
    component_list = ["water-source", "desalinator", "solar-radiation", "apv-system"]
    # TODO scenario folder name could come from survey_data
    scenario_folder = os.path.join(scenario_path, scenario_name)
    create_scenario_folder(scenario_folder)

    for component in component_list:
        add_component(component, scenario_folder)

    # TODO read spec csv file and update the scenario values of the resources
    # TODO the specs csv file must have the same component names and component attribute names


class ScenarioBuilder:
    def __init__(self):
        self.mapping = SURVEY_ANSWER_COMPONENT_MAPPING
        self.components = {}

    def process_survey(self, survey):
        """
        Process the survey responses to build a nested structure. Some answers add components, while some change
        the attributes of the components. The output structure allows to change all attributes in the .csv files at
        once without editing them multiple times.
        Example output:
        {
            "wind_turbine": {"capacity": 10, "some_parameter": 5},
            "diesel_generator": {"fuel_efficiency": 0.8}
        }
        """
        for question_id, answer in survey.items():
            if answer is not None:
                question_id = question_id.strip("criteria_")

                if question_id in self.mapping:
                    # Check if it's a top-level question for adding components
                    try:
                        int_test = int(question_id)
                        component_map = self.mapping[question_id]
                        components_to_add = []
                        for component in answer:
                            if isinstance(component_map.get(component, None), list):
                                components_to_add.extend(component_map.get(component, None))
                            else:
                                components_to_add.append(component_map.get(component, None))

                        self.components.update({component: {} for component in components_to_add})
                    # If the number can't be parsed as an integer, it's a subquestion
                    except ValueError:
                        answer_mapping = self.mapping[question_id].keys()
                        for map in answer_mapping:
                            component, attribute = map.split("/")
                            try:
                                self.components[component][attribute] = answer
                            except KeyError:
                                 print(f"Could not add attribute {attribute} to {component}, because {component} was not found")





if __name__=="__main__":
    repo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "scenarios")
    create_scenario_from_survey_data({}, "test_scenario", repo_path)
