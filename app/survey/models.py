import json
from django.db import models
from .survey import SURVEY_QUESTIONS_CATEGORIES


class SurveyQuestion(models.Model):
    question_id = models.CharField(null=False, max_length=30, primary_key=True)
    question = models.TextField(null=False)
    subquestion_to = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
    subquestion = models.TextField(null=True)
    possible_answers = models.TextField(null=True)
    multiple_answers = models.BooleanField(default=False)  # this is a parameter for checkbox questions
    matrix_answers = models.BooleanField(default=False)
    answer_type = models.CharField(null=False, max_length=8)
    description = models.TextField(null=False, default="")
    category = models.CharField(
        max_length=60,
        null=True,
        blank=False,
        choices=[(k, v) for k, v in SURVEY_QUESTIONS_CATEGORIES.items()],
    )

    @property
    def id(self):
        return self.question_id

    @property
    def subquestions(self):
        if self.subquestion is not None:
            answer = json.loads(self.subquestion)
        else:
            answer = self.subquestion
        return answer



class SurveyAnswer(models.Model):
    question = models.ForeignKey(
        SurveyQuestion, on_delete=models.CASCADE, null=True, blank=False
    )
    value = models.TextField(null=True)
    #TODO make this a ForeignKey
    scenario_id = models.IntegerField(null=False)

