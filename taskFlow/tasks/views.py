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

# https://stackoverflow.com/questions/17873855/manager-isnt-available-user-has-been-swapped-for-pet-person
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required()
def index(request):
    return render(request, "tasks/dashboard.html", {})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist: # register a new user
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
        "msg": "Enter your login credentials. If you don’t have an account, one will be created automatically."
    })

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse("index"))