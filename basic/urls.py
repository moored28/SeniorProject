from django.urls import path
from . import views

app_name="basic"

urlpatterns = [
    path("compute/<int:value>", views.compute, name="compute"),
    path('homepage/', views.homepage, name="homepage"),
    path('crews/', views.crews, name="crews"),
    path('profile/', views.profile, name="profile")
]
