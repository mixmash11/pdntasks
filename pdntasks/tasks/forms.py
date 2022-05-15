from crispy_forms.helper import FormHelper
from django.forms import DateInput, ModelForm

from pdntasks.tasks.models import Task, Goal


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Task
        fields = [
            "name",
            "status",
            "date_due",
            "repeats",
            "assigned_to",
            "project",
            "info",
        ]
        widgets = {"date_due": DateInput(attrs={"type": "date"})}


class GoalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Goal
        fields = ["title", "info", "end_date"]
        widgets = {"end_date": DateInput(attrs={"type": "date"})}
