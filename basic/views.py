from django.shortcuts import render
from django.http import Http404
from .models import Computed
from django.views.decorators.http import require_GET, require_POST
from tasks.models import *
from django.utils import timezone
from tasks.models import Task, Equipment, Note
from django.http import JsonResponse
from django.db.models import Q

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

def homepage(request):
    crew = Crew.objects.all()
    task = Task.objects.all()
   
    return render(request, 'basic/homepage.html', {
        'crew': crew, 
        'task' : task, 
    })


"""Task Page"""
def assignments(request):

    tasks = Task.objects.all()
    equipment = Equipment.objects.all()
    notes = Note.objects.all()
    

    return render(request, 'basic/assignments.html', {
        'tasks': tasks,
        'equipment': equipment,
        'notes': notes
    })

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