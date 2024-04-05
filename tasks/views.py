from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        register_form = RegisterForm()
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('basic:homepage')
            else:
                login_form.add_error(None, "Invalid username or password")
    else:
        login_form = LoginForm()
        register_form = RegisterForm()
    return render(request, 'tasks/login.html', {'login_form': login_form, 'register_form': register_form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.set_password(form.cleaned_data['password'])
            member.save()
            login(request, member)
            return redirect('basic:homepage')
    else:
        form = RegisterForm()
    return render(request, 'tasks/login.html', {'register_form': form, 'login_form': LoginForm()})

    

@login_required
def display_equipment(request):
    ordering = request.GET.get('order_by', 'name')  # Default ordering by name
    if ordering == 'status':
        equipment = Equipment.objects.all().order_by('status')
    elif ordering == 'crew':
        equipment = Equipment.objects.all().order_by('assignedTo')
    else:
        equipment = Equipment.objects.all().order_by('name')
    
    return render(request, 'tasks/equipment.html', {'equipment': equipment})

@login_required
def add_equipment(request):
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:equipment')
    else:
        form = AddEquipmentForm()
    return render(request, 'tasks/add_equipment.html', {'form': form})

@login_required
def delete_equipment(request, equipment_id):
    # Retrieve the pet for the provided pet_id and delete it
    equipment = Equipment.objects.get(id=equipment_id)
    equipment.delete()
    # Head back to equipment page
    return redirect('tasks:equipment')

@login_required
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