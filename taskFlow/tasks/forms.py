from django import forms
from .models import *

class regsiterLogin(forms.Form):
    username = forms.CharField(label="username", max_length=100, widget=forms.TextInput(attrs={'id': 'login-user','class': 'form-control', 'placeholder': 'Enter your username'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'id': 'login-password', 'class': 'form-control', 'placeholder': 'Enter your password'}), max_length=100)


class TaskForm(forms.ModelForm):
    is_recurring = forms.BooleanField(required=False)
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter task name.'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter task description.'
        })
    )
    type = forms.ChoiceField(
        choices=TaskType.choices,
        required=True,
        initial=TaskType.GENERAL
    )
    urgency = forms.IntegerField( # setting constraints for priority (1-10, inclusive) on the form
        min_value=1,
        max_value=10,
        help_text="On a scale of 1 to 10",
        widget=forms.NumberInput(attrs={
            'type': 'number',
            'min': '1',
            'max': '10',
            'placeholder': 'Enter urgency (1-10), 1 being the highest priority.'
        })
    )
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
        fields = ['name', 'description', 'type', 'urgency', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        is_recurring = cleaned_data.get('is_recurring')
        
        if is_recurring:
            # recurring tasks need these fields
            if not cleaned_data.get('start_date'):
                raise forms.ValidationError("Start date is required for recurring tasks")
            if not cleaned_data.get('end_date'):
                raise forms.ValidationError("End date is required for recurring tasks")
            if not cleaned_data.get('repetition_period'):
                raise forms.ValidationError("Repetition period is required for recurring tasks")
            # due date not required for recurring tasks
            cleaned_data['due_date'] = None
        else:
            # non-recurring tasks need due_date
            if not cleaned_data.get('due_date'):
                raise forms.ValidationError("Due date is required for non-recurring tasks")
        
        return cleaned_data


class calendarChoice(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)


class categoryChoice(forms.Form):
    category = forms.ChoiceField(choices=[('', 'All Tasks')] + list(TaskType.choices), widget=forms.Select(attrs={'class': 'form-select'}), required=False)
