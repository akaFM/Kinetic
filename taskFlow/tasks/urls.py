from django.urls import path

from . import views

urlpatterns = [
     path("", views.index, name="index"),
     path("login", views.login, name="login"),
     path("logout", views.logout, name="logout"),
     path("create-task", views.create_task, name="create_task")
 ]