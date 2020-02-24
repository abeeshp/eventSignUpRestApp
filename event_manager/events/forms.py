from django import forms
from .models import Registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'name',
            'email',
            'event'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'size': 100, 'title': 'Your name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'size': 100, 'title': 'Your mailId', 'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-control'}),
        }
