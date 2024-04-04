from django import forms
from .models import Crew

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
