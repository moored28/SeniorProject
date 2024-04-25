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
import googlemaps
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
import urllib.parse
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from pathlib import Path
import os
from django.shortcuts import redirect, get_object_or_404


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
    crews = Crew.objects.all()

    try:
        task = Task.objects.get(id = task_id)
    except Task.DoesNotExist:
        raise Http404('not found. error ms')
    
    return render(request, 'basic/assignments.html', {
        'task': task,
        'equipment' : equipment,
        'notes' : notes,
        'crews' : crews,
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

def completeTask(request, task_id):
    task = Task.objects.get(id=task_id)
    # Assuming task has a foreign key to Crew and current user belongs to the crew
    if request.user in task.assignedTo.members.all() or request.user.member.position == 'Manager':
        task.status = 2
        task.dateComplete = timezone.now()
        task.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'User must be a crew member or manager to complete the task'})


def assign_task(request, task_id):
    if request.method == 'POST':
        crew_name = request.POST.get('crew_name')
        print("Crew name from request:", crew_name)  # Add print statement
        task = Task.objects.get(id=task_id)
        crew = Crew.objects.get(crewName=crew_name)

        if request.user in task.assignedTo.members.all() or request.user.member.position == 'Manager':
            task.assignedTo = crew
            me = request.user.get_username()
            task.assignedFrom = Member.objects.get(username = me)
            task.save()
            print("New Assigned crew:", task.assignedTo)  # Add print statement
            return JsonResponse({'status': 'success', 'assigned_crew': crew.crewName})
        else:
            return JsonResponse({'status': 'error', 'message': 'User must be a crew member or manager to assign the task'})

def get_assigned_crew(request, task_id):
    if request.method == 'GET':
        task = Task.objects.get(id=task_id)
        assigned_crew = task.assignedTo
        print("Assigned crew:", assigned_crew)  # Add print statement
        return JsonResponse({'assigned_crew': assigned_crew.crewName})

def get_crew_options(request):
    if request.method == 'GET':
        crews = Crew.objects.values_list('crewName', flat=True)
        print("Available crews:", crews)  # Add print statement
        return JsonResponse({'crews': list(crews)})
    

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
def generate_route_for_crew(crew_name):
    # Initialize Google Maps client
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    # Fetch tasks for the crew
    crew = Crew.objects.get(crewName=crew_name)
    tasks = Task.objects.filter(assignedTo=crew)[:5]

    if len(tasks) == 0:
        return ""

    # Extract task locations
    task_locations = [task.location for task in tasks]

    # Assuming crew members start from the location of the first task
    start_location = task_locations[0]

    # Generate directions
    directions = gmaps.directions(
        origin=start_location,
        destination=task_locations[-1],
        waypoints=task_locations[1:-1],
        optimize_waypoints=True,
    )

    # Extract optimized waypoints from directions
    optimized_waypoints = [step["end_location"] for step in directions[0]["legs"]]
    
    # Construct Google Maps URL
    map_url = "https://www.google.com/maps/dir/?api=1"
    map_url += "&origin=" + urllib.parse.quote_plus(start_location)
    map_url += "&destination=" + urllib.parse.quote_plus(task_locations[-1])
    for waypoint in optimized_waypoints:
        map_url += "&waypoints=" + urllib.parse.quote_plus(f"{waypoint['lat']},{waypoint['lng']}")
    map_url += "&travelmode=driving"

    return map_url


def send_routes():
    # Fetch crews
    crews = Crew.objects.all()  #To test this crew since has real data

    # Loop through each crew
    for crew in crews:
        # Get members of the crew
        members = crew.members.all()

        # Loop through each member
        for member in members:
            # Generate route for the crew using Google Maps API
            
            route = generate_route_for_crew(crew.crewName)

            # Parse the URL
            route = urlparse(route)
            
            # Parse the query parameters
            query_params = parse_qs(route.query)
            
            # Re-encode the query parameters without HTML entities
            encoded_params = urlencode(query_params, doseq=True)
            
            # Reconstruct the URL without HTML entities
            route = urlunparse(route._replace(query=encoded_params))

            print(route)

            # Render email content with the route
            email_content = render_to_string('basic/email_template.html', {'route': route})

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


    