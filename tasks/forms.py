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

    def clean(self):
        cleaned_data = super().clean()
        crewName = cleaned_data.get('crewName')

        if crewName in 'crewName':
            raise forms.ValidationError("Crew already exists.")

        return cleaned_data
    
class EditCrewMemberForm(forms.ModelForm):
    class Meta:
        model = Crew
        fields = ['crewName', 'members']

    def clean(self):
        cleaned_data = super().clean()
        crewName = cleaned_data.get('crewName')
        members = cleaned_data.get('members')

        if members in 'crewName':
            raise forms.ValidationError("Crew already exists.")

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