from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(TaskType)
admin.site.register(RecurringPattern)
admin.site.register(Task)