import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class TaskType(models.TextChoices):
    GENERAL = "General"
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
    name = models.CharField(max_length=200, default="Untitled Recurring Task")
    description = models.TextField(default="")
    type = models.CharField(max_length=20, choices=TaskType.choices, default=TaskType.OTHER)
    urgency = models.IntegerField(default=3)
    repetition_period = models.CharField(max_length=20, choices=RepetitionPeriod.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=200, default="Untitled Task")
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    recurring_pattern = models.ForeignKey(RecurringPattern, on_delete=models.CASCADE, null=True, blank=True, related_name="instances")
    
    # only for non-recurring tasks
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TaskType.choices, null=True, blank=True, default=TaskType.GENERAL)
    urgency = models.IntegerField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Task urgency on a scale of 1 to 10"
    )
    @property
    def get_description(self):
        return self.recurring_pattern.description if self.recurring_pattern else self.description
        
    @property
    def get_type(self):
        return self.recurring_pattern.type if self.recurring_pattern else self.type
        
    @property
    def get_urgency(self):
        return self.recurring_pattern.urgency if self.recurring_pattern else self.urgency


class Note(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="note")
    content = models.TextField(blank=True)

    def __str__(self):
        return f"Note for {self.user.username}"