from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, redirect
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


def add_equipment(request):
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:equipment')
    else:
        form = AddEquipmentForm()
    return render(request, 'tasks/add_equipment.html', {'form': form})

def delete_equipment(request, equipment_id):
    # Retrieve the pet for the provided pet_id and delete it
    equipment = Equipment.objects.get(id=equipment_id)
    equipment.delete()
    # Head back to equipment page
    return redirect('tasks:equipment')

def edit_equipment(request, equipment_id):
    equipment = Equipment.objects.get(id=equipment_id)
    if request.method == 'POST':
        form = EditEquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('tasks:equipment')
    else:
        form = EditEquipmentForm(instance=equipment)
    return render(request, 'tasks/edit_equipment.html', {'form': form, 'equipment': equipment})