import copy
from django.utils.translation import gettext_lazy as _
import logging

TYPE_FLOAT = "float"
TYPE_INT = "int"
TYPE_STRING = "string"
TYPE_WATER = "string"
INFOBOX = "description"


# case A --> a dict with component mapped to answers (in this case possible_answers is a list)
# case B --> the column of the csv file which is concerned by this value (in this case possible_answers is not a list but one of TYPE_*


SURVEY_ANSWER_COMPONENT_MAPPING = {
    # "question_id": {"yes": "component_name"},
    # "question_id": {"no": "component_name", "yes": "other_component_name"},
    "1": {
        "photovoltaic system": "photovoltaics",
        "battery system": "battery-storage",
        "diesel generator": "diesel-generator",
        "wind turbine": "wind-turbine",
        "hydropower": "hydropower",
        "biogas plant": "biogas_plant", #TODO: biogas model in csv. format has to be created (can be inspired by OWEFE)
        "national grid": "electricity-grid",
    },
    "1.1": {"capacity": TYPE_FLOAT},
    "1.2": {"capacity": TYPE_FLOAT},
    "1.3": {"capacity": TYPE_FLOAT},
    "1.4": {"capacity": TYPE_FLOAT},
    "1.5": {"capacity": TYPE_FLOAT},
    "1.6": {"capacity": TYPE_FLOAT},
    "1.7": {"other energy_conversion": TYPE_STRING},
    "1.8": "capacity",
    # TODO Implement the following: TYPE_WATER_USE determines whether following components are connected to drinking water cycle
    #  (drinking_water_bus; drinking_water_demand), or service water cycle (service_water_bus, service_water_demand),
    #  note that often service water cycle and drinking water cycle are connected
    #  via an additional water treatment component
    "3": {
        "groundwater well": ["groundwater"],
        "desalinated seawater": ["swro", "seawater"],
        "river/creek": ["river-water-uptake", "hydropower"],
        "rainwater harvesting": [
            "precipitation",
            "rainwater-harvesting",
            "service-water-storage"
        ],
        "water truck": "water-truck",
        "public tap water": "tap-water",
    },
    "3.1": {
        "Yes": ["water-pump"]
    },
    "3.1.1": {"head": TYPE_FLOAT},
    "3.1.3": {"capacity": TYPE_FLOAT},
    "3.1.4": {"flow_max": TYPE_FLOAT},
    "3.2": {"water-truck/marginal_cost": TYPE_FLOAT},
    "4": {"salinity": ["ro"],
          "chemical contamination": ["ion_exchange", "membrane_filtration"],
          },
    #TODO add (decentralized) Treatment options for "fecal contamination","hardness","sediments and turbidity",
    # "nitrates and nitrites", pesticides, pharmaceutical_residues, fertilizers, industrial_chemicals
    "4.1": {"SOURCE_WATER_TYPE/salinity": TYPE_FLOAT},

    "5": {"reverse_osmosis": ["ro"],
          "boiling": ["boiling_water"],
          "distillation": ["water_distillation"],
          "activated carbon filter": ["activated_carbon_filter"],
          "chlorination": ["chlorination"],
          "UV-disinfection": ["uv-disinfection"],
          "cartridge filter": ["cartrdige_filter"],
          "microfiltration": ["microfiltration"],
          "ultrafilration": ["ultrafiltration"],
          "ceramic filter": ["ceramic_filter"],
          "nanofiltraion": ["nanofiltration"],
          "slow sand filter": ["slow_sand_filter"],
          "water softener": ["water_softener"],
          "membrane distillation": ["membrane_distillation"],
          "other": TYPE_STRING
          },
    "5.1": {"WT_TYPE/recovery_rate": TYPE_FLOAT},
    "5.2": {"WT_TYPE/capacity": TYPE_FLOAT},
    "SEC_DW": {"WT_TYPE/SEC": TYPE_FLOAT},


    "7": {"septic system": ["septic_system"],
          "constructed_wetland": ["constructed_wetland"],
          "centralized waste water treatment plant": ["cWWTP"],
          "decentralized waste water treatment plant": ["dWWTP"],
          "recycling and reuse system": ["RR"],
          "disposal to environment without treatment": ["direct_wastewater_disposal"]
          },
    "7.1": {"selected WWT_TYPE/capacity": TYPE_FLOAT},
    "7.3": {"flush toilet": ["flush_toilet"],
            "latrine": ["latrine"],
            "dry toilet": ["dry_toilet"],
            "composting toilet": ["composting_toilet"],
            "open filed": ["open_field"],
            },
    "8": {"wheat": ["wheat"],
          "rice": ["rice"],
          "maize": ["maize"],
          "soy bean": ["soy_bean"],
          "dry bean": ["dry_bean"],
          "peanut": ["peanut"],
          "potato": ["potato"],
          "cassava": ["cassava"],
          "tomato": ["tomato"],
          "sweetcorn": ["sweetcorn"],
          "green bean": ["green_bean"],
          "carrot": ["carrot"],
          "cotton": ["cotton"],
          "banana": ["banana"],
          "lettuce": ["lettuce"],
          "cucumber": ["cucumber"],
          "pineapple": ["pineapple"],
          "avocado": ["avocado"],
          "quinoa": ["quinoa"],
          "amaranth": ["amaranth"],
          "guava": ["guava"],
          "papaya": ["papaya"],
          "mango": ["mango"],
          "sorghum": ["sorghum"],
          "millet": ["millet"],
          "yam": ["yam"],
          "plantain": ["plantain"],
          "apple": ["apple"],
          "sunflower": ["sunflower"],
          "cacao": ["cacao"],
          "cashew": ["cashew"],
          "pumpkin": ["pumpkin"],
          "black bean": ["black_bean"],
          "oat": ["oat"],
          "pepper": ["pepper"],
          },
    "9.1": {"IRRIGATION_TYPE": ["IRRIGATION_TYPE"]},
    "9.3": {"capacity": TYPE_FLOAT},
    "10": {"yes": ["apv"]}
}

