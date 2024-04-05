from django.urls import path
from . import views

app_name="tasks"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path("equipment/", views.display_equipment, name="equipment"),
    path('crews/', views.crews, name="crews"),
    path("add_crew/", views.add_crew, name="add_crew"),
    path("edit_crewmembers/", views.edit_crewmember, name="edit_crewmembers")
]