from django.urls import path
from . import views

app_name="basic"

urlpatterns = [
    path('homepage/', views.homepage, name="homepage"),
    path("assignments/<task_id>/", views.assignments, name="assignments"),
    path("addNote/<task_id>/", views.addNote, name="addNote"),
    path("routeButton/", views.routeButton, name="routeButton"),
    path('createTask/', views.createTask, name='createTask'),
    path('execute_send_routes', views.execute_send_routes, name='execute_send_routes'),
    path('search_results/', views.search_results, name="search_results"),
    path('completeTask/<task_id>/', views.completeTask, name="completeTask"),
    path('assign_task/<int:task_id>/', views.assign_task, name='assign_task'),
    path('get_assigned_crew/<int:task_id>/', views.get_assigned_crew, name='get_assigned_crew'),
    path('get_crew_options/', views.get_crew_options, name='get_crew_options'),
]