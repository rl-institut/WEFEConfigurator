import logging

# TODO for now this is pseudo code for example purpose
SURVEY_ANSWER_COMPONENT_MAPPING = {
    "question1": {"yes": "component_name"},
    "question2": {"no": "component_name", "yes": "other_component_name"},
}

def create_components_list(survey_data):
    """Extrapolate the component of the energy system from the survey answers

    :param survey_data: dict with survey question code as key and the answer to the question as value
    :return:
    """
    component_list = []
    for question, survey_answer in survey_data.items():
        if question in SURVEY_ANSWER_COMPONENT_MAPPING:
            possible_answers = SURVEY_ANSWER_COMPONENT_MAPPING[question]
            if survey_answer in possible_answers:
                component_list.append(possible_answers[survey_answer])
        else:
            logging.info(f"Survey question '{question}' is not in the component mapping to build an energy system")
    return component_list

def create_timeseries(survey_data):
    """Based on survey data fetch the relevant timeseries"""
    # TODO clarify what in the survey data could help us download/select timeseries to assign to components
    # TODO maybe add this to create_components_list()
    pass