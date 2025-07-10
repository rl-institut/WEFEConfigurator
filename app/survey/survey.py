import copy
import functools
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
        "biogas plant": "biogas_plant",  # TODO: biogas model in csv. format has to be created (can be inspired by OWEFE)
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
            "service-water-storage",
        ],
        "water truck": "water-truck",
        "public tap water": "tap-water",
    },
    "3.1": {"Yes": ["water-pump"]},
    "3.1.1": {"head": TYPE_FLOAT},
    "3.1.3": {"capacity": TYPE_FLOAT},
    "3.1.4": {"flow_max": TYPE_FLOAT},
    "3.2": {"water-truck/marginal_cost": TYPE_FLOAT},
    "4": {
        "salinity": ["ro"],
        "chemical contamination": ["ion_exchange", "membrane_filtration"],
    },
    # TODO add (decentralized) Treatment options for "fecal contamination","hardness","sediments and turbidity",
    # "nitrates and nitrites", pesticides, pharmaceutical_residues, fertilizers, industrial_chemicals
    "4.1": {"SOURCE_WATER_TYPE/salinity": TYPE_FLOAT},
    "5": {
        "reverse_osmosis": ["ro"],
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
        "other": TYPE_STRING,
    },
    "5.1": {"WT_TYPE/recovery_rate": TYPE_FLOAT},
    "5.2": {"WT_TYPE/capacity": TYPE_FLOAT},
    "5.3": {"WT_TYPE/SEC": TYPE_FLOAT},
    "7": {
        "septic system": ["septic_system"],
        "constructed_wetland": ["constructed_wetland"],
        "centralized waste water treatment plant": ["cWWTP"],
        "decentralized waste water treatment plant": ["dWWTP"],
        "recycling and reuse system": ["RR"],
        "disposal to environment without treatment": ["direct_wastewater_disposal"],
    },
    "7.1": {"selected WWT_TYPE/capacity": TYPE_FLOAT},
    "7.3": {
        "flush toilet": ["flush_toilet"],
        "latrine": ["latrine"],
        "dry toilet": ["dry_toilet"],
        "composting toilet": ["composting_toilet"],
        "open filed": ["open_field"],
    },
    "8": {
        "wheat": ["wheat"],
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
    "10": {"yes": ["apv"]},
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


def get_survey_question_by_id(survey_questions, question_id):
    answer = None
    for q in survey_questions:
        if q["question_id"] == question_id:
            if answer is None:
                answer = q
            else:
                msg = f"Question number {question_id} appears multiple times"
                raise KeyError(msg)
    return answer


def get_survey_question_index(survey_questions, question):
    if isinstance(question, dict):
        q_id = question["question_id"]
    elif isinstance(question, str):
        q_id = question

    q_idx = None
    for i, q in enumerate(survey_questions):
        if q["question_id"] == q_id:
            q_idx = i
    return q_idx


def remove_question(survey_questions, question):
    q_id = question["question_id"]
    q_idx = None
    for i, q in enumerate(survey_questions):
        if q["question_id"] == q_id:
            q_idx = i
    if q_idx is not None:
        return survey_questions.pop(q_idx)


def get_shared_subquestions(subquestions):
    shared_subquestions_mapping = {}

    for k, v in subquestions.items():
        if not isinstance(v, list):
            v = [v]
        for sq in v:
            if sq in shared_subquestions_mapping:
                shared_subquestions_mapping[sq].append(k)
            else:
                shared_subquestions_mapping[sq] = [k]

    shared_subquestions = {}
    for k, v in shared_subquestions_mapping.items():
        if len(v) > 1:
            shared_subquestions[k] = v
    return shared_subquestions


def compare_matrix_questions(q1, q2):
    return int(q1["question_id"].split(".")[-1]) - int(q2["question_id"].split(".")[-1])


def generate_matrix_questions(survey_questions, text_to_replace):
    extra_questions = {}
    extra_questions_size = {}
    for qi, q in enumerate(survey_questions):
        if (
            q.get("display_type", "") == "multiple_choice_tickbox"
            and "subquestion" in q
        ):
            extra_number = 0
            sq = q["subquestion"]
            # get the list of question's answers which share the same link to a subquestion
            shared_subquestions = get_shared_subquestions(sq)
            # for each subquestion, if this one has the display type 'matrix', we will make as many copies of it
            # as there are question's answer with a link to the subquestion
            for ssq_id in shared_subquestions:
                ssq = get_survey_question_by_id(survey_questions, ssq_id)
                if ssq.get("display_type", "") == "matrix":
                    extra_questions[ssq_id] = []
                    for suffix, supra_answer in enumerate(shared_subquestions[ssq_id]):
                        temp = copy.deepcopy(ssq)
                        temp["question"] = temp["question"].replace(
                            text_to_replace, supra_answer
                        )
                        temp["question_id"] = ssq_id + "." + str(suffix)
                        # Replace the subquestion id in the supraquestion subquestions
                        if isinstance(q["subquestion"][supra_answer], str):
                            q["subquestion"][supra_answer] = temp["question_id"]
                        else:
                            q["subquestion"][supra_answer][
                                q["subquestion"][supra_answer].index(ssq_id)
                            ] = temp["question_id"]
                        extra_questions[ssq_id].append(temp)
                    # update the number of extra questions
                    extra_number += len(extra_questions[ssq_id])
                if extra_number > 0:
                    extra_questions_size[q["question_id"]] = extra_number

    for q_id in extra_questions:
        # find the original question index in the survey questions
        q_idx = get_survey_question_index(survey_questions, q_id)
        # insert the matrix subquestions
        survey_questions = (
            survey_questions[: q_idx + 1]
            + extra_questions[q_id]
            + survey_questions[q_idx + 1 :]
        )
        # remove the original question from the survey questions
        survey_questions.pop(q_idx)

    # sort the matrix questions by rows instead of by columns (only for display purposes)
    for q_id in extra_questions_size:
        q_idx = survey_questions.index(
            get_survey_question_by_id(survey_questions, q_id)
        )
        col_sorted_questions = survey_questions[
            q_idx + 1 : q_idx + 1 + extra_questions_size[q_id]
        ]
        row_sorted_questions = sorted(
            col_sorted_questions, key=functools.cmp_to_key(compare_matrix_questions)
        )
        survey_questions[q_idx + 1 : q_idx + 1 + extra_questions_size[q_id]] = (
            row_sorted_questions
        )

    return survey_questions


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
        "question": "What is the installed capacity [kWp] of your photovoltaic system?",
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

WATER_SUPPLY_TEMPLATE = [
    {
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
        "display_type": "multiple_choice_tickbox",
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
            "membrane distillation",
            "ultrafiltration",
            "boiling",
            "distillation",
            "activated carbon filter",
            "UV-disinfection",
            "cartridge filter",
            "microfiltration",
            "ceramic filter",
            "nanofiltration",
            "electrodialyis",
            "slow sand filter",
            "water softener",
            "chlorination",
            "other",
        ],
        "display_type": "multiple_choice_tickbox",
        "subquestion": {
            "reverse osmosis": ["5.1", "5.2", "5.3"],
            "membrane distillation": ["5.1", "5.2", "5.3"],
            "ultrafiltration": ["5.1", "5.2", "5.3"],
            "boiling": ["5.2", "5.3"],
            "distillation": ["5.2", "5.3"],
            "activated carbon filter": ["5.2", "5.3"],
            "UV-disinfection": ["5.2", "5.3"],
            "cartridge filter": ["5.2", "5.3"],
            "microfiltration": ["5.2", "5.3"],
            "ceramic filter": ["5.2", "5.3"],
            "nanofiltration": ["5.2", "5.3"],
            "electrodialyis": ["5.2", "5.3"],
            "slow sand filter": ["5.2", "5.3"],
            "water softener": ["5.2", "5.3"],
            "other": ["5.4", "5.1", "5.2", "5.3"],
        },
    },
    {
        "question": "What is the recovery rate [%]",  #  of your WT_TYPE system?
        "question_id": "5.1",
        "possible_answers": TYPE_FLOAT,
        "display_type": "matrix",
    },
    {
        "question": "What is the maximum flow rate [m³/h]",  #  of your WT_TYPE system?
        "question_id": "5.2",
        "possible_answers": TYPE_FLOAT,
        "display_type": "matrix",
    },
    {
        "question": "What is the specific energy consumption (SEC) [kWh/m³]",  #  of your WT_TYPE system?
        "question_id": "5.3",
        "possible_answers": TYPE_FLOAT,
        "display_type": "matrix",
    },
    {
        "question": "Which other water treatment technologies are you using to treat your TYPE_WATER_USE?",
        "question_id": "5.4",
        "possible_answers": TYPE_STRING,
    },
    {
        "question": "Do you typically experience TYPE_WATER_USE shortages from time to time?",
        "question_id": "6",
        "possible_answers": ["Yes", "No"],
    },
]

