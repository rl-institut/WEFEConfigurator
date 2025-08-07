import os

import numpy as np
import pandas as pd
import logging
import json

from app.survey.survey import SUB_QUESTION_MAPPING
from utils import AVAILABLE_COMPONENTS, COMPONENT_TEMPLATES_PATH
from analyse_survey import create_components_list

# TODO this needs to work standalone as well as a service

#-------------RELEVANT PATHS------------
# they may be changed if this script is moved somewhere else...
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(script_dir))
scenario_dir = os.path.join(project_dir, "scenarios")
lib_dir = os.path.join(project_dir, "component_library")

#-------SURVEY MAPPING----------
TYPE_FLOAT = "float"
TYPE_INT = "int"
TYPE_STRING = "string"
TYPE_WATER = "string"
INFOBOX = "description"

TYPE_COMPONENT = "component"
TYPE_COMPONENT_ATTRIBUTE = "attribute"
TYPE_NO_MAP = "skip"

type_check = {
    TYPE_FLOAT: float,
    TYPE_INT: int,
    TYPE_STRING: str,
}

# Later direct imports without .json
with open(os.path.join(project_dir, "app", "commented_mapping.json"),"r") as fp:
    SURVEY_ANSWER_COMPONENT_MAPPING= json.load(fp)


class ScenarioBuilder:
    def __init__(self):
        self.name = "test_scenario" # should be updated based on scenario
        self.mapping = SURVEY_ANSWER_COMPONENT_MAPPING
        self.subq_mapping = SUB_QUESTION_MAPPING
        self.components = {}
        self.scenario_folder = self.create_scenario_folder()


    def create_scenario_folder(self, destination_path=scenario_dir):
        """Create a folder with the datapackage structure, the components and timeseries will be filled later on"""
        scenario_folder = os.path.join(destination_path, self.name)
        if os.path.exists(scenario_folder):
            pass
        else:
            os.makedirs(scenario_folder)
            os.makedirs(os.path.join(scenario_folder, "scripts"))
            os.makedirs(os.path.join(scenario_folder, "data", "elements"))
            os.makedirs(os.path.join(scenario_folder, "data", "sequences"))

        return scenario_folder

    def process_survey(self, survey):
        """
        Process the survey responses to build a nested structure. Some answers add components, while some change
        the attributes of the components. The output structure allows to change all attributes in the .csv files at
        once without editing them multiple times.
        Example output:
        {
            "wind-turbine": {"capacity": 10, "some_parameter": 5},
            "diesel-generator": {"fuel_efficiency": 0.8}
        }
        """
        for question_id, answer in survey.items():
            # 2 options for answer:
            # option 1: list -> turn all TYPE_COMPONENT answers into list
            # option 2: single item (None, float, str) -> assume all TYPE_COMPONENT_ATTRIBUTE answers to be single items
            if answer is not None:
                # obtain question_id
                question_id = question_id.strip("criteria_")

                if question_id in self.mapping:
                    map_to, map_answer = next(iter(self.mapping[question_id].items()))
                    """
                    in general 3 options for map_answer (always dict):
                    option 1: {str1: list, str2: list, ...} -> for components
                    option 2: {str: list} -> not applicable at all (modify to align with option 1)
                    option 3: {str: str} -> for attributes
                    keys can be component_name, attribute_name, bool (related to some attribute/component)
                    """

                    if map_to == TYPE_COMPONENT:
                        components_to_add = []

                        # Align answer structure: Should always be of type "list" to match component mapping
                        answer = [answer] if not isinstance(answer, list) else answer

                        for a in answer:
                            # option 1: all "normal" components are keys in map_what
                            if a in map_answer:
                                components_to_add.extend(map_answer[a])

                            # option 2: so far not applicable for components -> dismiss

                            # option 3: "other" components are just given as user input (string) -> delete
                            # TODO: this will create user-defined component which is hard to handle,
                            #  questions where users insert components as strings should not be used in ESM directly,
                            #  "other" can be option to choose (tick) though with "other" in component_lib
                            else:
                                components_to_add.append(str(a))
                            # another condition to catch errors

                        self.components.update({component: {} for component in components_to_add})

                    elif map_to == TYPE_COMPONENT_ATTRIBUTE:
                        if question_id in self.subq_mapping:
                            # Obtain parent question_id and answer to link attribute to its component
                            parent_qid, parent_answer = self.subq_mapping[question_id]

                            # Align answer structure: Should always be single item to match attribute mapping
                            answer = answer[0] if isinstance(answer, list) else answer
                            # some debugging if answer is list longer than 1

                            # option 1: so far not applicable for attributes -> dismiss

                            # option 2: no idea yet how these attributes should be linked to a component
                            # example for opt 2: question 4.2, map_answer = {'water_metals': ['Arsenic', 'Lead', 'Mercury', 'Cadmium', 'Iron']}
                            # TODO: Modify these questions to be TYPE_COMPONENT formatted according to option 1

                            # option 3:
                            (attribute_name, attribute_type), = map_answer.items()
                            attribute_val = type_check[attribute_type](answer)

                            target_components = self.mapping[parent_qid][TYPE_COMPONENT][parent_answer]

                            for target_component in target_components:
                                self.components[target_component] = {attribute_name: attribute_val}
                                #some debugging for key error
                        else:
                            # TODO: Check if TYPE_COMPONENT_ATTRIBUTE questions are always subquestions of a TYPE_COMPONENT question
                            pass

                    elif map_to == TYPE_NO_MAP:
                        # Don't know what to do with this
                        pass
                    else:
                        print(f"Question {question_id} has unexpected key {map_to} that can't be mapped.")
                        pass


    def add_components(self):
        # TODO: does not add components that are not in AVAILABLE_COMPONENTS (component: "other")
        """
        Add all components and their corresponding attributes from the survey to the corresponding csv files. If a
        folder for the scenario doesn't exist, it will be created. If it does, the components and corresponding
        attributes will be updated
        """

        scenario_component_folder = os.path.join(self.scenario_folder, "data")

        for component in self.components:
            if component in AVAILABLE_COMPONENTS:
                fname = f"{AVAILABLE_COMPONENTS[component]}.csv"
                path = os.path.join(COMPONENT_TEMPLATES_PATH, "elements", fname)
                df = pd.read_csv(path, delimiter=";", index_col="name") # TODO change this to , instead of ;

                ofname = os.path.join(scenario_component_folder, "elements", fname)

                # Strip the component documentation columns
                selected_columns = [col for col in df.columns if col not in ['verbose_name', 'description']]
                component_params = df.loc[component]
                component_params = component_params[selected_columns]

                if os.path.exists(ofname):
                    category_df = pd.read_csv(ofname, index_col="name")
                    if component not in category_df.index:
                        # If the component doesn't exist, add a row for the component
                        component_df = component_params.to_frame().T
                        category_df = pd.concat([category_df, component_df])
                    else:
                        # If the component already exists, only update the attributes
                        component_params = category_df.loc[component]
                        category_df.loc[component] = self.update_component_attributes(component_params)
                    # Save the components back to the csv file
                    category_df.to_csv(ofname, index_label="name")


                else:
                    # Edit the attributes in the csv file if they have been set in the survey
                    component_params = self.update_component_attributes(component_params)
                    component_df = component_params.to_frame().T
                    component_df.to_csv(ofname, index_label="name")

            else:
                logging.warning(f"The component {component} is not in the available component list {', '.join([comp for comp in AVAILABLE_COMPONENTS])}")


    def update_component_attributes(self, component_params):
        """
        Edit the component attributes in the corresponding .csv file based on the component attributes set in
        self.components.
        :param component_params: DataSeries object containing the .csv row of parameters for the corresponding component
        :returns: component_params DataSeries updated according to attributes in self.components[component]
        """
        component = component_params.name
        for attr in self.components[component]:
            try:
                component_params[attr] = self.components[component][attr]
            except KeyError:
                logging.warning(f"Attribute {attr} was not found for {component}")

        return component_params


    def add_sequences(self, custom_timeseries=None):
        """
        Looks for the column "profile" within the elements .csv files. If existing, creates a *element*_profile file
        in the sequences folder. If no custom timeseries are provided, default or previously retrieved timeseries (e.g.
        for renewable energy output) will be used.
        :param custom_timeseries: DataFrame with datetime index and elements as columns (should be uploaded as .csv or .xlsx
        """
        scenario_component_folder = os.path.join(self.scenario_folder, "data/elements")
        scenario_sequences_folder = os.path.join(self.scenario_folder, "data/sequences")

        if not os.path.exists(scenario_component_folder):
            logging.warning("No components found to add timeseries. Please add components to the system first.")

        else:
            for filename in os.listdir(scenario_component_folder):
                file = os.path.join(scenario_component_folder, filename)
                components = pd.read_csv(file)
                # Look for components that should have profiles
                if "profile" in components.columns:
                    # Create a file for the corresponding profiles if the elements file has a profiles column
                    sequences_filename = f"{filename.replace('.csv', '')}_profile.csv"
                    component_names = components.name.values.tolist()
                    # TODO generate hourly timeseries based on scenario parameters (start, end, duration)
                    timeindex = pd.date_range(start=f'2025-01-01', end=f'2025-12-31 23:00:00', freq='h')
                    # Create a dataframe to store the profiles
                    profile_df = pd.DataFrame(index=timeindex, columns=component_names)
                    profile_df.index.rename("timeindex", inplace=True)
                    for component in component_names:
                        # If custom timeseries are provided, use these instead of the ones in database
                        if custom_timeseries is not None and component in custom_timeseries.columns:
                            # Check that the length of the custom data matches the index and does not contain NaN values
                            if len(custom_timeseries.index) != len(profile_df.timeindex):
                                logging.error(f"The uploaded timeseries should contain {len(profile_df.timeindex)} "
                                              f"timesteps, but it contains {len(custom_timeseries.index)} ")
                            elif custom_timeseries[component].isnan().any():
                                logging.error(f"The uploaded timeseries contains NaN values. Please revise your input.")
                            else:
                                # Output a warning if the timeseries indexes do not match but save to sequences regardless
                                if custom_timeseries.index != profile_df.timeindex:
                                    logging.warning(f"The uploaded timeseries and the scenario do not have identical "
                                                f"timestamps. Please make sure that the uploaded timeseries cover the correct period.")
                                profile_df[component] = custom_timeseries[component]
                        else:
                            profile_df[component] = self.fetch_component_timeseries(component)

                    # Save sequences to .csv file
                    filepath = os.path.join(scenario_sequences_folder, sequences_filename)
                    profile_df.to_csv(filepath)

        # TODO check the foreign keys between timeseries and component attributes are valid
        # i.e. that each of the component attribute value correspond to a timeseries header
        pass


    def add_buses(self):
        """
        Adds a bus.csv file to elements containing all the necessary buses. Looks through existing components to check
        which buses should be in the system.
        """
        scenario_component_folder = os.path.join(self.scenario_folder, "data/elements")

        if not os.path.exists(scenario_component_folder):
            logging.warning("No components found to infer buses. Please add components to the system first.")

        else:
            buses = []
            for filename in os.listdir(scenario_component_folder):
                file = os.path.join(scenario_component_folder, filename)
                components = pd.read_csv(file)
                # Look for columns pertaining to bus connections
                bus_cols = components.filter(regex="^(bus|from_bus_.*|to_bus_.*)$").columns
                for col in bus_cols:
                    buses.extend(components[col].tolist())

            # Convert to set to keep only unique values (add each bus once)
            buses = list(set(buses))
            # Save to buses .csv file
            filepath = os.path.join(scenario_component_folder, "bus.csv")
            bus_df = pd.DataFrame({"bus": buses, "type": "bus", "balanced": "True"})
            bus_df.to_csv(filepath, index=False)


    def fetch_component_timeseries(self, component):
        """
        Fetch the corresponding sequence for the component, e.g. potential output for volatile resources.
        :param component: Component for which to fetch the timeseries from the database
        :type component: str
        :return timeseries: List with timeseries values corresponding to the component
        """
        # TODO connect to the database to get existing profiles gathered from renewables.ninja, CDS or inputs
        dummy_timeseries = np.random.rand(8760)
        return dummy_timeseries


