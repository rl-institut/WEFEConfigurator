import json
from django.core.management.base import BaseCommand
from survey.models import SurveyQuestion, SurveyAnswer
from survey.survey import SURVEY_STRUCTURE, TYPE_STRING, SUB_QUESTION_MAPPING


class Command(BaseCommand):
    help = "Save as json the answers to a survey for given scenario(s)"


    def add_arguments(self, parser):
        parser.add_argument("scen_id", nargs="+", type=int)

    def handle(self, *args, **options):
        for scen_id in options["scen_id"]:
            qs = SurveyAnswer.objects.filter(scenario_id=scen_id)

            survey_answers = {}
            for ans in qs:
                survey_answers.update(ans.export(ignore_empty=True))

            with open(f"survey_answers_scenario_{scen_id}.json", "w") as fp:
                json.dump(survey_answers, fp, indent=4)