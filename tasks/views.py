from django.shortcuts import redirect, render
from .models import *
from .forms import *

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


#Crew Page
def crews(request):
    crew = Crew.objects.all()
    member = Member.objects.all()

    return render(request, 'tasks/crews.html', {
        'crew': crew,
        'member': member,
    })

def add_crew(request):
    if request.method == 'POST':
        form = AddCrewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:crew')
    else:
        form = AddCrewForm()
    return render(request, 'tasks/add_crew.html', {'form': form})

def edit_crewmember(request):
    if request.method == 'POST':
        form = EditCrewMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:crew')
    else:
        form = EditCrewMemberForm()
    return render(request, 'tasks/edit_crewmembers.html', {'form': form})

# @require_GET
# def load_members(request):
#     crew_name = request.GET.get('crew_name')
#     if crew_name:
#         crew = Crew.objects.get(crewName=crew_name)
#         members = crew.members.all()
#     else:
#         members = None
#     return render(request, 'basic/members_partial.html', {'members': members})


#End Crew Page