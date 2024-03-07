from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    

# Augment django's User model with new attributes
class Member(User):
    def __str__(self):
        return f"{self.username}"
    skills = models.TextField()
    position = models.enums()
    profileImage = models.ImageField()


# One crew to many users and vice versa
class Crew(models.Model):
    crewName = models.CharField
    members = models.ManyToManyField(Member)
    

# One project, many tasks
# Up to one assignee for a task
class Task(models.Model):
    name = models.TextField()
    location = models.CharField()
    id = models.CharField()
    description = models.TextField()
    assignedFrom = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
    assignedTo = models.ForeignKey(Crew, null=True, on_delete=models.SET_NULL)
    # 0 = not started, 1 = in progress, 2 = completed 
    status = models.IntegerField(default=0) # Better to use IntegerChoicesField here
    startDate = models.DateField()
    dueDate = models.DateField()
    equipment = models.ManyToOneRel()
    notes = models.ManyToOneRel()
    def started(self):
        self.status = 1

    def has_started(self):
        return self.status == 1

    def completed(self):
        self.status = 2

    def has_completed(self):
        return self.status == 2

    def __str__(self):
        return f"{self.description} -> {self.project.name} -> {self.assignee.username}"

class Equipment(models.Model):
    name = models.CharField()
    description = models.TextField()
    status = models.enums()
    assignedTo = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL)