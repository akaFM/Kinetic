import django
import random
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from datetime import date, datetime, timedelta
from calendar import monthrange
from django.http import JsonResponse
import json


import random
from django.shortcuts import render



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


def filter_tasks_by_category(tasks, category, year, month, day):
    if category and category in TaskType.values:
        filtered_tasks = tasks.filter(type=category)
        recurring_tasks = Task.objects.filter(recurring_pattern__in=RecurringPattern.objects.filter(type=category), due_date__year=year, due_date__month=month, due_date__day=day)
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
            name=pattern.name,
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
def get_day_tasks_description_json(request, year, month, day):
    category = request.GET.get("category")
    tasks_queryset = Task.objects.filter(user=request.user, due_date__year=year, due_date__month=month, due_date__day=day)
    tasks_queryset = filter_tasks_by_category(tasks_queryset, category, year, month, day)

    tasks = [{
        "id": t.id,
        "name": t.name,
        "description": t.get_description,
        "type": t.get_type,
        "urgency": t.get_urgency,
        "completed": t.completed
    } for t in tasks_queryset]
    
    return JsonResponse({"tasks": tasks})


@login_required()
# def index(request):
#     today = get_today(request)
    
#     context = {
#         "category": "All Tasks",
#         "month": today.month,
#         "year": today.year,
#         "currDay": date.today().day if (today.year, today.month) == (date.today().year, date.today().month) else -1,
#         "calendarForm": calendarChoice(),
#         "categoryForm": categoryChoice(),
#         "TaskType": TaskType,
#     }
#     return render(request, "tasks/dashboard.html", context)


def index(request):
    today = get_today(request)
    
    # Add the quote logic here
    quotes = [
        "Believe you can and you're halfway there.",
        "Your limitation—it's only your imagination.",
        "Push yourself, because no one else is going to do it for you.",
        "Sometimes later becomes never. Do it now.",
        "Dream it. Wish it. Do it.",
        "Great things never come from comfort zones.",
        "Don't stop when you're tired. Stop when you're done."
    ]

    random_quote = random.choice(quotes)

    context = {
        "category": "All Tasks",
        "month": today.month,
        "year": today.year,
        "currDay": date.today().day if (today.year, today.month) == (date.today().year, date.today().month) else -1,
        "calendarForm": calendarChoice(),
        "categoryForm": categoryChoice(),
        "TaskType": TaskType,
        "quote": random_quote,  # Pass the random quote to the template
    }

    return render(request, "tasks/dashboard.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            if not validate_password(password):  # never validate a password for a user that exists, we will lock people out
                context = {
                    "form": regsiterLogin(initial={"username": username}),
                    "msg": ("Password must be 6-20 characters long and contain at least one uppercase letter, "
                            "one lowercase letter, one number, and one special character.")
                }
                return render(request, "tasks/login.html", context)
            user = User.objects.create_user(username=username, password=password)
            user.save()

        if not check_password(password, user.password):
            context = {
                "form": regsiterLogin(initial={"username": username}),
                "msg": "Incorrect password. Please try again."
            }
            return render(request, "tasks/login.html", context)

        django.contrib.auth.login(request, user)
        return HttpResponseRedirect(reverse("index"))

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    context = {
        "form": regsiterLogin(),
        "msg": "Enter your login credentials. If you don't have an account, one will be created automatically."
    }
    return render(request, "tasks/login.html", context)

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
                    name=form.cleaned_data["name"],
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
                    name=form.cleaned_data["name"],
                    description=form.cleaned_data["description"],
                    type=form.cleaned_data["type"],
                    urgency=form.cleaned_data["urgency"],
                    due_date=form.cleaned_data["due_date"],
                )
            return HttpResponseRedirect(reverse("index"))
    else:
        form = TaskForm()
        
    context = {"form": form}
    return render(request, "tasks/create_task.html", context)
    
@login_required
def complete_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('task_id')
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.completed = True
            task.save()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
    
@login_required
def uncomplete_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('task_id')
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.completed = False
            task.save()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@login_required()
def edit_tasks(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        is_recurring = request.POST.get("is_recurring") == "true"
        toDelete = request.POST.get("action") == "true"
        
        try:
            if is_recurring:
                pattern = RecurringPattern.objects.get(id=task_id, user=request.user)
                if toDelete:
                    Task.objects.filter(recurring_pattern=pattern).delete()
                    pattern.delete()
                else:
                    pattern.name = request.POST.get("name", pattern.name)
                    pattern.description = request.POST.get("description", pattern.description)
                    pattern.type = request.POST.get("type", pattern.type)
                    pattern.urgency = request.POST.get("urgency", pattern.urgency)
                    pattern.save()
                    
                    Task.objects.filter(recurring_pattern=pattern).update(name=pattern.name, description=pattern.description, type=pattern.type, urgency=pattern.urgency)
            else:
                task = Task.objects.get(id=task_id, user=request.user)
                if toDelete:
                    task.delete()
                else:
                    task.name = request.POST.get("name", task.name)
                    task.description = request.POST.get("description", task.description)
                    task.type = request.POST.get("type", task.type)
                    task.urgency = request.POST.get("urgency", task.urgency)
                    task.due_date = datetime.strptime(request.POST.get("due_date", task.due_date.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
                    task.save()
            
            return HttpResponseRedirect(reverse("edit_tasks"))
            
        except (Task.DoesNotExist, RecurringPattern.DoesNotExist):
            pass
    
    one_time_tasks = Task.objects.filter(user=request.user, recurring_pattern__isnull=True).order_by('due_date')
    recurring_patterns = RecurringPattern.objects.filter(user=request.user).order_by('start_date')
    
    context = {
        "one_time_tasks": one_time_tasks,
        "recurring_patterns": recurring_patterns,
        "TaskType": TaskType,
    }
    return render(request, "tasks/edit_tasks.html", context)