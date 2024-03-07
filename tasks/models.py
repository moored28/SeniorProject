from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    name = models.TextField()
    # Other project attributes such as manager etc. here
    

# Augment django's User model with new attributes
class Member(User):
    def __str__(self):
        return f"{self.username}"


# One notification to many users and vice versa
class Notification(models.Model):
    message = models.TextField()
    users = models.ManyToManyField(Member)
    

# One project, many tasks
# Up to one assignee for a task
class Task(models.Model):
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assignee = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
    # 0 = not started, 1 = in progress, 2 = completed 
    status = models.IntegerField(default=0) # Better to use IntegerChoicesField here
    # Other attributes such as task deadline etc

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
