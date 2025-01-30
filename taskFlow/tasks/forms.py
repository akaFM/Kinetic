from django import forms
from .models import Task

class regsiterLogin(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), max_length=100)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'type', 'urgency', 'due_date']
