import json
from survey.survey import SUB_QUESTION_MAPPING, SURVEY_STRUCTURE, get_survey_question_by_id, TYPE_COMPONENT, TYPE_COMPONENT_ATTRIBUTE


mapping={}
possible_answers = []
for q in SURVEY_STRUCTURE:
    q_id = q["question_id"]
    pa = q.get("possible_answers")
    map_to = q.get("answer_map_to")
    if map_to is not None:
        if pa is not None:
            if isinstance(pa, list):
                variable_name = q.get("variable_name")
                if variable_name is not None:
                    mapping[q_id] = {
                        "map_to": map_to,
                        "map_answer": {variable_name:pa},
                    }
                else:
                    mapping[q_id] = {
                        "map_to": map_to,
                        "map_answer": {k:[""] for k in pa if k not in ("other", "Other")},
                    }
            else:
                variable_name = q.get("variable_name", "variable_name")
                mapping[q_id] = {
                    "map_to": map_to,
                    "map_answer": {variable_name: pa},
                }


with open("survey_answer_component_mapping.json", "w") as fp:
    json.dump(mapping,fp,indent=4)

with open("sub_question_mapping.json", "w") as fp:
    json.dump(SUB_QUESTION_MAPPING, fp, indent=4)

with open("survey_questions.json", "w") as fp:
    json.dump(SURVEY_STRUCTURE, fp, indent=4)