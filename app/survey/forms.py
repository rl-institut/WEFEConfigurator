from crispy_forms.helper import FormHelper
import json

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from .models import *
from .survey import SURVEY_STRUCTURE, SURVEY_CATEGORIES


class SurveyQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        qs = kwargs.pop("qs", [])
        super().__init__(*args, **kwargs)
        for q in SURVEY_STRUCTURE:
            answer = qs.get(question__question_id=q["question_id"])
            alv = answer.question.possible_answers
            opts = {"label": f"{answer.question.question_id}: {answer.question.question}"}

            # by default the subquestion are not required
            if answer.question.subquestion_to is not None:
                opts["required"] = False

            if alv is not None:
                try:
                    possible_answers = json.loads(alv)
                    list_choices = [(pa, pa.replace("_", " ").capitalize()) for pa in possible_answers]

                    if answer.question.multiple_answers is True:
                        opts["choices"] = list_choices
                        opts["widget"] = forms.CheckboxSelectMultiple
                        self.fields[f"criteria_{answer.question.id}"] = forms.MultipleChoiceField(**opts)
                    else:
                        opts["choices"] = [("", "----------")] + list_choices
                        self.fields[f"criteria_{answer.question.id}"] = forms.ChoiceField(**opts)
                except json.decoder.JSONDecodeError:
                    self.fields[f"criteria_{answer.question.id}"] = forms.FloatField(**opts)
            else:
                self.fields[f"criteria_{answer.question.id}"] = forms.FloatField(**opts)


            # treat sub question differently:
            # - links to onchange of supra question
            # - hide the sub question if the supra question's answer is not "Yes"
            if answer.question.subquestion_to is not None:

                supra_question = SurveyQuestion.objects.get(question_id=answer.question.subquestion_to.question_id)

                # subquestion class
                self.fields[f"criteria_{answer.question.id}"].widget.attrs.update({"class": "sub_question"})

                # subsubquestion class
                if supra_question.subquestion_to is not None:
                    if answer.question.matrix_answers is True:
                        # import pdb;pdb.set_trace()
                        def original_question_number(q_id):
                            answer = q_id
                            for letter in ("a", "b", "c", "d", "e"):
                                if letter in answer:
                                    answer = answer.replace(letter, "")
                            return answer
                        matrix_idxs = original_question_number(answer.question.id).replace(f"{original_question_number(supra_question.id)}.", "")
                        # print(supra_question.id)
                        # print(matrix_idxs)
                        matrix_col_idx, matrix_row_idx = matrix_idxs.split(".")

                        self.fields[f"criteria_{answer.question.id}"].widget.attrs.update({"class": f"sub_question sub_sub_question matrix_target matrix_row_{matrix_row_idx} matrix_col_{matrix_col_idx}"})
                        supra_question_css = self.fields[f"criteria_{supra_question.id}"].widget.attrs["class"]
                        if "matrix_source" not in supra_question_css:
                            self.fields[f"criteria_{supra_question.id}"].widget.attrs["class"] =  f"{supra_question_css} matrix_source"
                    else:
                        self.fields[f"criteria_{answer.question.id}"].widget.attrs.update({"class": "sub_question sub_sub_question"})
                if answer.question.matrix_answers is True:
                    self.fields[f"criteria_{supra_question.id}"].widget.attrs.update(
                        {
                            "onchange": f"triggerMatrixSubQuestion(new_value=this,subQuestionMapping={supra_question.subquestion})"
                        }
                    )
                else:
                    self.fields[f"criteria_{supra_question.id}"].widget.attrs.update(
                        {
                            "onchange": f"triggerSubQuestion(new_value=this,subQuestionMapping={supra_question.subquestion})"
                        }
                    )

                # only provide initial value for subquestion if the answer to supraquestion exists and is valid
                supra_answer = qs.get(question=supra_question)
                if supra_answer.value is not None:
                    if answer.value:
                        if answer.question.multiple_answers is True:
                            self.fields[f"criteria_{answer.question.id}"].initial = json.loads(answer.value.replace("'", '"'))
                        else:
                            self.fields[f"criteria_{answer.question.id}"].initial = answer.value

            else:
                if answer.value:
                    if answer.question.multiple_answers is True:
                        self.fields[f"criteria_{answer.question.id}"].initial = json.loads(answer.value.replace("'", '"'))
                    else:
                        self.fields[f"criteria_{answer.question.id}"].initial = answer.value


    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data:
            for record in cleaned_data:
                if cleaned_data[record] is not None:


                    if cleaned_data[record]:
                        print(record)
                        print(cleaned_data[record])
                        print(type(cleaned_data[record]))
                    else:
                        cleaned_data[record] = None
                    # TODO need to look at the expected type of the question's answer
                else:
                    question = SurveyQuestion.objects.get(question_id=record.replace("criteria_", ""))
                    if question.subquestion_to is None:
                        raise ValidationError("This field cannot be blank")
        else:
            raise ValidationError("This form cannot be blank")
        return cleaned_data
