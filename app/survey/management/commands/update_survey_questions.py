import json
from django.core.management.base import BaseCommand
from survey.models import SurveyQuestion
from survey.survey import SURVEY_STRUCTURE, TYPE_STRING, SUB_QUESTION_MAPPING


class Command(BaseCommand):
    help = "Update the survey question objects from SURVEY_STRUCTURE"

    def add_arguments(self, parser):
        parser.add_argument(
            "--update", action="store_true", help="Update survey questions"
        )

    def handle(self, *args, **options):
        update_assets = options["update"]

        assets = SURVEY_STRUCTURE
        for asset_params in assets:
            question_id = asset_params.get("question_id")
            qs = SurveyQuestion.objects.filter(question_id=question_id)

            if question_id in SUB_QUESTION_MAPPING:
                asset_params["subquestion_to"] = SurveyQuestion.objects.get(question_id=SUB_QUESTION_MAPPING[question_id])

            display_type = asset_params.pop("display_type", None)
            if display_type == "multiple_choice_tickbox":
                asset_params["multiple_answers"] = True
            if "possible_answers" in asset_params:
                if isinstance(asset_params["possible_answers"], str):
                    asset_params["answer_type"] = asset_params.pop("possible_answers")
                else:
                    asset_params["answer_type"] = TYPE_STRING

            for key in ("possible_answers", "subquestion"):
                key_var = asset_params.get(key)
                if key_var is not None:
                    asset_params[key] = json.dumps(key_var)
            # TODO add the categories here

            if qs.exists() is False:
                print("Create", asset_params)
                new_asset = SurveyQuestion(**asset_params)
                new_asset.save()

            else:
                if update_assets is True:
                    print("Update", qs.get().__dict__)
                    asset = qs.update(**asset_params)
                    print(asset)
                    print("To", asset_params)
