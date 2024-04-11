from django.urls import path
from . import views

app_name="basic"

urlpatterns = [
    path('homepage/', views.homepage, name="homepage"),
    path("assignments/<task_id>/", views.assignments, name="assignments"),
    path("addNote/<task_id>/", views.addNote, name="addNote"),
    path("routeButton/", views.routeButton, name="routeButton"),
    path('createTask/', views.createTask, name='createTask')
]