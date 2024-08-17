from django.urls import path, re_path
from survey.views import *

urlpatterns = [
    path("", view_survey_questions, name="view_survey_questions"),
    path("submit/survey/<int:scen_id>", view_survey_questions, name="submit_survey"),
    path("view/survey/<int:scen_id>", view_survey_questions, name="view_survey"),
]
