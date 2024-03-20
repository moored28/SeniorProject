from django.shortcuts import render
from .models import *

# Create your views here.


def display_equipment(request):
    equipment = Equipment.objects.all()
    return render(request, 'tasks/equipment.html', {'equipment': equipment})