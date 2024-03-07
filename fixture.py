from basic.models import Computed
from django.contrib.auth.models import User
from tasks.models import Project, Member, Notification, Task
from django.utils import timezone

# Delete existing objects
for c in [Computed, Project, Member, Notification, Task]:
    c.objects.all().delete()


# Install fixture
newobject = Computed(input=80,output=6400,time_computed=timezone.now())
newobject.save()

projects = [Project.objects.create(name=name) for name in ["Wireframes", "Models", "Fake data"]]
for project in projects:
    project.save()

members = [Member.objects.create_user(username= "m"+str(i)) for i in range(0,10)]
for m in members:
    m.save()


# Task status 0 = not started, 1 = in progress, 2 = completed
t0 = Task(description="Home page", project=projects[0], assignee=members[0])
t0.save()
t1 = Task(description="Login page", project=projects[0], assignee=members[1])
t1.save()
t2 = Task(description="Tasks dashboard page", project=projects[0], assignee=members[1])
t2.started()
t2.save()

t3 = Task(description="Member model", project=projects[1], assignee=members[2])
t3.started()
t3.save()
t4 = Task(description="Task model", project=projects[1], assignee=members[4])
t4.completed()
t4.save()
t5 = Task(description="Notification model", project=projects[1], assignee=members[3])
t5.save()
t6 = Task(description="Project model", project=projects[1], assignee=members[1])
t6.started()
t6.save()

t7 = Task(description="Fake members", project=projects[2], assignee=members[4])
t7.completed()
t7.save()
t8 = Task(description="Fake notifications", project=projects[2], assignee=members[5])
t8.started()
t8.save()
t9 = Task(description="Fake projects", project=projects[2], assignee=members[5])
t9.started()
t9.save()
t10 = Task(description="Fake tasks", project=projects[2], assignee=members[1])
t10.save()



n1 = Notification(message="Your wireframe task is running behind schedule!")
n1.save()
n1.users.add(members[0], members[1])

n2 = Notification(message="Good job with your progress on Task model")
n2.save()
n2.users.add(members[4])

n3 = Notification(message="Terrific job on your previous project!")
n3.save()
n3.users.add(members[1])


# Some useful queries that may be pertinent while writing view functions

# All tasks within project Models

tasks = Task.objects.filter(project__name="Models")
print(f"Tasks within the project Models are: {[t.description for t in tasks]}")

# Members working on project Fake data

members=Task.objects.filter(project__name="Fake data").values('assignee').distinct()
print(f"\nTeam members working on project Fake data are: \
{[Member.objects.get(pk=x['assignee']).username for x in members]}")

# Tasks assigned to member m4

tasks = Task.objects.filter(assignee__username="m4")
print("\nTasks assigned to user m4 are: {[t.description for t in tasks]}")

# Notifications for member m1

notifications = Member.objects.filter(username="m1")[0].notification_set.all()
print(f"\nNotifications for team member m1 are: {[n.message for n in notifications]}")

# Task description for those tasks have yet to be started within project Wireframes

descriptions = Task.objects.filter(project__name="Wireframes", status = 0).values_list('description', flat=True)
print(f"\nTasks that have yet to start in project Wireframes: {list(descriptions)}")

