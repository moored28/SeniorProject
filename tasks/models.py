from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    

# Augment django's User model with new attributes
class Member(User):
    def __str__(self):
        return f"{self.username}"
    skills = models.TextField()
    position = models.CharField(max_length = 50)
    profileImage = models.ImageField()


# One crew to many users and vice versa
class Crew(models.Model):
    crewName = models.CharField(max_length = 50)
    members = models.ManyToManyField(Member)

    def __str__(self):
        return f"{self.crewName}"
    

# Tasks
# Up to one crew for a task
class Task(models.Model):
    name = models.CharField(max_length = 50)
    location = models.CharField(max_length = 50)
    description = models.TextField()
    assignedFrom = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
    assignedTo = models.ForeignKey(Crew, null=True, on_delete=models.SET_NULL)
    # 0 = not started, 1 = in progress, 2 = completed 
    status = models.IntegerField(default=0) # Better to use IntegerChoicesField here
    startDate = models.DateField()
    dueDate = models.DateField(null = True, blank = True)

    def started(self):
        self.status = 1

    def has_started(self):
        return self.status == 1

    def completed(self):
        self.status = 2

    def has_completed(self):
        return self.status == 2

    def __str__(self):
        return f"{self.name} -> {self.description} -> {self.assignedFrom.username}"

class Equipment(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField()
    status = models.CharField(max_length = 50, default='Available')
    assignedTo = models.ForeignKey(Crew, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name}"


class Note(models.Model):
    text = models.TextField()
    createdBy = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
    picture = models.ImageField(null=True, blank=True)
    dateCreated = models.DateTimeField()
    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL)
