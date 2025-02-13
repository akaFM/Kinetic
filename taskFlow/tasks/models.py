import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """ inherits from AbstractUser, provided by Django """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # pk - id

class TaskType(models.TextChoices):
    FUN = "Fun"
    WORK = "Work"
    SCHOOL = "School"
    CHORE = "Chore"
    OTHER = "Other"

class RecurringPattern(models.Model):
    class RepetitionPeriod(models.TextChoices):
        DAILY = "Daily"
        WEEKLY = "Weekly"
        MONTHLY = "Monthly"
        YEARLY = "Yearly"
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recurring_patterns")
    description = models.TextField(default="A very important task.")
    type = models.CharField(max_length=20, choices=TaskType.choices, default=TaskType.OTHER)
    urgency = models.IntegerField(default=3)
    repetition_period = models.CharField(max_length=20, choices=RepetitionPeriod.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    """ task model """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    recurring_pattern = models.ForeignKey(RecurringPattern, on_delete=models.CASCADE, null=True, blank=True, related_name="instances")
    
    # Only for non-recurring tasks
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TaskType.choices, null=True, blank=True)
    urgency = models.IntegerField(null=True, blank=True)

    @property
    def get_description(self):
        return self.recurring_pattern.description if self.recurring_pattern else self.description
        
    @property
    def get_type(self):
        return self.recurring_pattern.type if self.recurring_pattern else self.type
        
    @property
    def get_urgency(self):
        return self.recurring_pattern.urgency if self.recurring_pattern else self.urgency
