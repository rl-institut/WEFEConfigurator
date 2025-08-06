from django.shortcuts import *
from django.urls import reverse
from .forms import *
from .models import *
from .survey import SURVEY_CATEGORIES, SURVEY_STRUCTURE, get_survey_question_by_id
import logging
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


def is_matrix_source(field):
    field_classes = field.widget.attrs.get("class")
    answer = False
    if field_classes is not None:
        if "matrix_source" in field_classes:
            answer = True
    return answer


@require_http_methods(["GET", "POST"])
def view_survey_questions(request, scen_id=None):

    if request.method == "POST":
        form = SurveyQuestionForm(
            request.POST, qs=SurveyAnswer.objects.filter(scenario_id=scen_id)
        )

        if form.is_valid():
            qs = SurveyAnswer.objects.filter(scenario_id=scen_id)
            with open(f"scenario_{scen_id}_survey_answers.json", "w") as fp:
                json.dump(form.cleaned_data, fp, indent=4)
            for criteria_num, value in form.cleaned_data.items():
                crit = qs.get(question_id=criteria_num.replace("criteria_", ""))
                crit.value = value
                crit.save(update_fields=["value"])

            answer = HttpResponseRedirect(reverse("view_survey", args=[scen_id]))
        else:
            # TODO
            print("Form is not valid")
            # import pdb;
            # pdb.set_trace()

    else:
        if scen_id is None:
            last_scenario_id = SurveyAnswer.objects.all().values_list("scenario_id",flat=True).distinct().order_by().last()
            if last_scenario_id is None:
                last_scenario_id = 0
            scenario_id = last_scenario_id + 1
            answer = HttpResponseRedirect(reverse("view_survey", args=[scenario_id]))
        else:
            scenario_id = scen_id

            # Check if answers already exists, if not create them
            qs_answer = SurveyAnswer.objects.filter(scenario_id=scenario_id)
            # import pdb;pdb.set_trace()
            if qs_answer.exists() is False:
                questions = SurveyQuestion.objects.all()
                print(questions)
                for question in questions:
                    #print(question)
                    answer_param = {}
                    answer_param["scenario_id"] = scenario_id
                    answer_param["question"] = question
                    new_answer = SurveyAnswer(**answer_param)
                    new_answer.save()
                qs_answer = SurveyAnswer.objects.filter(scenario_id=scenario_id)

            categories = [cat for cat in SURVEY_QUESTIONS_CATEGORIES.keys()]
            form = SurveyQuestionForm(qs=qs_answer)

            categories_map = []
            matrix_headers = {}
            matrix_labels = {}
            for field in form.fields:
                question_id = field.split("criteria_")[1]
                # TODO: could be done from models "category" attribute
                cat = SURVEY_CATEGORIES.get(question_id)
                # TODO: reassign cat after testing phase is over
                categories_map.append("components")
                # TODO here one can know that the question
                if is_matrix_source(form.fields[field]):
                    subs = []
                    labels = []
                    question = get_survey_question_by_id(SURVEY_STRUCTURE, question_id)
                    for answer, subquestions in question["subquestion"].items():
                        labels.append(answer)
                        for sq_id in subquestions:
                            q_main_id = ".".join(sq_id.split(".")[:2])
                            subquestion = get_survey_question_by_id(SURVEY_STRUCTURE, sq_id)
                            # print(subquestion)
                            if subquestion.get("display_type", "") == "matrix":
                                if subquestion["question"] not in subs:
                                    subs.append(subquestion["question"])
                    matrix_headers[field] = subs
                    matrix_labels[field] = labels

            answer = render(
                request,
                "survey_layout.html",
                {
                    "form": form,
                    "scen_id": scenario_id,
                    "categories_map": categories_map,
                    "categories": categories,
                    "categories_verbose": SURVEY_QUESTIONS_CATEGORIES,
                    "matrix_headers": matrix_headers,
                    "matrix_labels": matrix_labels,
                },
            )

    return answer
