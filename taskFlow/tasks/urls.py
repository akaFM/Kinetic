from django.urls import path

from . import views

urlpatterns = [
     path("", views.index, name="index"),
     path("login", views.login, name="login"),
     path("logout", views.logout, name="logout"),
     path("create-task", views.create_task, name="create_task"),
     path('tasks/<int:year>/<int:month>/<int:day>/', views.get_day_tasks_description_json, name='get_day_tasks_description_json'),
     path('tasks/complete/', views.complete_task, name='complete_task'),
 ]