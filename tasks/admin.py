from django.contrib import admin

#Import all our custom models
from .models import *

# Registering models here allows them to show up in Django's admin interface

admin.site.register(Member)
admin.site.register(Crew)
admin.site.register(Task)
admin.site.register(Equipment)
admin.site.register(Note)