WATER_SUPPLY_TEMPLATE = generate_matrix_questions(
    survey_questions=WATER_SUPPLY_TEMPLATE, text_to_replace="WT_TYPE"
)


WATER_SUPPLY_SURVEY_STRUCTURE = (
    [
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
                "No": ["3", "4", "5", "6"],
            },
        },
    ]
    + generate_generic_questions(
        WATER_SUPPLY_SPECIFIC, WATER_SUPPLY_TEMPLATE, text_to_replace="TYPE_WATER_USE"
    )
    + generate_matrix_questions(
        survey_questions=[
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
                "subquestion": {
                    "septic system": "7.1",
                    "constructed wetland": "7.1",
                    "centralized waste water treatment plant": "7.1",
                    "decentralized waste water treatment plant": "7.1",
                    "water recycling and reuse system": "7.1",
                    "other": ["7.2", "7.1"],
                },
            },
            {
                "question": "How much wastewater can be handled  [m³/h] by the WWT_TYPE system in place?",
                "question_id": "7.1",
                "possible_answers": TYPE_FLOAT,
                "display_type": "matrix",
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
                    "open field",
                ],
            },
        ],
        text_to_replace="WWT_TYPE",
    )
)


CROPS_SURVEY_STRUCTURE = (
    [
        # TODO try commenting this out or to get question up
        {
            "question": "Are you cultivating crops?",
            "question_id": "8",
            "possible_answers": ["Yes", "No"],
            "subquestion": {"Yes": ["11", "9", "10"]},
        }
    ]
    + generate_matrix_questions(
        survey_questions=[
            {
                "question": "Please list the crops types you are cultivating",
                "question_id": "11",
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
                    "pineapple",
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
                "display_type": "multiple_choice_tickbox",
                "subquestion": {
                    "wheat": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "rice": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "soy bean": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "dry bean": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "peanut": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "potato": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "cassava": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "tomato": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "sweetcorn": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "green bean": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "carrot": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "cotton": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "banana": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "lettuce": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "cucumber": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "pineapple": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "avocado": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "quinoa": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "amaranth": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "guava": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "papaya": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "mango": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "sorghum": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "millet": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "yam": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "plantain": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "apple": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "sunflower": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "cacao": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "cashew": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "pumpkin": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "black bean": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "oat": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "pepper": ["11.1", "11.2", "11.3", "11.4", "11.5"],
                    "other": ["8.2", "11.1", "11.2", "11.3", "11.4", "11.5"],
                },
            },
            {
                "question": "What is the size of the area on which you are cultivating [m²]?",
                "question_id": "11.1",
                "possible_answers": TYPE_STRING,
                "display_type": "matrix",
            },
            {
                "question": "What is your annual production [kg]",
                INFOBOX: "Note that here we refer to actual [CROP_TYPE] biomass used for food production",
                "question_id": "11.2",
                "possible_answers": TYPE_STRING,
                "display_type": "matrix",
            },
            {
                "question": "How much organic waste occurs annually [kg/year] from the cultivation in place?",
                "question_id": "11.3",
                "possible_answers": TYPE_FLOAT,
                "display_type": "matrix",
            },
            {
                "question": "Please indicate the irrigation technology you are using",
                "question_id": "11.4",
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
                ],
                "display_type": "matrix",
            },
            {
                "question": "What is the maximum flow rate [m³/h] of the irrigation system that you have in place?",
                "question_id": "11.5",
                "possible_answers": TYPE_FLOAT,
                "display_type": "matrix",
            },
        ],
        text_to_replace="CROP_TYPE",
    )
    + [
        {
            "question": "Which other crops not mentioned above are you cultivating",
            "question_id": "8.2",
            "possible_answers": TYPE_STRING,
        },
        {
            "question": "Are you interested to combine electricity and crop production on the same land in the form of"
            " agrivoltaics, the combination of solar photovoltaic systems with agricultural production"
            " on the same land?",
            "question_id": "10",
            "possible_answers": ["yes", "no"],
        },
    ]
)
IRRIGATION_TYPE_SURVEY = [
        {
            "question": "Are you irrigating your CROP_TYPE cultivation?",
            "question_id": "9",
            "possible_answers": ["yes", "no"],
            "subquestion": {"yes": ["9.1", "9.2"]},
        },]  + generate_matrix_questions(
        survey_questions=[
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
            ],
            "display_type": "multiple_choice_tickbox",
            # TODO: map all ticked answers to IRRIGATION TYPE and repeat the following questions for all of them
            "subquestion": {
                "other": ["9.2", "9.3", "9.4"],
                "surface irrigation": ["9.3", "9.4"],
                "center-pivot irrigation": ["9.3", "9.4"],
                "irrigation sprinkler": ["9.3", "9.4"],
                "subsurface drip irrigation": ["9.3", "9.4"],
                "drip irrigation": ["9.3", "9.4"],
                "furrow irrigation": ["9.3", "9.4"],
                "basin irrigation": ["9.3", "9.4"],
                "border irrigation": ["9.3", "9.4"],
                "watering can": ["9.3", "9.4"],
                "smart irrigation system": ["9.3", "9.4"],
            },
        },
        {
            "question": "What is the maximum flow rate [m³/h] of the IRRIGATION_TYPE system that you have in place?",
            "question_id": "9.3",
            "possible_answers": TYPE_FLOAT,
            "display_type": "matrix",
        },
        {
            "question": "For which crop types are you using this irrigation technology?",
            "question_id": "9.4",
            "display_type": "matrix",
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
                "pineapple",
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
        },
    ],
    text_to_replace="CROP_TYPE",

) + [
    {
        "question": "What is the other irrigation technology you are using?",
        "question_id": "9.2",
        "possible_answers": TYPE_STRING,
    },
]


SURVEY_STRUCTURE = (
    COMPONENT_SURVEY_STRUCTURE + WATER_SUPPLY_SURVEY_STRUCTURE + CROPS_SURVEY_STRUCTURE #+ IRRIGATION_TYPE_SURVEY
)


def infer_survey_categories():
    question_category_map = {}
    for category, question_list in zip(
        (COMPONENT_CATEGORY, WATER_CATEGORY, CROP_CATEGORY),
        (
            COMPONENT_SURVEY_STRUCTURE,
            WATER_SUPPLY_SURVEY_STRUCTURE,
            CROPS_SURVEY_STRUCTURE,
        ),
    ):
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
                print(
                    f"The subquestion key '{subq}' of question '{question.get('question_id')}' is not listed within the allowed values. The allowed values are:\n{', '.join(possible_answers)}\n\n"
                )


def check_questions_format():
    for i, question in enumerate(SURVEY_STRUCTURE):
        if "question_id" not in question:
            print(
                f"{i}th question of the survey does not have the mandatory field 'question_id'"
            )


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
                print(
                    f"The subquestion key '{subq}' is not listed within the allowed values. The allowed values are:\n{', '.join(possible_answers)}\n\n"
                )
