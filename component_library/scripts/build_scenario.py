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
from water_treatment_dict import water_treatment_train

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
        self.additional_busses = []
        self.weather_data_path = "weather_data.csv"
        self.demand_data_path = "demand_data.csv"
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

        def safety_check():
            # --- SAFETY CLEANUP STEP ---
            # Remove any existing water-treatment components that process_survey might have added
            water_main_list = []
            for comp in water_treatment_train["main_list"]:
                if isinstance(comp, list):
                    water_main_list.extend(comp)
                else:
                    water_main_list.append(comp)
            for comp in water_main_list:
                self.components.pop((comp, comp), None)
            # --- END CLEANUP ---

        def fill_component_list(suffix):
            unique_slim_component_list = []
            combined_component_list = []
            if survey[f"criteria_4{suffix}.1"] is not None:
                salinity_value = survey[f"criteria_4{suffix}.1"]
                print(salinity_value)  # float
                combined_component_list.extend(self.mapping[f"4{suffix}.1"]["map_answer"]["salinity_selected"])
            if survey[f"criteria_4{suffix}.2"] is not None:
                metals_selected = survey[f"criteria_4{suffix}.2"]
                for metal in metals_selected:
                    print(metal)
                    combined_component_list.extend(self.mapping[f"4{suffix}.2"]["map_answer"][metal])
            if survey[f"criteria_4{suffix}.3"] is not None:
                chemicals_selected = survey[f"criteria_4{suffix}.3"]
                for chemical in chemicals_selected:
                    print(chemical)
                    combined_component_list.extend(self.mapping[f"4{suffix}.3"]["map_answer"][chemical])
            for item in combined_component_list:
                if isinstance(item, list):
                    unique_slim_component_list.extend(item)
                else:
                    unique_slim_component_list.append(item)

            unique_slim_component_list = list(dict.fromkeys(unique_slim_component_list))
            return unique_slim_component_list

        def arrange_components(main_list, component_list):
            arranged_component_list = []
            for component in main_list:
                if isinstance(component, list): # parallel component adding
                    parallel_components = [
                        parallel
                        for parallel in component
                        if parallel in component_list]
                    # single component from parallel choices
                    if len(parallel_components) == 1: arranged_component_list.append(parallel_components[0])
                    # multiple components from parallel choices
                    elif len(parallel_components) > 1: arranged_component_list.append(parallel_components)
                else: # single component adding
                    if component in component_list:
                        arranged_component_list.append(component)

            return arranged_component_list

        def create_component_dict(component_list, entry_bus, water_type):
            prefix = "SW_" if water_type.lower() == "service" else "DW_"
            components_dict = {}
            counter = {} # counts the number of times a component appears in the train
            previous_out_bus = entry_bus # entry bus to the treatment train
            for index, component in enumerate(component_list):
                if isinstance(component, list): # handling parallel components
                    parallel_out_bus = f"{prefix}parallel_{index+1}_out_bus"
                    for parallel in component:
                        counter[parallel] = counter.get(parallel, 0) + 1
                        key = (f"{parallel}", f"{prefix}{parallel}_{counter[parallel]}")
                        components_dict[key] = {"water_in_bus":previous_out_bus,"water_out_bus":parallel_out_bus}
                    previous_out_bus = parallel_out_bus
                else:
                    counter[component] = counter.get(component, 0) + 1
                    out_bus = f"{prefix}{component}_{counter[component]}_out_bus"
                    key = (f"{component}", f"{prefix}{component}_{counter[component]}")
                    components_dict[key] = {"water_in_bus": previous_out_bus,"water_out_bus": out_bus}
                    previous_out_bus = out_bus

            return components_dict

        safety_check()
        if survey["criteria_2"] == "Yes": # set Yes currently
            suffixes_a = ["_GWa", "_DSa", "_RCa", "_La"] # drinking water
            suffixes_b = ["_GWb", "_DSb", "_RCb", "_Lb"] # service water
            drinking_water_component_list = []
            service_water_component_list = []
            for a_suffix, b_suffix in zip(suffixes_a, suffixes_b):
                drinking_water_component_list.extend(fill_component_list(a_suffix))
                service_water_component_list.extend(fill_component_list(b_suffix))
            drinking_water_component_list = list(dict.fromkeys(drinking_water_component_list))
            service_water_component_list = list(dict.fromkeys(service_water_component_list))
            print("DW treatment dictionary")
            drinking_water_component_list = arrange_components(water_treatment_train["main_list"], drinking_water_component_list)
            drinking_water_treatment_dict = create_component_dict(drinking_water_component_list, entry_bus = "water-in-bus", water_type = "drinking")
            for (component_type, component_name), component_attrs in drinking_water_treatment_dict.items():
                # Add the component from the train
                self.add_single_component(component_type, component_name, component_attrs)
                # Add the water in and water out buses for each component
                for bus_type in ["water_in_bus", "water_out_bus"]:
                    if component_attrs.get(bus_type):  # only add if defined
                        self.add_single_bus(name=component_attrs.get(bus_type), balanced=True, carrier="water")
            print(drinking_water_treatment_dict)
            print("SW treatment dictionary")
            service_water_component_list = arrange_components(water_treatment_train["main_list"], service_water_component_list)
            service_water_treatment_dict = create_component_dict(service_water_component_list, entry_bus = "water-in-bus", water_type = "service")
            for (component_type, component_name), component_attrs in service_water_treatment_dict.items():
                # Add the component from the train
                self.add_single_component(component_type, component_name, component_attrs)
                # Add the water in and water out buses for each component
                for bus_type in ["water_in_bus", "water_out_bus"]:
                    if component_attrs.get(bus_type):  # only add if defined
                        self.add_single_bus(name=component_attrs.get(bus_type), balanced=True, carrier="water")
            print(service_water_treatment_dict)
        else:
            suffixes = ["_GW", "_DS", "_RC", "_L"] # all water assumed drinking water
            drinking_water_component_list = []
            for suffix in suffixes:
                drinking_water_component_list.extend(fill_component_list(suffix))
            drinking_water_component_list = list(dict.fromkeys(drinking_water_component_list))
            print("DW treatment dictionary")
            drinking_water_component_list = arrange_components(water_treatment_train["main_list"], drinking_water_component_list)
            drinking_water_treatment_dict = create_component_dict(drinking_water_component_list, entry_bus="water-in-bus", water_type="drinking")
            for (component_type, component_name), component_attrs in drinking_water_treatment_dict.items():
                # Add the component from the train
                self.add_single_component(component_type, component_name, component_attrs)
                # Add the water in and water out buses for each component
                for bus_type in ["water_in_bus", "water_out_bus"]:
                    if component_attrs.get(bus_type):  # only add if defined
                        self.add_single_bus(name=component_attrs.get(bus_type), balanced=True, carrier="water")
            print(drinking_water_treatment_dict)

        #final_water_treatment_train
        #self.add_single_component()
        #self.add_single_bus()

    def waste_water_systems_postprocessing(self, survey):
        """Go through the survey and implement specific logic regarding the water questions"""
        # water_distinction_question_id = "7"
        # waste_systems = survey["criteria_7"]
        # if "septic system" in waste_systems:
        # Add this to the list pass
        # Need to be the same name as in WIP components in the csv
        # self.components.update({"septic_system": {"name":"grey_water_se"}})
        # self.components.update({"septic_system": {"name":"black_water_se"}})
        # exemple if you need to change an attribute of a resource/component
        # self.components["septic_system"].update({"capacity": 100})

        #### Vivek's attempt at hardcode logic

        # Survey responses assumed or taken from survey
        wastewater_systems = survey["criteria_7"]
        population = 1000 #  # survey needs to ask population, makes most of the logic implementation easier
        toilet_types = survey["criteria_7.3"]


        # black water treatment
        if "flush toilet" in toilet_types:
            if "septic system" in wastewater_systems:
                self.components.update({("septic_system", "black_water_septic"): {"water_in_bus": "black-water-bus"}})
                # to update attributes if survey provides it
                # self.components[("septic_system","black_water_septic")].update({"capacity": 100})
            elif "constructed wetland" in wastewater_systems:
                self.components.update({("constructed_wetland", "black_water_cw"): {"water_in_bus": "black-water-bus", "water_out_bus": "wwtp-ip-water-bus"}})
                # to update attributes if survey provides it
                # self.components[("constructed_wetland", "black_water_cw")].update({"capacity": 100})
            else:
                # default addition of septic system
                self.components.update({("septic_system", "black_water_septic"): {"water_in_bus": "black-water-bus", "water_out_bus": "wwtp-ip-water-bus"}})

        # grey water treatment

        if "septic system" in wastewater_systems:
            component_key = self.add_single_component(
                component_type="septic_system",
                component_name="grey_water_septic",
                component_attrs= {
                    "water_in_bus": "grey-water-bus"
                }
            )
            capacity = survey["criteria_7.1.0"]
            if capacity is not None:
                # to update attributes if survey provides it
                self.components[component_key].update({"capacity": capacity})
        elif "constructed wetland" in wastewater_systems:
            self.components.update({("constructed_wetland", "grey_water_cw"): {"water_in_bus": "grey-water-bus", "water_out_bus": "wwtp-ip-water-bus"}})
            # to update attributes if survey provides it
            # self.components[("constructed_wetland", "grey_water_cw")].update({"capacity": 100})
        else:
            # default addition of septic system
            self.components.update({("septic_system", "grey_water_septic"): {"water_in_bus": "grey-water-bus", "water_out_bus": "wwtp-ip-water-bus"}})

        # waste water treatment plant based on population
        if population >= 10000:
            # centralized waste water treatment plant
            self.components.update({"centralized_waste_water_treatment_plant": {"water_in_bus": "wwtp-ip-water-bus", "water_out_bus": "wwtp-op-water-bus"}})
            if "centralized waste water treatment plant" in wastewater_systems:
                # to update attributes if survey provides it
                # self.components["centralized_waste_water_treatment_plant"].update({"capacity": 100})
                pass
        else:
            # decentralized waste water treatment plant
            # default addition of this component

            self.components.update({("decentralized_waste_water_treatment_plant","decentralized_waste_water_treatment_plant"): {"water_in_bus": "wwtp-ip-water-bus", "water_out_bus": "wwtp-op-water-bus"}})
            if "decentralized waste water treatment plant" in wastewater_systems:
                # to update attributes if survey provides it
                # self.components["decentralized_waste_water_treatment_plant"].update({"capacity": 100})
                pass

        # water recycling and reuse system
        # default addition of this component
        self.add_single_component(component_type="water_reuse_system", component_attrs={"water_in_bus": "wwtp-op-water-bus", "water_out_bus": "service-water-bus"})
        if "water recycling and reuse system" in wastewater_systems:
            # to update attributes if survey provides it
            #self.components["water_reuse_system"].update({"capacity": 100})
            pass

        print(self.components)

    def get_single_component_from_datapackage(self, dp, resource_name, component_name):
        """
        Returns a component from a single resource (csv file) of a datapackage as a one-row df.
        ATTENTION: the returned df will be empty if there is no match!
        """
        resource = dp.get_resource(resource_name)
        df = pd.DataFrame.from_records(resource.read(keyed=True))
        component = df[df["name"] == component_name]
        # TODO: check uniqueness of resource names
        #  (if necessary...check if there are already other checks for uniqueness of names in the reference datapackage)

        return component

    def get_single_component_from_datapackage(self, dp, resource_name, component_name):
        """
        Returns a component from a single resource (csv file) of a datapackage as a one-row df.
        ATTENTION: the returned df will be empty if there is no match!
        """
        resource = dp.get_resource(resource_name)
        df = pd.DataFrame.from_records(resource.read(keyed=True))
        component = df[df["name"] == component_name]
        # TODO: check uniqueness of resource names
        #  (if necessary...check if there are already other checks for uniqueness of names in the reference datapackage)

        return component

    def crop_systems_postprocessing(self):
        """
        AFTER survey_processing to fetch crop components
        BEFORE add_components to be able to add extra components based on crop components
        """
        dp_ref = self.reference_datapackage

        # Get additional components as reference
        # TODO: assign these components directly when adding single comp, use busses of "crop" from below
        sun = self.get_single_component_from_datapackage(dp=dp_ref, resource_name="energy_sources",
                                                         component_name="solar-radiation")
        rain = self.get_single_component_from_datapackage(dp=dp_ref, resource_name="water_sources",
                                                          component_name="precipitation")
        generic_excess = self.get_single_component_from_datapackage(dp=dp_ref, resource_name="excess",
                                                                    component_name="generic-excess")

        # loop through components
        components_so_far = self.components.copy()
        for (component_type, component_name), component_attributes in components_so_far.items():
            crop = self.get_single_component_from_datapackage(dp=dp_ref, resource_name="mimo_crops",
                                                              component_name=component_type)
            if crop.empty:
                continue

            # add sources: sun, rain
            sun_bus = f"{component_name}_{sun['bus'].iloc[0]}"
            self.add_single_component(component_type=sun['name'].iloc[0],
                                      component_name=f"{component_name}_{sun['name'].iloc[0]}",
                                      component_attrs={
                                          "capacity": component_attributes["capacity"],
                                          "bus": sun_bus,
                                          "expandable": False
                                      }
                                      )
            self.add_single_bus(name=sun_bus, balanced=True, carrier=sun["carrier"].iloc[0])

            rain_bus = f"{component_name}_{rain['bus'].iloc[0]}"
            self.add_single_component(component_type=rain['name'].iloc[0],
                                      component_name=f"{component_name}_{rain['name'].iloc[0]}",
                                      component_attrs={
                                          "capacity": component_attributes["capacity"],
                                          "bus": rain_bus,
                                          "expandable": False
                                        }
                                      )
            self.add_single_bus(name=rain_bus, balanced=True, carrier=rain["carrier"].iloc[0])

            # add excess: crops, biomass
            crop_bus = crop["crop_bus"].iloc[0]
            self.add_single_component(component_type="generic-excess",
                                      component_name=f"{component_name}_crop-excess",
                                      component_attrs={
                                          "bus": crop_bus,
                                        }
                                      )
            self.add_single_bus(name=crop_bus, balanced=True, carrier=rain["carrier"].iloc[0])

            biomass_bus = crop["biomass_bus"].iloc[0]
            self.add_single_component(component_type="generic-excess",
                                      component_name=f"{component_name}_biomass-excess",
                                      component_attrs={
                                          "bus": biomass_bus
                                        }
                                      )
            self.add_single_bus(name=biomass_bus, balanced=True, carrier=rain["carrier"].iloc[0])

            # add irrigation as converter
            # TODO: irrigation-tech-mapping
            irrigation_map = {
                "surface irrigation": "surface-irrigation",
                "smart irrigation system": "smart-irrigation",
            }

            irrigation = self.get_single_component_from_datapackage(dp=dp_ref, resource_name="irrigation",
                                    component_name=irrigation_map[component_attributes["irrigation_tech"]])
            try:
                irrigation_bus = f"{component_name}_{irrigation['to_bus'].iloc[0]}"
            except Exception:
                import pdb
                pdb.set_trace()

            self.add_single_component(component_type=irrigation['name'].iloc[0],
                                          component_name=f"{component_name}_{irrigation['name'].iloc[0]}",
                                          component_attrs={
                                              "capacity": component_attributes["capacity"],
                                              "bus": irrigation_bus,
                                              "expandable": False
                                          }
                                          )
            self.add_single_bus(name=irrigation_bus, balanced=True, carrier=irrigation["carrier"].iloc[0])

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

    def download_demand_data(self):
        if not os.path.exists(self.demand_data_path):
            # TODO: empty df for now, add real data download later
            df = pd.DataFrame(columns=["dummy"])
            df.to_csv(self.demand_data_path, index=False)

    @property
    def demand_data(self):
        if not os.path.exists(self.demand_data_path):
            self.download_demand_data()

        return pd.read_csv(self.demand_data_path)

    def download_weather_data(self):
        if not os.path.exists(self.weather_data_path):
            df = weather_data.get_data()
            df.to_csv(self.weather_data_path, index=False)

    @property
    def weather_data(self):
        if not os.path.exists(self.weather_data_path):
            self.download_weather_data()

        return pd.read_csv(self.weather_data_path)

    # TODO: put together demand_data, weather_data and others to profiles_data or sequences_data
    #  and process all together as one df
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


    def add_loads(self):
        """
        Add load.csv to the energy system based on demand_data.csv.
        --------------------------
        ATTENTION regarding the variable names:
        "demand" refers to the actual data (from WEFEDemand)
        "load" refers to the load.csv from the component library
        profiles.csv basically maps: load_name -> demand_name

        "usual" workflow:
        AVAILABLE_COMPONENTS
        -> component_type: name_of_the_csv (load)
        -> get the load_name
        -> profiles.csv for mapping (is in AVAILABLE_COMPONENTS itself)
        -> get the demand_name
        
        I need a reversed workflow because I got the demand_name and map it to load_name
        to get the modified component (load).
        
        I assume "load.csv" and "profiles.csv" to be the only necessary components and that they will not be renamed.

        I assume the demands to be unique (one for electricity, one for drinking water, ...) so in the load.csv,
        there will only be one row for every component (sink with demand profile) using the predefined component name.
        """
        demand_df = self.demand_data
        demands_to_add = demand_df.columns

        dp = self.scenario_datapackage
        dp_ref = self.reference_datapackage

        # Read in "load.csv" from component library into DataFrame, add metadata to scenario datapackage
        resource = dp_ref.get_resource("load")
        descriptor = deepcopy(resource.descriptor)
        dp.add_resource(descriptor)
        load_df = pd.DataFrame.from_records(resource.read(keyed=True))

        # Read in "excess.csv" from component library into DataFrame, add metadata to scenario datapackage
        resource = dp_ref.get_resource("excess")
        descriptor = deepcopy(resource.descriptor)
        dp.add_resource(descriptor)
        excess_df = pd.DataFrame.from_records(resource.read(keyed=True))

        # Read in "profiles.csv" from component library
        profiles_resource = dp_ref.get_resource("profiles")
        profiles_df = pd.DataFrame.from_records(profiles_resource.read(keyed=True))

        # Map the given demands to the corresponding loads of the component library
        loads_to_add = []
        for demand in demands_to_add:
            match = profiles_df.columns[(profiles_df.iloc[0] == demand).values].tolist()
            if not match:
                logging.warning(f"Demand '{demand}' not found in '{profiles_resource.name}.csv'")
            loads_to_add.extend(match)

        # Create new load DF (matches only) and corresponding excess DF
        filtered_load_df = load_df[load_df["profile"].isin(loads_to_add)]
        filtered_excess_df = excess_df[excess_df["bus"].isin(filtered_load_df["bus"])]

        # Save the required load.csv and excess.csv in the scenario component folder
        filtered_load_df.to_csv(os.path.join(self.scenario_component_folder, "load.csv"), index=False, sep=";")
        filtered_excess_df.to_csv(os.path.join(self.scenario_component_folder, "excess.csv"), index=False, sep=";")

        # Save scenario datapackage metadata
        dp.commit()
        dp.save(os.path.join(self.scenario_folder, "datapackage.json"))


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
                        # TODO here make this check independent of question id
                        if question_id.startswith("4_") and question_id.endswith(".1") and isinstance(answer, (int, float)):
                            # treat any float as salinity selected
                            components_to_add.extend(map_answer["salinity_selected"])
                            other_answers = []

                        else:
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

                        # temporary error solving trick for parallel components
                        for component in components_to_add:
                            if isinstance(component, list):
                                # parallel components: add each one
                                for subcomponent in component:
                                    self.components[(subcomponent, subcomponent)] = {}
                            else:
                                # single sequential component
                                self.components[(component, component)] = {}

                        #self.components.update({(component,component): {} for component in components_to_add})
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
                                self.components[(target_component, target_component)].update({attribute_name: attribute_val})
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
        for component_key in self.components:
            component_type, component_name = component_key
            if component_type in AVAILABLE_COMPONENTS:
                # Load the resource from the reference datapackage
                resource = dp_ref.get_resource(AVAILABLE_COMPONENTS[component_type])
                df = pd.DataFrame.from_records(resource.read(keyed=True))
                df.set_index("name", drop=False, inplace=True)

                # Strip the component documentation columns
                selected_columns = [col for col in df.columns if col not in ['verbose_name', 'description']]

                component_params = df.loc[component_type]
                component_params = component_params[selected_columns]
                # Edit the attributes in the csv file if they have been set in the survey
                component_params = self.update_component_attributes(component_key,component_params)
                ofname = os.path.join(self.scenario_component_folder, f"{AVAILABLE_COMPONENTS[component_type]}.csv")

                # Write or modify the component in the new datapackage
                if os.path.exists(ofname):
                    component_df = pd.read_csv(ofname, sep=";")
                    existing_records = component_df.name.tolist()
                    if component_params["name"] not in existing_records and component_name not in existing_records:
                        # If the component doesn't exist, add a row for the component
                        component_df = pd.concat([component_df, component_params.to_frame().T])
                    else:
                        # If the component already exists, only update the attributes
                        if component_params["name"] in existing_records:
                            component_name = component_params["name"]
                        component_df.set_index("name", drop=False, inplace=True)
                        component_params = component_df.loc[component_name].copy()
                        component_df.loc[component_name] = self.update_component_attributes(component_key,
                                                                                           component_params)
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

                # Save the components back to the csv file
                component_df[selected_columns].to_csv(ofname, index=False, sep=";")


            else:
                logging.warning(f"The component {component_key} is not in the available component list {', '.join([comp for comp in AVAILABLE_COMPONENTS])}")

        dp.save(os.path.join(self.scenario_folder, "datapackage.json"))


    def update_component_attributes(self, component_key,component_params):
        """
        Edit the component attributes in the corresponding .csv file based on the component attributes set in
        self.components.
        :param component_key: tuple containing the component type and component name
        :param component_params: DataSeries object containing the .csv row of parameters for the corresponding component
        :returns: component_params DataSeries updated according to attributes in self.components[component]
        """
        for attr in self.components[component_key]:
            try:
                component_params.loc[attr] = self.components[component_key][attr]
            except KeyError:
                logging.warning(f"Attribute {attr} was not found for {component_key}")

        if "name" not in self.components[component_key]:
            # make sure the name provided in the component_key is used instead of the name of component library
            if component_key[0] != component_key[1]:
                component_params["name"] = component_key[1]
        return component_params


    def add_single_component(self, component_type, component_name=None, component_attrs=None):

        if not isinstance(component_attrs, dict):
            component_attrs = {}
            logging.warning(f"The component attributes {component_attrs} must be of type dict! Will be ignored...")

        if component_name is None:
            component_key = (component_type, component_type)
        elif isinstance(component_name, tuple):
            component_key = component_name
        elif isinstance(component_name, str):
            component_key = (component_type, component_name)
        else:
            logging.warning(f"The component name {component_name} is neither a string nor a tuple")

        self.components.update({component_key: component_attrs})
        return component_key


    def add_sequences(self, custom_timeseries=None):
        """
        Looks for the column "profile" within the elements .csv files. If existing, creates a *element*_profile file
        in the sequences folder. If no custom timeseries are provided, default or previously retrieved timeseries (e.g.
        for renewable energy output) will be used.
        :param custom_timeseries: DataFrame with datetime index and elements as columns (should be uploaded as .csv or .xlsx
        """
        dp_ref = self.reference_datapackage
        dp = self.scenario_datapackage

        if not os.path.exists(self.scenario_component_folder):
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

            # TODO: process all profiles data into one df that shall be imported here
            # Get processed weather data
            weather_df = self.process_weather_data

            # Get demand data
            demand_df = self.demand_data

            # Check data profiles length
            # TODO: Check possible issues with demand data and weather data,
            #  I assumed weather data to always be of correct length while demand data may be flexible in length
            if len(weather_df) != len(demand_df):
                logging.warning(f"Length mismatch between {self.demand_data_path} and {self.weather_data_path}.")

            if demand_df.dropna(how="all").empty:
                profiles_len = len(weather_df)
                logging.warning(f"{self.demand_data_path} seems to be effectively empty")
                logging.info(f"{self.weather_data_path} will be used to set the time index of the model.")
            else:
                profiles_len = len(demand_df)
                logging.info(f"{self.demand_data_path} will be used to set the time index of the model.")

            # Get blueprint profile names from component library for mapping
            lib_profiles_path = os.path.join(lib_dir, "WIP_components", "data", "sequences", "profiles.csv")
            lib_profiles_df = pd.read_csv(lib_profiles_path, sep=";")

            # Create DF for the scenario profiles and match index with profiles length
            scen_profiles_df = pd.DataFrame(columns=profiles_to_add, index=range(profiles_len))

            # If timeindex col exists: extract year (of first entry), else: set year to 2022 (according to weather data)
            if "timeindex" in scen_profiles_df.columns:
                scen_profiles_df["timeindex"] = pd.to_datetime(scen_profiles_df["timeindex"])
                scen_profiles_year = int(scen_profiles_df["timeindex"].dt.year.iloc[0])
            else:
                scen_profiles_year = int(2022)

            # Add timeindex column in right format and length
            timeindex = pd.date_range(
                start=f"{scen_profiles_year}-01-01",
                periods=profiles_len,
                freq="h",
                tz="UTC"
            )
            scen_profiles_df["timeindex"] = timeindex.strftime("%Y-%m-%dT%H:%M:%SZ")

            # Compare with profiles from library profiles csv and in case of a match, populate with data from weather df
            for profile in profiles_to_add:
                if profile in lib_profiles_df.columns:
                    matching_col = str(lib_profiles_df[profile].iloc[0])
                    if matching_col in weather_df.columns:
                        scen_profiles_df[profile] = weather_df[matching_col].reindex(range(profiles_len)).values
                    elif matching_col in demand_df.columns:
                        scen_profiles_df[profile] = demand_df[matching_col].reindex(range(profiles_len)).values
                    else:
                        logging.warning(
                            f"Profile '{profile}' is not in the available data. A dummy profile (series of 1) will be used.")
                        scen_profiles_df[profile] = pd.Series([1] * profiles_len)
                else:
                    logging.warning(
                        f"Profile '{profile}' is not in the profile library. A dummy profile (series of 1) will be used.")
                    scen_profiles_df[profile] = pd.Series([1] * profiles_len)

            ofname = os.path.join(self.scenario_folder, "data/sequences", "profiles.csv")
            scen_profiles_df.to_csv(ofname, index=False, sep=";")


        # TODO check the foreign keys between timeseries and component attributes are valid
        # i.e. that each of the component attribute value correspond to a timeseries header

    def add_single_bus(self, name, balanced=True, carrier=""):
        # Check if bus is in component_lib, if not: Add to additional busses so that it will be ignored later
        dp_ref = self.reference_datapackage
        bus_ref = self.get_single_component_from_datapackage(dp=dp_ref, resource_name="bus", component_name=name)
        if bus_ref.empty:
            self.additional_busses.append(name)

        ofname = os.path.join(self.scenario_component_folder, "bus.csv")
        bus = pd.Series({"name": name, "type": "bus", "balanced": balanced, "carrier": carrier}).to_frame().T
        # Write or modify the bus in the new datapackage
        if os.path.exists(ofname):
            busses_df = pd.read_csv(ofname, sep=";")
            existing_records = busses_df.name.tolist()
            if name not in existing_records:
                # If the bus doesn't exist, add a row for it
                busses_df = pd.concat([busses_df, bus])
            else:
                # If the bus already exists, replace it
                busses_df.set_index("name", drop=False, inplace=True)
                try:
                    # TODO: ask chatgpt about the indexing error...
                    busses_df.loc[name] = bus
                except Exception:
                    # import pdb
                    # pdb.set_trace()
                    pass
        else:
            busses_df = bus
        # Save the components back to the csv file
        busses_df.to_csv(ofname, index=False, sep=";")


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
                                        if bus_name not in self.additional_busses:
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

            # Write or modify the bus in the new datapackage
            # why are you replacing the bus in the else block?

            if os.path.exists(ofname):
                busses_df = pd.read_csv(ofname, sep=";")
                existing_records = busses_df.name.tolist()
                if df_buses:
                    new_buses = [bus for bus in df_buses if not bus.empty and bus["name"].iloc[0] not in existing_records]
                    if new_buses:
                        busses_df = pd.concat([busses_df] + new_buses, ignore_index=True)
               # if df_buses:
                    # If the bus doesn't exist, add a row for it
                 #   busses_df = pd.concat([busses_df] + df_buses)
                #else:
                    # If the bus already exists, replace it
                #    busses_df.set_index("name", drop=False, inplace=True)
                 #   busses_df.loc[name] = bus
            else:
                if df_buses:
                    busses_df = pd.concat(df_buses, ignore_index=True)
            # Save the components back to the csv file
            busses_df.to_csv(ofname, index=False, sep=";")




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

    scen_id = 15

    with open(os.path.join(project_dir, "app", f"scenario_{scen_id}_survey_answers.json"), "r") as fp:
        survey_answers =  json.load(fp)

    scenario = ScenarioBuilder(name=f"scenario_{scen_id}", overwrite=False)
    #parse the survey to add components to a list
    scenario.process_survey(survey_answers)

    scenario.water_systems_postprocessing(survey_answers)
    scenario.waste_water_systems_postprocessing(survey_answers)
    # scenario.crop_systems_postprocessing()

    # Add a load.csv component based on demand data from WEFEDemand
    scenario.add_loads()

    # adding the component to the datapackge from the component library based on the list of component
    # to add we got from the survey
    scenario.add_components()
    scenario.add_buses()
    scenario.add_sequences()
