from django.shortcuts import render, redirect
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
from tasks.forms import *

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

@login_required
def addNote(request, task_id):
    task = Task.objects.get(id = task_id)
    if request.method == 'POST':
        date = timezone.now()
        form = AddNotes(request.POST, date)
        if form.is_valid():

            form.save()
            return redirect('basic:assignments')
        else:
            form = AddNotes()
        return render(request, "basic/addNote.html", {
            'form': form,
            'task': task
            })
    
    else:
        form = AddNotes()
        return render(request, "basic/addNote.html", {
            'form': form,
            'task': task
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
