from django.test import TestCase
import json
from survey import (
    check_subquestions_keys,
    collect_subquestion_mapping,
    check_questions_format,
    SURVEY_STRUCTURE,
    SURVEY_ANSWER_COMPONENT_MAPPING
)




def validate_answer_mapping_against_survey_structure(survey_questions, answer_mapping):
    id_map = {q["question_id"]: q for q in survey_questions}
    visited_ids = set()
    missing_ids = set()
    extra_ids = set(answer_mapping.keys()) - set(id_map.keys())
    missing_answers = {}
    extra_answers = {}

    def visit(qid):
        if qid in visited_ids or qid not in id_map:
            return
        visited_ids.add(qid)
        q = id_map[qid]

        # Check for missing question_id in mapping
        if qid not in answer_mapping:
            missing_ids.add(qid)
        else:
            mapping_entry = answer_mapping[qid]
            # If the mapping is a dict and question has possible answers, compare them
            if isinstance(mapping_entry, dict) and "possible_answers" in q:
                pa = q["possible_answers"]
                if isinstance(pa, list):
                    mapped_answers = set(mapping_entry.keys())
                    variable_name = q.get("variable_name")
                    if variable_name is not None:

                        if variable_name not in mapped_answers:
                            missing_answers[qid] = variable_name
                        else:
                            if len(mapped_answers) > 1:
                                extra_answers[qid] = mapped_answer - set([variable_name])
                    else:
                        expected_answers = set(q["possible_answers"])
                        missing = expected_answers - mapped_answers
                        if missing:
                            missing_answers[qid] = missing
                        extra = mapped_answers - expected_answers
                        if extra:
                            extra_answers[qid] = extra

            # TODO add extras here ....

        # Recurse into subquestions
        if "subquestion" in q:
            for targets in q["subquestion"].values():
                for sub_id in targets:
                    visit(sub_id)

    # Start traversal from all top-level questions
    for q in survey_questions:
        visit(q["question_id"])

    return {
        "missing_question_ids": missing_ids,
        "extra_question_ids": extra_ids,
        "missing_answers": missing_answers,
        "extra_answers": extra_answers,

    }


if __name__ == "__main__":
    check_subquestions_keys()
    collect_subquestion_mapping()
    check_questions_format()

    results = validate_answer_mapping_against_survey_structure(SURVEY_STRUCTURE, SURVEY_ANSWER_COMPONENT_MAPPING)

    print("Missing question IDs:", sorted(results["missing_question_ids"]))
    print("Extra question IDs in mapping:", sorted(results["extra_question_ids"]))

    for qid, answers in results["missing_answers"].items():
        print(f"❌ Question {qid} is missing mappings for answers: {sorted(answers)}")

    for qid, answers in results["extra_answers"].items():
        print(f"⚠️ Question {qid} has extra mappings for answers not in survey: {sorted(answers)}")
