from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
     path("", views.index, name="index"),
     path("login", views.login, name="login"),
     path("logout", views.logout, name="logout"),
     path("create-task", views.create_task, name="create_task"),
     path('tasks/<int:year>/<int:month>/<int:day>/', views.get_day_tasks_description_json, name='get_day_tasks_description_json'),
     path('tasks/complete/', views.complete_task, name='complete_task'),
     path('tasks/uncomplete/', views.uncomplete_task, name='uncomplete_task'),
     path("edit-tasks", views.edit_tasks, name="edit_tasks"),
     path("music-playlist", views.music_playlist, name="music_playlist"),
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)