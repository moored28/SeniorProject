from django.urls import path
from . import views

app_name="basic"

urlpatterns = [
    path("compute/<int:value>", views.compute, name="compute"),
    path('homepage/', views.homepage, name="homepage"),
    path("assignments/<task_id>/", views.assignments, name="assignments"),
    path("addNote/<task_id>/", views.addNote, name="addNote")
]