import copy
from django.utils.translation import gettext_lazy as _
import logging


TYPE_FLOAT = "float"
TYPE_INT = "int"
TYPE_STRING = "string"
TYPE_WATER = "string"
INFOBOX = "description"


# TODO add existing capacities to the csv files
# TODO add all components in component mapping in correct format
# TODO probably subquestions have to be marked/named differently
#  so that they not pop up if not induced by specific answers

# TODO the answer from float does not need to be a dict {"capacity":TYPE_FLOAT}
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
    # TODO "2" define water cycles service and drinking water; in case there are both cycles
    #  -> add a); and b) to each of the following mapping questions;
    #  and connect accordingly to service and drinking water buses
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
    "3.1": {
        "Yes": ["water-pump"]
    },
    },
    "3.1.1": {"head": TYPE_FLOAT},
    "3.1.3": {"capacity": TYPE_FLOAT},
    "3.1.4": {"flow_max": TYPE_FLOAT},
    # TODO check whether flow max is the right column name for maximum throughput
    "3.2": {"water-truck/marginal_cost": TYPE_FLOAT},
},

COMPONENT_CATEGORY = "components"
WATER_CATEGORY = "water"
CROP_CATEGORY = "crops"

SURVEY_QUESTIONS_CATEGORIES = {
    COMPONENT_CATEGORY: _("Components"),
    WATER_CATEGORY: _("Water"),
    CROP_CATEGORY: _("Crops"),
}


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
            "biogas plant"
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
            "groundwater well"
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
            "photovoltaic system": ["3.1.3"],
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
            "reverse_osmosis",
            "boiling",
            "distillation",
            "activated_carbon_filter",
            "chlorination",
            "UV-disinfection",
            "cartridge_filter",
            "microfiltration",
            "ultrafiltration",
            "ceramic_filter",
            "nanofiltration",
            "electrodialyis",
            "slow_sand_filter",
            "water_softener",
            "membrane_distillation",
            "other",
        ],
        "display_type": "multiple_choice_tickbox",
        "subquestion": {
            "reverse_osmosis": [
                "5.1",
                "SEC_DW",
            ],
            "membrane_distillation": [
                "5.1",
                "SEC_DW",
            ],
            "ultrafiltration": [
                "5.1",
                "SEC_DW",
            ],
            "boiling": ["5.2", "SEC_DW"],
            "distillation": ["5.2", "SEC_DW"],
            "activated_carbon_filter": ["5.2", "SEC_DW"],
            "UV-disinfection": ["5.2", "SEC_DW"],
            "cartridge_filter": ["5.2", "SEC_DW"],
            "microfiltration": ["5.2", "SEC_DW"],
            "ultrafiltration": ["5.2", "SEC_DW"],
            "ceramic_filter": ["5.2", "SEC_DW"],
            "nanofiltration": ["5.2", "SEC_DW"],
            "electrodialyis": ["5.2", "SEC_DW"],
            "slow_sand_filter": ["5.2", "SEC_DW"],
            "water_softener": ["5.2", "SEC_DW"],
            "other": "5.3",
        },
    },
    {
        "question": "What is the recovery rate [%] of your [name of ticked treatment technology]?",
        "question_id": "5.1",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the maximum throughput rate [m³/h] of your [name of ticked treatment technology] system?",
        "question_id": "5.2",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the specific energy consumption [kWh/m³] of your [name of ticket treatment technology]"
                    " system",
        "question_id": "SEC_DW",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "Which other water treatment technologies are you using to treat your "
                    "[name of ticked treatment technology]",
        "question_id": "5.3",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "Do you typically experience TYPE_WATER_USE shortages from time to time?",
        "question_id": "6",
        "possible_answers": ["Yes", "No"],
    },
]



