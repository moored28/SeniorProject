from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name="tasks"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path("equipment/", views.display_equipment, name="equipment"),
    path("add_equipment/", views.add_equipment, name="add_equipment"),
    path("edit_equipment/<int:equipment_id>/", views.edit_equipment, name="edit_equipment"),
    path("delete_equipment/<int:equipment_id>/", views.delete_equipment, name="delete_equipment"),
    path('crews/', views.crews, name="crews"),
    path("add_crew/", views.add_crew, name="add_crew"),
    path("edit_crewmembers/", views.edit_crewmember, name="edit_crewmembers")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)