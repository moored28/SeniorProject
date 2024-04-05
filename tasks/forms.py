from django import forms
from .models import Equipment
from .models import Member
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

    ## Validate that username is not already taken
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Member.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    ## Validate that email is not already taken
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Member.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email

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