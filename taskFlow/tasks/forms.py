from django import forms
from .models import Task, RecurringPattern

class regsiterLogin(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), max_length=100)


class TaskForm(forms.ModelForm): # used to create a new task
    is_recurring = forms.BooleanField(required=False)
    repetition_period = forms.ChoiceField(
        choices=RecurringPattern.RepetitionPeriod.choices,
        required=False
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Task
        fields = ['description', 'type', 'urgency', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }  

class calendarChoice(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

