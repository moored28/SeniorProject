from django import forms
from .models import *
from django.forms import ModelForm
from django.db import models    

from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Member
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'position']

# Used on Profile page
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'skills', 'profileImage']

class EditEquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'status', 'assignedTo']

    # Validate that equipment in maintenance or available can't be assigned to a crew
    # and that equipment marked assigned, must have an assigned crew
    # clean method is called when validating form data
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        crew = cleaned_data.get('assignedTo')

        if status in ['Maintenance', 'Available'] and crew is not None:
            raise forms.ValidationError("Equipment with status maintenance or available can't be assigned to a crew")
        if status == 'Assigned' and crew is None:
            raise forms.ValidationError("Equipment marked assigned must have an assigned crew")
        return cleaned_data
    
class AddEquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'status', 'assignedTo']
    
    # Validate that equipment in maintenance or available can't be assigned to a crew
    # and that equipment marked assigned, must have an assigned crew
    # clean method is called when validating form data
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        crew = cleaned_data.get('assignedTo')

        if status in ['Maintenance', 'Available'] and crew is not None:
            raise forms.ValidationError("Equipment with status maintenance or available can't be assigned to a crew")
        if status == 'Assigned' and crew is None:
            raise forms.ValidationError("Equipment marked assigned must have an assigned crew")
        return cleaned_data

class AddCrewForm(forms.ModelForm):
    class Meta:
        model = Crew
        fields = ['crewName']

    def save(self, commit=True):
        crew_name = self.cleaned_data['crewName']
        existing_crew = Crew.objects.filter(crewName=crew_name).first()
        if existing_crew:
            existing_crew.delete()  # Delete the existing crew
        else:
            super().save(commit)  # Save the new crew if it doesn't exist

        return None  # We don't return any instance since it's deleted or not created

    def clean_crewName(self):
        crew_name = self.cleaned_data.get('crewName')
        return crew_name
    
class EditCrewMemberForm(forms.ModelForm):
    class Meta:
        model = Crew
        fields = ['crewName', 'members']

    def clean(self):
        cleaned_data = super().clean()
        crewName = cleaned_data.get('crewName')

        try:
            crewName = Crew.objects.get(crewName=crewName)
        except Crew.DoesNotExist:
            raise forms.ValidationError("Crew does not exist.")

        return cleaned_data


class AddNotes(forms.ModelForm):
    text = forms.CharField()
    #createdBy = models.ForeignKey(Member, models.SET_NULL)
    #picture = forms.ImageField()
    #dateCreated = forms.DateTimeField()
    task = models.ForeignKey(Task, models.SET_NULL)
    
    class Meta:
        model = Note
        #fields = ['text', 'picture']
        fields = ['text']

    def clean(self):
        cleaned_data = super().clean()
        comment = cleaned_data.get('text')
        #picture= cleaned_data.get('picture')
        #date = cleaned_data.get('dateCreated')
        task = cleaned_data.get('task')


        if comment is None:
            raise forms.ValidationError("Empty comment.")
        
        
        return cleaned_data
    
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'location', 'description', 'assignedFrom', 'assignedTo', 'status', 'startDate', 'dueDate']

    def clean(self):
        cleaned_data = super().clean()
        assigned_to = cleaned_data.get('assignedTo')
        status = cleaned_data.get('status')

        if assigned_to is None and status != 0:
            self.add_error('status', 'Status must be 0 if assigned to None.')

        start_date = cleaned_data.get('startDate')
        due_date = cleaned_data.get('dueDate')

        if start_date and due_date and start_date > due_date:
            raise ValidationError("Due date must be after start date.")

        return cleaned_data