COMPONENT_CATEGORY = "components"
WATER_CATEGORY = "water"
CROP_CATEGORY = "crops"

SURVEY_QUESTIONS_CATEGORIES = {
    COMPONENT_CATEGORY: _("Components"),
    WATER_CATEGORY: _("Water"),
    CROP_CATEGORY: _("Crops"),
}


def generate_generic_questions(suffixes, survey_questions_template, text_to_replace):
    """Generate redundant question for different cases
    :param suffixes: dict mapping of label to subquestion suffix
    :param survey_questions_template: the redundant questions which need to be duplicated for each suffix mapping
    :param text_to_replace: the text placeholder which will be replaced by the `suffices` keys
    :return: list of survey questions
    """
    new_questions = []
    for name, suffix in suffixes.items():
        temp = copy.deepcopy(survey_questions_template)
        for question in temp:
            question["question"] = question["question"].replace(text_to_replace, name)
            id = question["question_id"]
            question["question_id"] = id + suffix
            subquestions = question.get("subquestion", {})
            for subq in subquestions.keys():
                subq_id = subquestions[subq]
                if isinstance(subq_id, str):
                    subq_id = [subq_id]

                new_ids = [q_id + suffix for q_id in subq_id]
                if len(new_ids) == 1:
                    new_ids = new_ids[0]
                subquestions[subq] = new_ids
            if subquestions:
                question["subquestion"] = subquestions
            new_questions.append(question)
    return new_questions

