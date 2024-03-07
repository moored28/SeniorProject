from django.urls import path

from . import views

app_name="htmx"

urlpatterns = [

    # Demo page with Tailwind CSS
    path("demo", views.demo, name="demo"),

    # Partials URLS
    path('oneimage/', views.oneimage, name='oneimage'),
    path("answer", views.answer, name="answer"),
    path("answer1", views.answer1, name="answer1"),

    # URLs for Boostrap CSS + navbar demo
    path("demob", views.demo_bootstrap, name="demob"),
    path('example1/', views.example1, name='example1'),
    path('example2/', views.example2, name='example2'),
    path('example3/', views.example3, name='example3'),

    
]