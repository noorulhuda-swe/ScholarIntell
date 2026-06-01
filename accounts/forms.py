from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name  = forms.CharField(max_length=100, required=True)
    email      = forms.EmailField(required=True)

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model  = StudentProfile
        fields = [
            'cgpa',
            'degree_level',
            'field_of_study',
            'country_of_origin',
            'language_cert',
            'language_score',
            'preferred_country',
        ]
        widgets = {
            'cgpa':             forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '4.0', 'placeholder': 'e.g. 3.5'}),
            'language_score':   forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'e.g. 6.5 for IELTS'}),
            'field_of_study':   forms.TextInput(attrs={'placeholder': 'e.g. Computer Science'}),
            'country_of_origin':forms.TextInput(attrs={'placeholder': 'e.g. Pakistan'}),
            'preferred_country':forms.TextInput(attrs={'placeholder': 'e.g. Germany (optional)'}),
        }
