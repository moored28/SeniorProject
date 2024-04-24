from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.decorators.http import require_GET, require_POST


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

# Check if the user is a manager - Utilized to only allow Managers to create and edit information
def is_manager(user):
    return user.member.position == 'Manager'

@login_required
def profile(request):
    member = request.user.member
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            if 'profileImage' in request.FILES:
                member.profileImage.delete()
                member.profileImage.save('profile_image.jpg', request.FILES['profileImage'])
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('tasks:profile')
    else:
        form = MemberForm(instance=member)
    return render(request, 'tasks/profile.html', {'member': member, 'form': form, 'image': str(member.profileImage)})

@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Stops user from having to relog
            messages.success(request, 'Your password was successfully updated!')
            return redirect('tasks:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_form = PasswordChangeForm(request.user)
    return render(request, 'tasks/change_password.html', {'password_form': password_form})

def logout_view(request):
    logout(request)
    return redirect('tasks:login')


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
@user_passes_test(is_manager)
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
@user_passes_test(is_manager)
def delete_equipment(request, equipment_id):
    # Retrieve the pet for the provided pet_id and delete it
    equipment = Equipment.objects.get(id=equipment_id)
    equipment.delete()
    # Head back to equipment page
    return redirect('tasks:equipment')
  
@login_required
@user_passes_test(is_manager)
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


# <<<<<<<<<Crew Page>>>>>>>>>>>

@require_GET
def crews(request):
    crew = Crew.objects.all()
    member = Member.objects.all()

    return render(request, 'tasks/crews.html', {
        'crews': crew,
        'members': member,
    })

@require_POST
def crewmembers(request, id):
    crew = Crew.objects.get(id=id)
    return render(request, "tasks/members_partial.html", {
        'crew': crew,
    })


@login_required
@user_passes_test(is_manager)
def add_crew(request):
    if request.method == 'POST':
        form = AddCrewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:crews')
    else:
        form = AddCrewForm()
    return render(request, 'tasks/add_crew.html', {'form': form})

@login_required   
@user_passes_test(is_manager)
def edit_crewmember(request):
    if request.method == 'POST':
        form = EditCrewMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:crews')
        else:
            # Form is not valid, handle errors
            return render(request, 'tasks/edit_crewmembers.html', {'form': form,})
    else:
        form = EditCrewMemberForm()
    return render(request, 'tasks/edit_crewmembers.html', {'form': form,})

@login_required
@user_passes_test(is_manager)
def remove_crewmember(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        crew_id = request.POST.get('crew_id')
        member = Member.objects.get(id=member_id)
        crew = Crew.objects.get(id=crew_id)
        crew.members.remove(member)
    return redirect(request.META.get('HTTP_REFERER', 'tasks:members_partial'))

#   <<<<<<<<<<< End Crew Page >>>>>>>>>>>>>
