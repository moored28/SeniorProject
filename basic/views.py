from django.shortcuts import render, redirect
from django.http import Http404
from .models import *
from django.views.decorators.http import require_GET, require_POST
from tasks.models import *
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from tasks.models import Task, Equipment, Note, Member
from django.http import JsonResponse
from django.db.models import Q
from django.apps import apps
from tasks.forms import *
#import googlemaps
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string

from pathlib import Path
import os


# Create your views here.

# Computation function

@login_required
def homepage(request):
    crew = Crew.objects.all()
    task = Task.objects.all()
    equipment = Equipment.objects.all()
    notes = Note.objects.all()

    bind = zip(task, equipment, notes)
    context= {
        'bind': bind
    }
   
    return render(request, 'basic/homepage.html', {
        'crew': crew, 
        'task' : task, 
        'context' : context
    })

"""Task Page"""
@login_required
def assignments(request, task_id):
    equipment = Equipment.objects.all()
    notes = Note.objects.all()

    try:
        task = Task.objects.get(id = task_id)
    except Task.DoesNotExist:
        raise Http404('not found. error ms')
    
    return render(request, 'basic/assignments.html', {
        'task': task,
        'equipment' : equipment,
        'notes' : notes,
        })

@login_required
def addNote(request, task_id):
    task = Task.objects.get(id = task_id)
    me = request.user.get_username()
    
    if request.method == 'POST':
        form = AddNotes(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            member = Member.objects.get(username = me)
            dateCreated = timezone.now()
            note = Note(
                text=text,
                createdBy=member,
                #picture=picture,
                dateCreated=dateCreated,
                task=task
            )
            note.save()
            return redirect('basic:assignments', task_id)
    else:
        form = AddNotes()
    return render(request, "basic/addNote.html", {
        'form': form,
        'task': task
        })
    

"""Temp Button to send Routes"""
@login_required
def routeButton(request):
    return render(request, 'basic/routeButton.html')

def search(request):
    query = request.GET.get('q')
    if query:
          # Perform search query on your Django models
        task_results = Task.objects.filter(
            Q(name__icontains=query) |
            Q(id__in=Note.objects.filter(text__icontains=query).values('task_id'))
        ).distinct()[:10]
        
        # Serialize the results into JSON format
        serialized_results = [{'name': task.name} for task in task_results]
        return JsonResponse(serialized_results, safe=False)
    else:
        return JsonResponse([], safe=False)
    

"""Creates a Task"""
@login_required
def createTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('basic:homepage') 
    else:
        form = TaskForm()
    
    return render(request, 'basic/createTask.html', {'form': form})

# Handling of Google Maps
def generate_route_for_crew(crew):
    # Initialize Google Maps client
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    # Fetch tasks for the crew
    tasks = Task.objects.filter(crew=crew)[:5]  # Fetch first 5 tasks

    if len(tasks) == 0:  # If no tasks found, return empty route
        return []

    # Extract task locations
    task_locations = [task.location for task in tasks]

    # Assuming crew members start from the location of the first task
    start_location = task_locations[0]

    # Concatenate task locations
    all_locations = task_locations

    # Generate route
    directions = gmaps.directions(
        origin=start_location,
        destination=all_locations[-1],
        waypoints=all_locations[1:-1],
        optimize_waypoints=True
    )

    return directions

def send_routes():
    # Fetch crews
    crews = Crew.objects.filter(crewName='Dylan Crew')  #To test this crew since has real data

    # Loop through each crew
    for crew in crews:
        # Get members of the crew
        members = crew.members.all()

        # Loop through each member
        for member in members:
            # Generate route for the crew using Google Maps API
            route = generate_route_for_crew(crew.crewName)

            # Render email content with the route
            email_content = render_to_string('email_template.html', {'route': route})

            # Send email to member
            send_mail(
                'Your Daily Route',
                email_content,
                'moored28@students.rowan.edu',  
                [member.email],  # Send to member's email
                fail_silently=False,
            )

    return HttpResponse('Routes sent successfully')


def execute_send_routes(request):
    # Call the send_routes function
    send_routes()
    # Redirect back to the original page
    return redirect('basic:homepage')

def search_results(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            # Perform search query on the Crew model
            crew_results = Crew.objects.filter(crewName__icontains=query)
 
            # Perform search query on the Task model
            task_results = Task.objects.filter(name__icontains=query)
            return render(request, 'basic/search_results.html', {'query': query, 'crew_results': crew_results, 'task_results': task_results})
        
    return render(request, 'basic/search_results.html', {})


