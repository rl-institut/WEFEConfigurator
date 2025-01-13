from django.shortcuts import *
from django.urls import reverse
from .forms import *
from .models import *
from .survey import SURVEY_CATEGORIES
import logging
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def view_survey_questions(request, scen_id=None):
    if request.method == "POST":
        form = SurveyQuestionForm(request.POST, qs=SurveyAnswer.objects.filter(scenario_id=scen_id))

        if form.is_valid():
            qs = SurveyAnswer.objects.filter(scenario_id=scen_id)

            for criteria_num, value in form.cleaned_data.items():
                crit = qs.get(question_id=criteria_num.replace("criteria_", ""))
                crit.value = value
                crit.save(update_fields=["value"])

            answer = HttpResponseRedirect(reverse("view_survey", args=[scen_id]))
        else:
            # TODO
            import pdb;
            pdb.set_trace()

    else:
        # TODO this is currently for testing
        if scen_id is None:
            scenario_id = 1
        else:
            scenario_id = scen_id

        # Check if answers already exists, if not create them
        qs = SurveyAnswer.objects.filter(scenario_id=scenario_id)
        if qs.exists() is False:
            questions = SurveyQuestion.objects.all()
            for question in questions:
                answer_param = {}
                answer_param["scenario_id"] = scenario_id
                answer_param["question"] = question
                new_answer = SurveyAnswer(**answer_param)
                new_answer.save()

        categories = [cat for cat in SURVEY_QUESTIONS_CATEGORIES.keys()]

        form = SurveyQuestionForm(
            qs=SurveyAnswer.objects.filter(scenario_id=scenario_id)
        )

        categories_map = []
        for field in form.fields:
            question_id = field.split("criteria_")[1]
            # TODO: could be done from models "category" attribute
            cat = SURVEY_CATEGORIES[question_id]
            # TODO: reassign cat after testing phase is over
            categories_map.append("components")

        answer = render(
            request,
            "survey_layout.html",
            {
                "form": form,
                "scen_id": scenario_id,
                "categories_map": categories_map,
                "categories": categories,
                "categories_verbose": SURVEY_QUESTIONS_CATEGORIES,
            },
        )

    return answer
