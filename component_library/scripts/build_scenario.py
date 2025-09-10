import os
from copy import deepcopy
import datapackage as dp
import tableschema
import numpy as np
import pandas as pd
import logging
import json
import shutil

from utils import AVAILABLE_COMPONENTS, AVAILABLE_SEQUENCES, COMPONENT_TEMPLATES_PATH
from analyse_survey import create_components_list

import weather_data
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
TYPE_OTHER = "other"

type_check = {
    TYPE_FLOAT: float,
    TYPE_INT: int,
    TYPE_STRING: str,
}

# Later direct imports without .json
# TODO update this mapping with the latest produced survey_answer_component_mapping.json
with open(os.path.join(project_dir, "app", "survey_answer_component_mapping_in_use.json"),"r") as fp:
    SURVEY_ANSWER_COMPONENT_MAPPING= json.load(fp)

with open(os.path.join(project_dir, "app","sub_question_mapping.json"),"r") as fp:
    SUB_QUESTION_MAPPING= json.load(fp)


class ScenarioBuilder:
    def __init__(self, name="test_scenario", overwrite=False):
        self.name = name # should be updated based on scenario
        self.overwrite = overwrite
        self.mapping = SURVEY_ANSWER_COMPONENT_MAPPING
        self.subq_mapping = SUB_QUESTION_MAPPING
        self.components = {}
        self.wished_components = {}
        self.weather_data_path = "weather_data.csv"
        self.scenario_folder = self.create_scenario_folder()


    def create_scenario_folder(self, destination_path=scenario_dir):
        """Create a folder with the datapackage structure, the components and timeseries will be filled later on"""
        scenario_folder = os.path.join(destination_path, self.name)
        create_folder = True
        if os.path.exists(scenario_folder):
            if self.overwrite is False:
                create_folder = False
            else:
                shutil.rmtree(scenario_folder)

        if create_folder is True:
            os.makedirs(scenario_folder)
            os.makedirs(os.path.join(scenario_folder, "scripts"))
            os.makedirs(os.path.join(scenario_folder, "data", "elements"))
            os.makedirs(os.path.join(scenario_folder, "data", "sequences"))

        return scenario_folder

    def water_systems_postprocessing(self, survey):
        """Go through the survey and implement specific logic regarding the water questions"""
        water_distinction_question_id = "2"
        # TODO look answer to question 2 and implement specific logic there
        # in this method, one needs to refer to the question number as they are hard coded in the survey, that means one
        # need to pay attention if the question numbering changes to also carry out the changes here
        # This is a tradeoff between efficiency of survey processing and being able to treat special cases as we would
        # like to and make conditional choices (like add this component only to the drinking water bus and only if quesiton XYZ was answered with ...)

    @property
    def reference_datapackage(self):
        dp_json = os.path.join(COMPONENT_TEMPLATES_PATH, "datapackage.json")
        return dp.Package(dp_json)

    @property
    def scenario_datapackage(self):
        dp_json = os.path.join(self.scenario_folder, "datapackage.json")
        if os.path.exists(dp_json):
            answer = dp.Package(dp_json)
        else:
            answer = dp.Package(base_path=self.scenario_folder)
        return answer

    @property
    def scenario_component_folder(self):
        return os.path.join(self.scenario_folder, "data", "elements")

    def download_weather_data(self):
        if not os.path.exists(self.weather_data_path):
            df = weather_data.get_data()
            df.to_csv(self.weather_data_path,index=False)

    @property
    def weather_data(self):
        if not os.path.exists(self.weather_data_path):
            self.download_weather_data()

        return pd.read_csv(self.weather_data_path)

    @property
    def process_weather_data(self):
        """
        Function to calculate and add new columns to the weather_data DataFrame
        TODO: add more cols for river_flow, groundwater_recharge, etc (check WIP_components\...\profiles.csv)
        """

        weather_df = self.weather_data.copy()
        c_j_to_kwh = 1 / 3600000
        weather_df["ghi"] = weather_df.apply(
            lambda row: row["ssrd"] * c_j_to_kwh, axis=1
        )

        weather_df["windspeed10"] = weather_df.apply(
            lambda row: np.sqrt(row["u10"] ** 2 + row["v10"] ** 2), axis=1
        )

        weather_df["windspeed100"] = weather_df.apply(
            lambda row: np.sqrt(row["u100"] ** 2 + row["v100"] ** 2), axis=1
        )

        return weather_df


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
            print(question_id)
            # 2 options for answer:
            # option 1: list -> turn all TYPE_COMPONENT answers into list
            # option 2: single item (None, float, str) -> assume all TYPE_COMPONENT_ATTRIBUTE answers to be single items
            if answer is not None:
                # obtain question_id
                question_id = question_id.strip("criteria_")

                if question_id in self.mapping:

                    answer_mapping = self.mapping[question_id]
                    bus = answer_mapping.pop("bus", None)

                    map_to = answer_mapping["map_to"]
                    map_answer = answer_mapping["map_answer"]

                    if map_to == TYPE_COMPONENT:
                        # if question_id == "3":
                        #     import pdb;pdb.set_trace()
                        # TODO here for bus handling
                        components_to_add = []

                        # Align answer structure: Should always be of type "list" to match component mapping
                        answer = [answer] if not isinstance(answer, list) else answer

                        # loop over the answers provided and add components to the energy system if the answer finds
                        # itself within the survey answer mapping. If the answer
                        other_answers = []
                        for a in answer:
                            if a in map_answer:
                                components_to_add.extend(map_answer[a])

                            else:
                                 other_answers.append(str(a))

                        self.components.update({component: {} for component in components_to_add})
                        self.wished_components[question_id] = other_answers

                    elif map_to == TYPE_COMPONENT_ATTRIBUTE:
                        if question_id in self.subq_mapping:
                            # Obtain parent question_id and answer to link attribute to its component
                            parent_qid, parent_answer = self.subq_mapping[question_id]

                            # Align answer structure: Should always be single item to match attribute mapping
                            answer = answer[0] if isinstance(answer, list) else answer
                            print(map_answer)
                            # import pdb;pdb.set_trace()

                            # example for opt 2: question 4.2, map_answer = {'water_metals': ['Arsenic', 'Lead', 'Mercury', 'Cadmium', 'Iron']}
                            # TODO: Modify these questions to be TYPE_COMPONENT formatted according to option 1

                            (attribute_name, attribute_type), = map_answer.items()
                            attribute_val = type_check[attribute_type](answer)
                            try:
                                target_components = self.mapping[parent_qid]["map_answer"][parent_answer]
                            except:
                                print(f"There is a problem with question {question_id}")
                                import pdb;pdb.set_trace()

                            for target_component in target_components:
                                self.components[target_component].update({attribute_name: attribute_val})
                                #some debugging for key error
                        else:
                            # TODO: Check if TYPE_COMPONENT_ATTRIBUTE questions are always subquestions of a TYPE_COMPONENT question
                            pass

                    elif map_to == TYPE_NO_MAP:
                        # Don't know what to do with this
                        pass
                    elif map_to == TYPE_OTHER:
                        self.wished_components[question_id] = answer
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

        dp = self.scenario_datapackage
        dp_ref = self.reference_datapackage
        for component in self.components:
            if component in AVAILABLE_COMPONENTS:
                print(component)
                # Load the resource from the reference datapackage
                resource = dp_ref.get_resource(AVAILABLE_COMPONENTS[component])
                df = pd.DataFrame.from_records(resource.read(keyed=True), index="name")

                # Strip the component documentation columns
                selected_columns = [col for col in df.columns if col not in ['verbose_name', 'description']]

                component_params = df.loc[component]
                component_params = component_params[selected_columns]
                # Edit the attributes in the csv file if they have been set in the survey
                component_params = self.update_component_attributes(component_params)

                ofname = os.path.join(self.scenario_component_folder, f"{AVAILABLE_COMPONENTS[component]}.csv")

                # Write or modify the component in the new datapackage
                if os.path.exists(ofname):
                    category_df = pd.read_csv(ofname, index_col="name", sep=";")
                    if component not in category_df.index:
                        # If the component doesn't exist, add a row for the component
                        component_df = component_params.to_frame().T
                        component_df.name = "name"
                        category_df = pd.concat([f.dropna(axis=1, how="all") for f in [category_df, component_df]])
                        # category_df = pd.concat([category_df, component_df])
                    else:
                        # If the component already exists, only update the attributes
                        component_params = category_df.loc[component]
                        category_df.loc[component] = self.update_component_attributes(component_params)
                    # Save the components back to the csv file
                    category_df.to_csv(ofname, index_label="name", sep=";")


                else:
                    # Copy package metadata
                    descriptor = deepcopy(resource.descriptor)
                    selected_fields = []
                    for f in descriptor["schema"]["fields"]:
                        if f["name"] in selected_columns + ["name"]:
                            selected_fields.append(f)
                    descriptor["schema"]["fields"] = selected_fields
                    dp.add_resource(descriptor)
                    dp.commit()

                    component_df = component_params.to_frame().T
                    component_df.to_csv(ofname, index_label="name", sep=";")

            else:
                logging.warning(f"The component {component} is not in the available component list {', '.join([comp for comp in AVAILABLE_COMPONENTS])}")

        dp.save(os.path.join(self.scenario_folder, "datapackage.json"))


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


        scenario_component_folder = self.scenario_component_folder

        dp_ref = self.reference_datapackage
        # ref_buses = dp_ref.get_resource("bus")
        # df_ref_buses = pd.DataFrame.from_records(ref_buses.read(keyed=True))

        # TODO need to do a mapping of sequence to

        dp = self.scenario_datapackage
        scenario_sequences_folder = os.path.join(self.scenario_folder, "data/sequences")


        if not os.path.exists(scenario_component_folder):
            logging.warning("No components found to add timeseries. Please add components to the system first.")

        else:
            profiles_to_add = []
            for res in dp.resources:
                if "/elements/" in res.descriptor["path"]:
                    try:
                        resource_data = pd.DataFrame.from_records(res.read(keyed=True))
                    except tableschema.exceptions.CastError as err:
                        if err.errors:
                            logging.error(
                                f"The resource {res.name} has the following casting errors: {','.join([str(e) for e in err.errors])}")
                        else:
                            logging.error(f"The resource {res.name} has the following casting error: {err}")
                        resource_data = pd.DataFrame()
                    for fk in res.descriptor["schema"]["foreignKeys"]:
                        fk_target = fk["reference"]["resource"]
                        if fk_target != "bus":
                            target_res = dp_ref.get_resource(fk_target)
                            sequence_headers = [
                                f"{f['name']}"
                                for f in target_res.descriptor["schema"].get("fields", [])
                            ]
                            col_name = fk["fields"]
                            if col_name in resource_data.columns:
                                profile_names = resource_data[col_name].values.tolist()
                                # check the bus names are listed in the component library
                                for profile_name in profile_names:
                                    if profile_name not in sequence_headers:
                                        logging.warning(f"In the column '{col_name}' of the resource '{res.name}' the profile {profile_name} is listed, however it is missing from the component library resource in data/sequences path")
                                    else:
                                        if profile_name not in profiles_to_add:
                                            profiles_to_add.append(profile_name)
                            else:
                                logging.error(
                                    f"Column '{col_name}' missing from resource '{res.name}' although it is listed as foreignKey")
            # WIP, here need to take an external file as argument and only select 'profiles_to_add' columns

            if len(profiles_to_add) == 0:
                print(f"No profiles listed within the component for the '{self.scenario_folder.split(os.sep)[-1]}' datapage. If you think it is an error, double check the foreign keys")

            # Get processed weather data
            weather_df = self.process_weather_data
            weather_data_len = len(weather_df)

            # Get blueprint profiles from component library for mapping
            lib_profiles_path = os.path.join(lib_dir, "WIP_components", "data", "sequences", "profiles.csv")
            lib_profiles_df = pd.read_csv(lib_profiles_path, sep=";")

            # Create DF for the scenario profiles and match index with weather data
            scen_profiles_df = pd.DataFrame(columns=profiles_to_add)
            scen_profiles_df = scen_profiles_df.reindex(range(weather_data_len))

            # If timeindex col exists: extract year (of first entry), else: set year to 2022 (according to weather data)
            if "timeindex" in scen_profiles_df.columns:
                scen_profiles_df["timeindex"] = pd.to_datetime(scen_profiles_df["timeindex"])
                scen_profiles_year = int(scen_profiles_df["timeindex"].dt.year.iloc[0])
            else:
                scen_profiles_year = int(2022)

            # Add timeindex column in right format and length
            timeindex = pd.date_range(
                start=f"{scen_profiles_year}-01-01",
                periods=weather_data_len,
                freq="h",
                tz="UTC"
            )
            scen_profiles_df["timeindex"] = timeindex.strftime("%Y-%m-%dT%H:%M:%SZ")

            # Compare with profiles from library profiles csv and in case of a match, populate with data from weather df
            for profile in profiles_to_add:
                if profile in lib_profiles_df.columns:
                    weather_data_match = str(lib_profiles_df[profile].iloc[0])
                    if weather_data_match in weather_df.columns:
                        scen_profiles_df[profile] = weather_df[weather_data_match]
                    else:
                        print(
                            f"Profile '{profile}' is not in the available weather data. A dummy profile (series of 1) will be used.")
                        dummy_series = pd.Series([1] * weather_data_len)
                        scen_profiles_df[profile] = dummy_series
                else:
                    print(
                        f"Profile '{profile}' is not in the profile library. A dummy profile (series of 1) will be used.")
                    scen_profiles_df[profile] = pd.Series([1] * weather_data_len)

            ofname = os.path.join(scenario_sequences_folder, "profiles.csv")
            scen_profiles_df.to_csv(ofname, index=False, sep=";")


        # TODO check the foreign keys between timeseries and component attributes are valid
        # i.e. that each of the component attribute value correspond to a timeseries header


    def add_buses(self):
        """
        Adds a bus.csv file to elements containing all the necessary buses. Looks through existing components to check
        which buses should be in the system.
        """
        scenario_component_folder = self.scenario_component_folder

        dp_ref = self.reference_datapackage
        ref_buses = dp_ref.get_resource("bus")
        df_ref_buses = pd.DataFrame.from_records(ref_buses.read(keyed=True))

        dp = self.scenario_datapackage

        if not os.path.exists(scenario_component_folder):
            logging.warning("No components found to infer buses. Please add components to the system first.")

        else:
            buses_to_add = []
            for res in dp.resources:
                if ("/elements/" in res.descriptor["path"]) and res.name != "bus":
                    try:
                        resource_data = pd.DataFrame.from_records(res.read(keyed=True))
                    except tableschema.exceptions.CastError as err:
                        if err.errors:
                            logging.error(
                                f"The resource {res.name} has the following casting errors: {','.join([str(e) for e in err.errors])}")
                        else:
                            logging.error(f"The resource {res.name} has the following casting error: {err}")
                        resource_data = pd.DataFrame()
                    for fk in res.descriptor["schema"]["foreignKeys"]:
                        if fk["reference"]["resource"] == "bus":
                            col_name = fk["fields"]
                            if col_name in resource_data.columns:
                                bus_names = resource_data[col_name].values.tolist()
                                # check the bus names are listed in the component library
                                for bus_name in bus_names:
                                    if bus_name not in df_ref_buses.name.values:
                                        raise KeyError(f"In the column '{col_name}' of the resource '{res.name}' the bus {bus_name} is listed, however it is missing from the component library resource 'bus.csv'")

                                buses_to_add.extend(bus_names)
                            else:
                                logging.error(f"Add buses: column '{col_name}' missing from resource '{res.name}' although it is listed as foreignKey")

            # for filename in os.listdir(scenario_component_folder):
            #     file = os.path.join(scenario_component_folder, filename)
            #     components = pd.read_csv(file)
            #     # Look for columns pertaining to bus connections
            #     # TODO use the datapakage to get the busses connection
            #     bus_cols = components.filter(regex="^(bus|from_bus_.*|to_bus_.*)$").columns
            #     for col in bus_cols:
            #         buses_to_add.extend(components[col].tolist())

            # Convert to set to keep only unique values (add each bus once)
            buses_to_add = list(set(buses_to_add))


            df_buses = []

            for bus_name in buses_to_add:
                lines = df_ref_buses.loc[df_ref_buses.name == bus_name]
                df_buses.append(lines)
                logging.info(f"Added bus {bus_name} to the '{self.scenario_folder.split(os.sep)[-1]}' datapage")

            if len(buses_to_add) == 0:
                print(
                    f"No buses listed within the component for the '{self.scenario_folder.split(os.sep)[-1]}' datapage. This is likely because the foreign keys are missing from the component library's datapackage.json file.")

            ofname = os.path.join(scenario_component_folder, "bus.csv")
            if df_buses:
                df_buses = pd.concat(df_buses)
                df_buses.to_csv(ofname, index=False, sep=";")

            # TODO add the source component which are connected to the busses using foreign keys, check beforehand the logic


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

    scen_id = 1

    with open(os.path.join(project_dir, "app", f"scenario_{scen_id}_survey_answers.json"), "r") as fp:
        survey_answers =  json.load(fp)

    scenario = ScenarioBuilder(name=f"scenario_{scen_id}", overwrite=True)
    #parse the survey to add components to a list
    scenario.process_survey(survey_answers)
    #scenario.water_systems_postprocessing()
    # adding the component to the datapackge from the component library based on the list of component
    # to add we got from the survey
    scenario.add_components()
    scenario.add_buses()
    scenario.add_sequences()