def generate_water_questions(suffixes, survey_questions):
    new_questions = []
    for name, suffix in suffixes.items():
        temp = copy.deepcopy(survey_questions)
        for question in temp:
            question["question"] = question["question"].replace("TYPE_WATER_USE", name)
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
            "yes": ["3a", "4a", "5a", "6a", "3b", "4b", "5b", "6b"],
            "no": ["3", "4", "5", "6"]
        }
    },
] + generate_water_questions(WATER_SUPPLY_SPECIFIC, WATER_SUPPLY_TEMPLATE) + [
    {
        "question": "How are you treating your waste water?",
        "question_id": "7",
        "possible_answers": [
            "septic system",
            "constructed_wetland",
            "centralized_waste_water_treatment_plant",
            "decentralized_waste_water_treatment_plant",
            "recycling_and_reuse_systems",
            "no_treatment_disposal_to_environment",
            "other",
        ],
        "display_type": "multiple_choice_tickbox",
        "subquestion": {
            "septic_system": "7.1",
            "constructed_wetlands": "7.1",
            "centralized_waste_water_treatment_plant": "7.1",
            "decentralized_waste_water_treatment_plant": "7.1",
            "recycling_and_reuse_systems": "7.1",
            "other": ["7.1", "7.2"],
        },
    },
    # should this question be repeated for each
    {
        "question": "How much wastewater can be handled per day [m³/d] by this facility?",
        "question_id": "7.1",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "Please specify 'Other'",
        "question_id": "7.2",
        "possible_answers": TYPE_STRING,
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
            "tomato",
            "potato",
            "raspberry",
            "corn",
            "wheat",
            "soybean",
            "carrot",
            "lettuce",
            "strawberry",
            "cucumber",
            "cassava",
            "sweet_potato",
            "quinoa",
            "amaranth",
            "pineapple",
            "guava",
            "papaya",
            "avocado",
            "mango",
            "sorghum",
            "millet",
            "yam",
            "plantain",
            "maca",
            "aji_amarillo",
            "malagueta_pepper",
            "chuño",
            "yacón",
            "peanut",
            "sunflower",
            "custard_apple",
            "arrowroot",
            "cacao",
            "cashew",
            "pumpkin",
            "squash",
            "ullucu",
            "oca",
            "beans",
            "tapioca",
            "other",
        ],
        "display_type": "multiple_choice_tickbox",
        "subquestion": {"other": "8.2"},
    },
    {
        "question": "Which other crops are you cultivating",
        "question_id": "8.2",
        "possible_answers": TYPE_STRING,
    },

    #TODO define CROP_TYPE ask all the following question for the specific crop type: Cultivation area;
    # annual crop production in [t], do you irrigate CROP_TYPE"
    {
        "question": "What is the size of the area on which you are cultivating [CROP_TYPE] [m²]?",
        "question_id": "8.3",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "Are you interested to combine electricity and crop production on the same land in the form of"
                    " agrivoltaics, the combination of solar photovoltaic systems with agricultural production"
                    " on the same land??",
        "question_id": "10",
        "possible_answers": ["yes", "no"],
    },
]
IRRIGATION_TYPE_SURVEY =[

    {
        "question": " Do you use irrigation systems?",
        "question_id": "9",
        "possible_answers": ["yes", "no"],
        "subquestion": {"yes": ["9.1", "9.2"]},
    },

    {
        "question": "Please indicate the irrigation technologies you are using",
        "question_id": "9.1",
        "possible_answers": [
            "surface_irrigation",
            "center-pivot_irrigation",
            "irrigation_sprinkler",
            "subsurface_drip_irrigation",
            "drip_irrigation",
            "furrow_irrigation",
            "basin_irrigation",
            "border_irrigation",
            "watering_can",
            "smart_irrigation_system",
            "other",
        ],
        "display_type": "multiple_choice_tickbox",
        "subquestion": {
            "surface_irrigation": "9.1.1",
            "center-pivot_irrigation": "9.1.2",
            "irrigation_sprinkler": "9.1.3",
            "subsurface_drip_irrigation": "9.1.4",
            "drip_irrigation": "9.1.5",
            "furrow_irrigation": "9.1.6",
            "basin_irrigation": "9.1.7",
            "border_irrigation": "9.1.8",
            "watering_can": "9.1.9",
            "smart_irrigation_system": "9.1.10",
            "other": ["9.1.11", "9.1.12"],
        },
    },
    # TODO Simplify here ask question for specific irrigation type
    {
        "question": "What is the maximum throughput [m³/h] of your installed surface irrigation system?",
        "question_id": "9.1.1",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the maximum throughput [m³/h] of your installed center-plot irrigation system?",
        "question_id": "9.1.2",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the maximum throughput [m³/h] of your installed irrigation sprinkler system?",
        "question_id": "9.1.3",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the maximum throughput [m³/h] of your installed subsurface drip irrigation system?",
        "question_id": "9.1.4",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the maximum throughput [m³/h] of your drip irrigation system?",
        "question_id": "9.1.5",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the maximum throughput [m³/h] of your furrow irrigation system?",
        "question_id": "9.1.6",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the maximum throughput [m³/h] of your basin irrigation system?",
        "question_id": "9.1.7",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "What is the maximum throughput [m³/h] of your border irrigation system?",
        "question_id": "9.1.8",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "How much water can you apply to your plants per hour [m³/h] using watering cans?",
        "question_id": "9.1.9",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "Which other irrigation technology are you using?",
        "question_id": "9.1.11",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "What is the maximum throughput [m³/h] of this other irrigation technology you have installed?",
        "question_id": "9.1.12",
        "possible_answers": TYPE_FLOAT,
    },
    {
        "question": "Which of your crops are served by the irrigation system?",
        "question_id": "9.2",
        "possible_answers": TYPE_STRING,  # TODO: options shall be ticked crops above!
    },
],


SURVEY_STRUCTURE = COMPONENT_SURVEY_STRUCTURE + WATER_SUPPLY_SURVEY_STRUCTURE + CROPS_SURVEY_STRUCTURE

def infer_survey_categories():
    question_category_map = {}
    for category, question_list in zip((COMPONENT_CATEGORY, WATER_CATEGORY, CROP_CATEGORY),(COMPONENT_SURVEY_STRUCTURE, WATER_SUPPLY_SURVEY_STRUCTURE, CROPS_SURVEY_STRUCTURE)):
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
                print(f"The subquestion key '{subq}' is not listed within the allowed values. The allowed values are:\n{', '.join(possible_answers)}\n\n")

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