COMPONENT_SURVEY_STRUCTURE = [
    # {"question": "", "question_id": "", "possible_answers":["answer1", "answer2"]}
    {
        "question": "Which components do yoú use for electricity production?",
        "question_id": "1",
        "possible_answers": [
            "photovoltaic system",
            "battery system",
            "diesel generator",
            "wind turbine",
            "hydropower",
            "national grid",
            "biogas plant",
            "other",
        ],
        "display_type": "multiple_choice_tickbox",
        "subquestion": {
            "photovoltaic system": "1.1",
            "battery system": "1.2",
            "diesel generator": "1.3",
            "wind turbine": "1.4",
            "hydropower": "1.5",
            "biogas plant": "1.6",
            "other": ["1.7", "1.8"],
        },
    },
    {
        "question": "What is the installed capacity [kWp] of of your photovoltaic system?",
        "question_id": "1.1",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "How much battery storage capacity [kWh] do you have installed at your site?",
        "question_id": "1.2",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the overall rated power [kW] of the installed diesel generators?",
        "question_id": "1.3",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What ist the capacity [kW] of the installed wind power systems?",
        "question_id": "1.4",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What ist the capacity [kW] of the installed hydropower systems?",
        "question_id": "1.5",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What ist the capacity [kW] of the installed biogas plant??",
        "question_id": "1.6",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "Which other technology do you use for electricity supply?",
        "question_id": "1.7",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "What is the installed capacity [kW] of this other electricity production technology",
        "question_id": "1.8",
        "possible_answers": TYPE_FLOAT,
    },
    ]

# CROP: The list should be crated on the fly a,b,c
# IRRIGATION: The list should be crated on the fly

WATER_SUPPLY_SPECIFIC = {
    "water": "",
    "drinking water": "a",
    "service water": "b",

}

WATER_SUPPLY_TEMPLATE = [{
        "question": "Which water source do you use for TYPE_WATER_USE",
        "question_id": "3",
        "possible_answers": [
            "groundwater well",
            "public tap water",
            "desalinated seawater",
            "river/creek",
            "lake",
            "water truck",
            "rainwater harvesting",
            "bottled water",
            "other",
        ],
        "display_type": "multiple_choice_tickbox",
        "subquestion": {
            "groundwater well": ["3.1"],
            "desalinated seawater": ["3.1"],
            "river/creek": ["3.1"],
            "lake": ["3.1"],
            "water truck": ["3.2"],
            "other": ["3.3"],
        },
    },
    {
        "question": "Are water pumps required to convey water from the source to the point of consumption?",
        "question_id": "3.1",
        "possible_answers": ["Yes", "No"],
        "subquestion": {
            "Yes": ["3.1.1", "3.1.2", "3.1.4"],
        },
    },
    {
        "question": "What is the height difference between the elevation of the water source"
                    "and the elevation of the location where you are using the water (both above sea level)?",
        INFOBOX: "Elevation of the water source refers to for example average elevation of the groundwater level,"
                 " lake surface, or the elevation of the location of river water uptake. We require this information"
                 "to obtain information regarding a potential water pump head",
        "question_id": "3.1.1",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "Which energy source is the pump using?",
        "question_id": "3.1.2",
        "possible_answers": [
            "manual",
            "diesel",
            "electricity (grid)",
            "wind turbine",
            "photovoltaics",
        ],
        "subquestion": {
            "diesel": ["3.1.3"],
            "electricity (grid)": ["3.1.3"],
            "wind turbine": ["3.1.3"],
            "photovoltaics": ["3.1.3"],
        },
    },
    {
        "question": "What is the rated power of the water pump?",
        "question_id": "3.1.3",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the maximum throughput [m³/h] of the water pump",
        "question_id": "3.1.4",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the price of the water provided by truck [$/m³]",
        "question_id": "3.2",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "Which other source do you use for TYPE_WATER_USE",
        "question_id": "3.3",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "Do you encounter water quality issues at your TYPE_WATER_USE source, if yes which?",
        "question_id": "4",
        "possible_answers": [
            "salinity",
            "heavy metals",
            "chemical contamination",
            "fecal contamination",
            "hardness",
            "sediments and turbidity",
            "nitrates and nitrites",
        ],
        "display_type": "multiple_choice_tickbox",
        "subquestion": {
            "salinity": "4.1",
            "heavy metals": "4.2",
            "chemical contamination": "4.3",
        },
    },
    {
        "question": "What is the Salinity of your TYPE_WATER_USE source [g/l]?",
        "question_id": "4.1",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "Which heavy metals are prevalent in your TYPE_WATER_USE source?",
        "question_id": "4.2",
        "possible_answers": ["Arsenic", "Lead", "Mercury", "Cadmium", "Iron"],
        "display_type": "multiple_choice_tickbox",
    },
    {
        "question": "Which chemical contamination is prevalent in your drinking water source?",
        "question_id": "4.3",
        "possible_answers": [
            "pesticides",
            "pharmaceutical_residues",
            "fertilizers",
            "industrial_chemicals",
        ],
        "display_type": "multiple_choice_tickbox",
    },
    {
        "question": "Do you treat your TYPE_WATER_USE, if yes, which technologies are your using?",
        "question_id": "5",
        "possible_answers": [
            "no",
            "reverse osmosis",
            "boiling",
            "distillation",
            "activated carbon filter",
            "chlorination",
            "UV-disinfection",
            "cartridge filter",
            "microfiltration",
            "ultrafiltration",
            "ceramic filter",
            "nanofiltration",
            "electrodialyis",
            "slow sand filter",
            "water softener",
            "membrane distillation",
            "other",
        ],
        "display_type": "multiple_choice_tickbox",
        "subquestion": {
            "reverse osmosis": ["5.1", "5.2", "SEC_DW"],
            "membrane distillation": ["5.1", "5.2", "SEC_DW"],
            "ultrafiltration": ["5.1", "5.2", "SEC_DW"],
            "boiling": ["5.2", "SEC_DW"],
            "distillation": ["5.2", "SEC_DW"],
            "activated carbon filter": ["5.2", "SEC_DW"],
            "UV-disinfection": ["5.2", "SEC_DW"],
            "cartridge filter": ["5.2", "SEC_DW"],
            "microfiltration": ["5.2", "SEC_DW"],
            "ceramic filter": ["5.2", "SEC_DW"],
            "nanofiltration": ["5.2", "SEC_DW"],
            "electrodialyis": ["5.2", "SEC_DW"],
            "slow sand filter": ["5.2", "SEC_DW"],
            "water softener": ["5.2", "SEC_DW"],
            "other": ["5.3", "5.1", "5.2", "SEC_DW"]
        },
    },
    # TODO: map the ticked answers to WT_TYPE
    {
        "question": "What is the recovery rate [%] of your WT_TYPE system?",
        "question_id": "5.1",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the maximum flow rate [m³/h] of your WT_TYPE system?",
        "question_id": "5.2",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "Which other water treatment technologies are you using to treat your TYPE_WATER_USE?",
        "question_id": "5.3",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "What is the specific energy consumption (SEC) [kWh/m³] of your WT_TYPE system",
        "question_id": "SEC_DW",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "Do you typically experience TYPE_WATER_USE shortages from time to time?",
        "question_id": "6",
        "possible_answers": ["Yes", "No"],
    },
]





