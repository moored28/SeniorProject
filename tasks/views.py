from django.shortcuts import render
from .models import *

# Create your views here.

def display_equipment(request):
    ordering = request.GET.get('order_by', 'name')  # Default ordering by name
    if ordering == 'status':
        equipment = Equipment.objects.all().order_by('status')
    elif ordering == 'crew':
        equipment = Equipment.objects.all().order_by('assignedTo')
    else:
        equipment = Equipment.objects.all().order_by('name')
    
    return render(request, 'tasks/equipment.html', {'equipment': equipment})
