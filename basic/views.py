from django.shortcuts import render
from django.http import Http404
from .models import Computed
from django.views.decorators.http import require_GET, require_POST
from tasks.models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from tasks.models import Task, Equipment, Note
from django.http import JsonResponse
from django.db.models import Q
from django.apps import apps
import googlemaps
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.

# Computation function
def compute(request, value):
    try:
        input = int(value)
        precomputed = Computed.objects.filter(input=input)
        if precomputed.count() != 0:  
            # This was already computed, so look up answer
            answer = precomputed[0].output
            time_computed = precomputed[0].time_computed
        else:
            # Compute the answer
            answer = input * input
            time_computed = timezone.now()
            # Save it into the database
            computed = Computed(
                input=input, 
                output=answer,
                time_computed=time_computed
            )
            computed.save() # Store it into the database
    except:
        raise Http404(f"Invalid input: {value}")

    return render (
        request,
        "basic/compute.html",
        {
            'input': input,
            'output': answer,
            'time_computed': time_computed

        }
    )

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
        'notes' : notes
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


def send_routes(request):
    # Fetch all crews
    crews = Crew.objects.all()

    # Loop through each crew
    for crew in crews:
        # Generate route for the crew using Google Maps API
        route = generate_route_for_crew(crew)

        # Render email content with the route
        email_content = render_to_string('email_template.html', {'route': route})

        # Send email to crew
        send_mail(
            'Your Daily Route',
            email_content,
            'your_email@example.com',
            [crew.email],
            fail_silently=False,
        )

    return HttpResponse('Routes sent successfully')