WATER_SUPPLY_SURVEY_STRUCTURE = [
    {
        "question": "Considering your water supply, do you distinguish between drinking water and service water?",
        INFOBOX: "Service water, also known as non-potable water, refers to water used for various purposes"
                 " other than drinking. It can include water for showering, washing, toilet flushing, irrigation,"
                 " industrial processes, cooling systems, and other non-consumptive applications. Unlike potable water,"
                 " which meets drinking water standards, service water does not need to meet the same quality criteria. "
                 "Its primary function is to support specific activities without being directly consumed by humans.",
        "question_id": "2",
        "possible_answers": ["Yes", "No"],
        "subquestion": {
            "Yes": ["3a", "4a", "5a", "6a", "3b", "4b", "5b", "6b"],
            "No": ["3", "4", "5", "6"]
        }
    },
] + generate_generic_questions(WATER_SUPPLY_SPECIFIC, WATER_SUPPLY_TEMPLATE, text_to_replace="TYPE_WATER_USE") + [
    {
        "question": "How are you treating your waste water?",
        "question_id": "7",
        "possible_answers": [
            "septic system",
            "constructed wetland",
            "centralized waste water treatment plant",
            "decentralized waste water treatment plant",
            "water recycling and reuse system",
            "disposal to environment without treatment",
            "other",
        ],
        "display_type": "multiple_choice_tickbox",
        # TODO: map all ticked answers to WWT_TYPE (Wastewater Treatment Type)
        #  and repeat the following questions for all of them
        "subquestion": {
            "septic system": "7.1",
            "constructed wetland": "7.1",
            "centralized waste water treatment plant": "7.1",
            "decentralized waste water treatment plant": "7.1",
            "water recycling and reuse system": "7.1",
            "disposal to environment without treatment": "7.1",
            #"WWT_Type": "7.1",
            "other": ["7.2", "7.1"],
        },
    },
    # should this question be repeated for each
    {
        "question": "How much wastewater can be handled  [m³/h] by the WWT_TYPE system in place?",
        "question_id": "7.1",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "Please name the wastewater treatment method you are using",
        "question_id": "7.2",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "Which kind of toilet are you using?",
        "question_id": "7.3",
        "possible_answers": [
            "flush toilet",
            "latrine",
            "dry toilet",
            "composting toilet",
            "open field"
        ]
    },
]

