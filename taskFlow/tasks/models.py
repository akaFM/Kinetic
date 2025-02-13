import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """ inherits from AbstractUser, provided by Django """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # pk - id

class Task(models.Model):
    """ task model """
    class TaskType(models.TextChoices):
        FUN = "Fun"
        WORK = "Work"
        SCHOOL = "School"
        CHORE = "Chore"
        OTHER = "Other"

    class RepetitionPeriod(models.TextChoices):
        DAILY = "Daily"
        WEEKLY = "Weekly"
        MONTHLY = "Monthly"
        YEARLY = "Yearly"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # pk - id
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")  # fk - user
    description = models.TextField(default="A very important task.") 
    type = models.CharField(max_length=20, choices=TaskType.choices, default=TaskType.OTHER) # default - OTHER (filterable)
    urgency = models.IntegerField(default=3)  # 1 (most urgent) to 5 (least urgent) (filterable)
    due_date = models.DateField() # filterable
    created_at = models.DateTimeField(auto_now_add=True) # filterable
    completed = models.BooleanField(default=False) # filterable
    
    # Recurring task fields
    is_recurring = models.BooleanField(default=False)
    repetition_period = models.CharField(
        max_length=20,
        choices=RepetitionPeriod.choices,
        null=True,
        blank=True
    )
    start_interval = models.DateField(null=True, blank=True)
    end_interval = models.DateField(null=True, blank=True)
