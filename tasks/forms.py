from django import forms
from .models import *
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
        members = cleaned_data.get('members')

        if members in 'crewName':
            raise forms.ValidationError("Crew already exists.")

        return cleaned_data

class AddNotes(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']

    def clean(self):
        cleaned_data = super().clean()
        comment = cleaned_data.get('text')
        date = cleaned_data.get('dateCreated')

        if comment or date is None:
            raise forms.ValidationError("Cannot be empty.")
        
        return cleaned_data