CROPS_SURVEY_STRUCTURE = [

    {
        "question": "Are you cultivating crops?",
        "question_id": "8",
        "possible_answers": ["Yes", "No"],
        "subquestion": {"Yes": ["8.1", "9", "10"]},
    },
    {
        "question": "Please list the crops types you are cultivating",
        "question_id": "8.1",
        "possible_answers": [
            "wheat",
            "rice",
            "soy bean",
            "dry bean",
            "peanut",
            "potato",
            "cassava",
            "tomato",
            "sweetcorn",
            "green bean",
            "carrot",
            "cotton",
            "banana",
            "lettuce",
            "cucumber",
            "pineanpple",
            "avocado",
            "quinoa",
            "amaranth",
            "guava",
            "papaya",
            "mango",
            "sorghum",
            "millet",
            "yam",
            "plantain",
            "apple",
            "sunflower",
            "cacao",
            "cashew",
            "pumpkin",
            "black bean",
            "oat",
            "pepper",
            "other",
            "CROP_TYPE",  # put CROP_TYPE here to avoid error; in the end
            # TODO CROP_TYPE related question has to be posed for all stated/ticked crops
        ],
        "display_type": "multiple_choice_tickbox",
        # TODO: map all ticked answers to CROP_TYPE and repeat the following questions for all of them
        "subquestion": {"other": ["8.2", "8.3", "8.4", "8.5"],
                        "CROP_TYPE": ["8.3", "8.4", "8.5"]
                        },
    },
    {
        "question": "Which other crops not mentioned above are you cultivating",
        "question_id": "8.2",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "What is the size of the area on which you are cultivating [CROP_TYPE] [m²]?",
        "question_id": "8.3",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "What is your annual [CROP_TYPE] production [kg]",
        INFOBOX: "Note that here we refer to actual [CROP_TYPE] biomass used for food production",
        "question_id": "8.4",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "How much organic waste occurs annually [kg/year] from the [CROP_TYPE] cultivation in place?",
        "question_id": "8.5",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "Are you interested to combine electricity and crop production on the same land in the form of"
                    " agrivoltaics, the combination of solar photovoltaic systems with agricultural production"
                    " on the same land?",
        "question_id": "10",
        "possible_answers": ["yes", "no"],
    },
]
IRRIGATION_TYPE_SURVEY =[

    {
        "question": "Are you irrigating your CROP_TYPE cultivation?",
        "question_id": "9",
        "possible_answers": ["yes", "no"],
        "subquestion": {"yes": ["9.1", "9.2"]},
    },
    {
        "question": "Please indicate the irrigation technologies you are using",
        "question_id": "9.1",
        "possible_answers": [
            "surface irrigation",
            "center-pivot irrigation",
            "irrigation sprinkler",
            "subsurface drip irrigation",
            "drip irrigation",
            "furrow irrigation",
            "basin irrigation",
            "border irrigation",
            "watering can",
            "smart irrigation system",
            "other",
            "IRRIGATION_TYPE",
        ],
        "display_type": "multiple_choice_tickbox",
        # TODO: map all ticked answers to IRRIGATION TYPE and repeat the following questions for all of them
        "subquestion": {
            "other": ["9.2", "9.3", "9.4"],
            "IRRIGATION_TYPE": ["9.3", "9.4"]
        },
    },
    {
        "question": "What is the maximum flow rate [m³/h] of the IRRIGATION_TYPE system that you have in place?",
        "question_id": "9.3",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the other irrigation technology you are using?",
        "question_id": "9.2",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "For which crop types are you using this irrigation technology?",
        "question_id": "9.4",
        "possible_answers": [  # TODO ideally reduce options to CROP_TYPE which have been ticked in question 8.1
            "wheat",
            "rice",
            "soy bean",
            "dry bean",
            "peanut",
            "potato",
            "cassava",
            "tomato",
            "sweetcorn",
            "green bean",
            "carrot",
            "cotton",
            "banana",
            "lettuce",
            "cucumber",
            "pineanpple",
            "avocado",
            "quinoa",
            "amaranth",
            "guava",
            "papaya",
            "mango",
            "sorghum",
            "millet",
            "yam",
            "plantain",
            "apple",
            "sunflower",
            "cacao",
            "cashew",
            "pumpkin",
            "black bean",
            "oat",
            "pepper",
            "other",
        ],
    }
],