if __name__=="__main__":
    repo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "scenarios")
    # create_scenario_from_survey_data({}, "test_scenario", repo_path)

    with open(f"test_survey.json", "r") as fp:
        test_survey =  json.load(fp)

    # test_survey =  {'criteria_1': ['diesel_generator', 'wind_turbine'],
    #                 'criteria_1.1': None, 'criteria_1.2': None,
    #                 'criteria_1.3': 10.0, 'criteria_1.4': 5.0,
    #                 'criteria_1.5': None, 'criteria_1.6': None,
    #                 'criteria_1.7': None, 'criteria_2': 'yes',
    #                 'criteria_3': None, 'criteria_3.1': None,
    #                 'criteria_3.2': None, 'criteria_3.3': None,
    #                 'criteria_3.4': None, 'criteria_3.5': None,
    #                 'criteria_3.6': None, 'criteria_4': None,
    #                 'criteria_4.1': None, 'criteria_4.2': None,
    #                 'criteria_4.3': None, 'criteria_5': None,
    #                 'criteria_5.1': None, 'criteria_5.2': None,
    #                 'criteria_SEC_DW': None, 'criteria_5.3': None,
    #                 'criteria_6': None, 'criteria_3a': ['well_with_hand_pump', 'unprotected_spring', 'desalinated_seawater'],
    #                 'criteria_3.1a': 5.0, 'criteria_3.2a': None,
    #                 'criteria_3.3a': None, 'criteria_3.4a': None,
    #                 'criteria_3.5a': None, 'criteria_3.6a': None,
    #                 'criteria_4a': ['hardness'], 'criteria_4.1a': None,
    #                 'criteria_4.2a': None, 'criteria_4.3a': None,
    #                 'criteria_5a': ['no'], 'criteria_5.1a': None,
    #                 'criteria_5.2a': None, 'criteria_SEC_DWa': None,
    #                 'criteria_5.3a': None, 'criteria_6a': None,
    #                 'criteria_3b': ['well_with_hand_pump', 'unprotected_spring', 'river/creek'],
    #                 'criteria_3.1b': 1.0, 'criteria_3.2b': None, 'criteria_3.3b': None,
    #                 'criteria_3.4b': None, 'criteria_3.5b': None, 'criteria_3.6b': None,
    #                 'criteria_4b': None, 'criteria_4.1b': None, 'criteria_4.2b': None,
    #                 'criteria_4.3b': None, 'criteria_5b': ['boiling'],
    #                 'criteria_5.1b': None, 'criteria_5.2b': 5.0,
    #                 'criteria_SEC_DWb': 4.0, 'criteria_5.3b': None,
    #                 'criteria_6b': 'no', 'criteria_7': ['septic_system', 'constructed_wetlands'],
    #                 'criteria_7.1': 15.0, 'criteria_7.2': None,
    #                 'criteria_8': 'yes', 'criteria_8.1': ['tomato', 'raspberry', 'wheat'],
    #                 'criteria_8.2': None, 'criteria_9': 'yes', 'criteria_9.1': ['surface_irrigation'],
    #                 'criteria_9.1.1': 1.5, 'criteria_9.1.2': None, 'criteria_9.1.3': None,
    #                 'criteria_9.1.4': None, 'criteria_9.1.5': None, 'criteria_9.1.6': None,
    #                 'criteria_9.1.7': None, 'criteria_9.1.8': None, 'criteria_9.1.9': None,
    #                 'criteria_9.1.11': None, 'criteria_9.1.12': None, 'criteria_10': 'yes'}

    scenario = ScenarioBuilder()
    scenario.process_survey(test_survey)
    scenario.add_components()
    scenario.add_buses()
    scenario.add_sequences()

