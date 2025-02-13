from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import django.contrib.auth
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from datetime import date, datetime, timedelta
from calendar import monthrange

# https://stackoverflow.com/questions/17873855/manager-isnt-available-user-has-been-swapped-for-pet-person
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required()
def index(request):
    today = None
    realToday = date.today()

    if request.method == "POST":
        today = datetime.strptime(request.POST["date"], "%Y-%m-%d").date()

    if not today:
        today = realToday # if user and server are in a unqiue timezone, we get a OBO for displayed month and possibly year
    
    startDate = today.replace(day=1)
    endDate = startDate.replace(day=monthrange(startDate.year, startDate.month)[1])

    tasksToShow = Task.objects.filter(due_date__range=(startDate, endDate), user=request.user)
    taskList = [[] for _ in range(monthrange(startDate.year, startDate.month)[1])]
    
    for task in tasksToShow:
        taskList[task.due_date.day - 1].append(task)
    
    return render(request, "tasks/dashboard.html", {
        "taskList": taskList,
        "month": today.month,
        "year": today.year,
        "currDay": realToday.day if startDate.month == realToday.month and startDate.year == realToday.year else -1, 
        "form": calendarChoice(),
    })


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist: # register a new user
            # since passsword reqs can change over time
            # only new users get their password validated
            # otherwise we will lock people out of their accounts
            lengthOfPassword = 0
            hasUpper = False
            hasLower = False
            hasNumber = False
            hasSpecial = False
            for char in password:
                lengthOfPassword += 1
                if char.isupper():
                    hasUpper = True
                elif char.islower():
                    hasLower = True
                elif char.isdigit():
                    hasNumber = True
                else:
                    hasSpecial = True

            if not (lengthOfPassword >= 6 and lengthOfPassword <= 20 and hasUpper and hasLower and hasNumber and hasSpecial):
                return render(request, "tasks/login.html", {
                    "form": regsiterLogin(initial={"username": username}),
                    "msg": "Password must be 6-20 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character."
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

    return render(request, "tasks/login.html", {
        "form": regsiterLogin(),
        "msg": "Enter your login credentials. If you don't have an account, one will be created automatically."
    })

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required()
def create_task(request):
    
    # POST req (data being submitted to create_task route)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():

            is_recurring = form.cleaned_data['is_recurring']
            
            if is_recurring:

                # only in this case do we create a recurring pattern object
                # otherwise, the task is one-time, so there isnt a point
                pattern = RecurringPattern.objects.create(
                    user=request.user,
                    description=form.cleaned_data['description'],
                    type=form.cleaned_data['type'],
                    urgency=form.cleaned_data['urgency'],
                    repetition_period=form.cleaned_data['repetition_period'],
                    start_date=form.cleaned_data['start_date'],
                    end_date=form.cleaned_data['end_date']
                )

                # TODO: somewhere in this route, implement a backend check to limit the end date- 
                # the user shouldnt be able to make the end date more than 5 years away or something like that
                
                # now, we create a different task object until the end date
                # for now im using a less efficient data design, but will refine this soon to avoid
                # redundant rows
                current_date = pattern.start_date
                while current_date <= pattern.end_date: # this will keep tasks from being created past the end date
                    
                    # as of right now, the task object has a bunch of repetitive info that repeatedly
                    # gets entered into the table, but this will be fixed with a M:1 relationship with the
                    # recurring pattern object
                    Task.objects.create(
                        user=request.user,
                        description=pattern.description,
                        type=pattern.type,
                        urgency=pattern.urgency,
                        due_date=current_date,
                        recurring_pattern=pattern
                    )
                    
                    # calculate next date based on repetition period
                    if pattern.repetition_period == RecurringPattern.RepetitionPeriod.DAILY:
                        current_date += timedelta(days=1)
                    elif pattern.repetition_period == RecurringPattern.RepetitionPeriod.WEEKLY:
                        current_date += timedelta(weeks=1)
                    elif pattern.repetition_period == RecurringPattern.RepetitionPeriod.MONTHLY:
                        # add month
                        if current_date.month == 12:
                            current_date = current_date.replace(year=current_date.year + 1, month=1)
                        else:
                            current_date = current_date.replace(month=current_date.month + 1)
                    else:  # yearly 
                        current_date = current_date.replace(year=current_date.year + 1)
            else:
                #  task is nonrepetitious- just create the object
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                
            return HttpResponseRedirect(reverse("index"))
    else:

        # defining the form
        form = TaskForm()
        # GET req (form being rendered)
        
    return render(request, "tasks/create_task.html", {
        "form": form
    })