SURVEY_STRUCTURE = COMPONENT_SURVEY_STRUCTURE + WATER_SUPPLY_SURVEY_STRUCTURE + CROPS_SURVEY_STRUCTURE

def infer_survey_categories():
    question_category_map = {}
    for category, question_list in zip((COMPONENT_CATEGORY, WATER_CATEGORY, CROP_CATEGORY),
                                       (COMPONENT_SURVEY_STRUCTURE, WATER_SUPPLY_SURVEY_STRUCTURE,
                                        CROPS_SURVEY_STRUCTURE)):
        for question in question_list:
            question_category_map[question["question_id"]] = category
    return question_category_map

SURVEY_CATEGORIES = infer_survey_categories()



# tick box would be required; other crop: user writes down; feedback to backend developers
# it is not just surveys; hydropower potential has to be assumed from surrounding rivers; input from WEFESiteAnalyst
# Shall there be a way of only modeling the water, energy or agricultural system?
# TODO Troubleshoot line: In case component is already added, avoid double adding
def collect_subquestion_mapping():
    subquestion_mapping = {}
    for question in SURVEY_STRUCTURE:
        subquestions = question.get("subquestion", {})
        for subq in subquestions.values():
            if isinstance(subq, list):
                for sq in subq:
                    if sq not in subquestion_mapping:
                        subquestion_mapping[sq] = question["question_id"]
                    else:
                        if subquestion_mapping[sq] != question["question_id"]:
                            print("problem with subquestion", sq)

            else:
                if subq not in subquestion_mapping:
                    subquestion_mapping[subq] = question["question_id"]
                else:
                    if subquestion_mapping[subq] != question["question_id"]:
                        print("problem with subquestion", subq)

    return subquestion_mapping

def check_subquestions_keys():
    for question in SURVEY_STRUCTURE:
        subquestions = question.get("subquestion", {})
        possible_answers = question.get("possible_answers", [])
        for subq in subquestions.keys():
            if subq not in possible_answers:
                print(f"The subquestion key '{subq}' of question '{question.get('question_id')}' is not listed within the allowed values. The allowed values are:\n{', '.join(possible_answers)}\n\n")

SUB_QUESTION_MAPPING = collect_subquestion_mapping()



def map_subquestions():
    """
    2 has
    subQuestionMapping={"yes": ["3", "4", "5", "6"]})'
    4 has
    subQuestionMapping={"salinity": "4.1", "heavy_metals": "4.2", "chemical_contamination": "4.3"}



    sq_map = {
        1: {
            a1:[{id:1.1, subquestions:{a11:1.1.1}}],
            a2:1.2,
            a3: [1.3, 1.4]}

    }
    (1.2, subquestions)

    it stops when no subquestions
    """

    for question in SURVEY_STRUCTURE:
        subquestions = question.get("subquestion", {})
        for subq in subquestions.keys():
            if subq not in possible_answers:
                print(f"The subquestion key '{subq}' is not listed within the allowed values. The allowed values are:\n{', '.join(possible_answers)}\n\n")
