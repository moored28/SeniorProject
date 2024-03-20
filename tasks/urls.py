from django.urls import path
from . import views

app_name="tasks"

urlpatterns = [
    path("equipment/", views.display_equipment, name="equipment"),
]