import django
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from datetime import date, datetime, timedelta
from calendar import monthrange

from .models import *
from .forms import *

# https://stackoverflow.com/questions/17873855/manager-isnt-available-user-has-been-swapped-for-pet-person
User = get_user_model()

def get_today(request):
    date_str = request.POST.get("date")
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            pass
    return date.today()


def filter_tasks_by_category(tasks, category):
    if category and category in TaskType.values:
        filtered_tasks = tasks.filter(type=category)
        recurring_tasks = Task.objects.filter(recurring_pattern__in=RecurringPattern.objects.filter(type=category))
        return filtered_tasks | recurring_tasks
    return tasks


def group_tasks_by_day(tasks, year, month):
    num_days = monthrange(year, month)[1]
    task_list = [[] for _ in range(num_days)]
    for task in tasks:
        task_list[task.due_date.day - 1].append(task)
    return task_list


def validate_password(password):
    if not 6 <= len(password) <= 20:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_number = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    return has_upper and has_lower and has_number and has_special


def create_recurring_tasks(user, pattern):
    current_date = pattern.start_date
    while current_date <= pattern.end_date:
        Task.objects.create(
            user=user,
            due_date=current_date,
            recurring_pattern=pattern,
        )
        current_date = get_next_date(current_date, pattern.repetition_period)


def get_next_date(current_date, repetition_period):
    if repetition_period == RecurringPattern.RepetitionPeriod.DAILY:
        return current_date + timedelta(days=1)
    elif repetition_period == RecurringPattern.RepetitionPeriod.WEEKLY:
        return current_date + timedelta(weeks=1)
    elif repetition_period == RecurringPattern.RepetitionPeriod.MONTHLY:
        if current_date.month == 12:
            return current_date.replace(year=current_date.year + 1, month=1)
        return current_date.replace(month=current_date.month + 1)
    elif repetition_period == RecurringPattern.RepetitionPeriod.YEARLY:
        return current_date.replace(year=current_date.year + 1)
    return current_date


@login_required()
def index(request):
    category = request.POST.get("category")
    today = get_today(request)
    start_date = today.replace(day=1)
    end_date = today.replace(day=monthrange(today.year, today.month)[1])

    tasks = Task.objects.filter(due_date__range=(start_date, end_date), user=request.user)
    tasks = filter_tasks_by_category(tasks, category)
    task_list = group_tasks_by_day(tasks, today.year, today.month)

    context = {
        "taskList": task_list,
        "category": category if category and category in TaskType.values else "All Tasks",
        "month": today.month,
        "year": today.year,
        "currDay": date.today().day if (today.year, today.month) == (date.today().year, date.today().month) else -1,
        "calendarForm": calendarChoice(),
        "categoryForm": categoryChoice(),
    }
    return render(request, "tasks/dashboard.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            if not validate_password(password): # never validate a password for a user that exists, we will lock people out
                return render(request, "tasks/login.html", {
                    "form": regsiterLogin(initial={"username": username}),
                    "msg": ("Password must be 6-20 characters long and contain at least one uppercase letter, "
                            "one lowercase letter, one number, and one special character.")
                })
            user = User.objects.create_user(username=username, password=password)
            user.save()

        if not check_password(password, user.password):
            return render(request, "tasks/login.html", {
                "form": regsiterLogin(initial={"username": username}),
                "msg": "Incorrect password. Please try again."
            })

        django.contrib.auth.login(request, user)
        return HttpResponseRedirect(reverse("index"))

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "tasks/login.html", {
        "form": regsiterLogin(),
        "msg": "Enter your login credentials. If you don't have an account, one will be created automatically."
    })

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required()
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get("is_recurring"):
                start_date = form.cleaned_data["start_date"]
                end_date = min(form.cleaned_data["end_date"], start_date + timedelta(days=5 * 365)) # cap recurring tasks at 5 years
                pattern = RecurringPattern.objects.create(
                    user=request.user,
                    description=form.cleaned_data["description"],
                    type=form.cleaned_data["type"],
                    urgency=form.cleaned_data["urgency"],
                    repetition_period=form.cleaned_data["repetition_period"],
                    start_date=start_date,
                    end_date=end_date,
                )
                create_recurring_tasks(request.user, pattern)
            else:
                Task.objects.create(
                    user=request.user,
                    description=form.cleaned_data["description"],
                    type=form.cleaned_data["type"],
                    urgency=form.cleaned_data["urgency"],
                    due_date=form.cleaned_data["due_date"],
                )
            return HttpResponseRedirect(reverse("index"))
    else:
        form = TaskForm()

    return render(request, "tasks/create_task.html", {"form": form})