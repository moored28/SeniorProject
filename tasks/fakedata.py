from tasks.models import Member, Crew, Task, Equipment, Note
from django.contrib.auth.models import User
from faker import Faker
import random

from datetime import timedelta
import requests
from django.core.files.base import ContentFile

# Delete existing objects
for c in [Crew, Note, Member, User, Equipment, Task]:
    c.objects.all().delete()

fake = Faker()

# Create superuser account
User.objects.create_superuser('admin', password='admin')

##Members
def create_users(num_members):
    for _ in range(num_members):
        username = fake.user_name()
        email = fake.email()
        skills = fake.text()
        position = fake.job()
        # Download a random image from the internet
        response = requests.get(fake.image_url())
        profile_image = ContentFile(response.content, 'profile_image.jpg')
        # Create the member
        member = Member(username=username, email=email, skills=skills, position=position)
        member.profileImage.save('profile_image.jpg', profile_image)
        member.save()

#Crews
def create_crews(num_crews, max_members_per_crew, members):
    for i in range(1, num_crews + 1):
        crew_name = f"Crew{i}"
        crew = Crew.objects.create(crewName=crew_name)
        num_members = random.randint(1, max_members_per_crew)
        crew.members.set(random.sample(members, num_members))
        crew.save()

##Tasks
def create_tasks(num_tasks, crews, members):
    for _ in range(num_tasks):
        crew = random.choice(crews)
        existing_tasks = Task.objects.filter(assignedTo=crew).exists()

        # Ensure due date is after start
        start_date = fake.date_this_year()
        end_date = fake.date_between_dates(date_start=start_date, date_end=start_date + timedelta(days=365))

        # Check if there are any existing tasks assigned to the crew
        if not existing_tasks or not Task.objects.filter(assignedTo=crew, status=1).exists():
            # If no existing in-progress tasks, create a new task with status=1
            task = Task.objects.create(
                name=fake.catch_phrase(),
                location=fake.address(),
                description=fake.text(),
                assignedFrom=random.choice(members),
                assignedTo=crew,
                status=1,
                startDate=start_date,
                dueDate=end_date
            )
            task.save()
        else:
            # If existing in-progress tasks, create a new task with random status (0 or 2)
            status = random.choice([0, 2])
            task = Task.objects.create(
                name=fake.catch_phrase(),
                location=fake.address(),
                description=fake.text(),
                assignedFrom=random.choice(members),
                assignedTo=crew,
                status=status,
                startDate=start_date,
                dueDate=end_date
            )
            task.save()

##Equipment
def create_equipment(num_equipment, crews):
    for _ in range(num_equipment):
        status = random.choice(['Available', 'Assigned', 'Maintenance'])
        assigned_to = random.choice(crews) if status != 'Available' else None
        
        equipment = Equipment.objects.create(
            name=fake.word(),
            description=fake.text(),
            status=status,
            assignedTo=assigned_to
        )
        equipment.save()

def create_notes(num_notes, members, tasks):
    for _ in range(num_notes):
        note = Note.objects.create(
            text=fake.text(),
            createdBy=random.choice(members),
            picture=fake.image_url(),
            dateCreated=fake.date_time_this_year(),
            task = random.choice(tasks)
        )
        note.save() 

# Populate users
create_users(10)  # Generate 20 users
members = list(Member.objects.all())
# Populate crews

create_crews(5, 5, members)  # Generate 5 crews with up to 5 members each
crews = list(Crew.objects.all())
# Populate tasks

create_tasks(10, crews, members)  # Generate 10 tasks assigned to random crews
tasks = list(Task.objects.all())

# Populate equipment
create_equipment(20, crews)  # Generate 20 equipment assigned to random crews

# Populate notes

create_notes(10, members ,tasks) # Generate 10 notes on random tasks


