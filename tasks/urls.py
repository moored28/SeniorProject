from django.urls import path
from . import views

app_name="tasks"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path("equipment/", views.display_equipment, name="equipment"),
    path("add_equipment/", views.add_equipment, name="add_equipment"),
    path("edit_equipment/<int:equipment_id>", views.edit_equipment, name="edit_equipment"),
    path("delete_equipment/<int:equipment_id>", views.delete_equipment, name="delete_equipment"),
]