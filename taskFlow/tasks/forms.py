from django import forms
from .models import Task

class regsiterLogin(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), max_length=100)


class TaskForm(forms.ModelForm): # used to create a new task
    class Meta:
        model = Task
        fields = ['description', 'type', 'urgency', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

class calendarChoice(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

