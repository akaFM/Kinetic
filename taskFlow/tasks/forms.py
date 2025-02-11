from django import forms
from .models import Task
from calendar import month_name

class regsiterLogin(forms.Form):
    username = forms.CharField(label="username", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}), max_length=100)


class TaskForm(forms.ModelForm): # used to create a new task
    class Meta:
        model = Task
        fields = ['description', 'type', 'urgency', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }


class calendarChoice(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)


class categoryChoice(forms.Form):
    category = forms.ChoiceField(choices=[('', 'All Tasks')] + list(Task.TaskType.choices), widget=forms.Select(attrs={'class': 'form-select'}), required=False)
