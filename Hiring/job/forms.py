
from django.forms.widgets import HiddenInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CandidateSignupForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['email', 'name']

class CandidateLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
        fields = ['phone', 'experience', 'current_ctc', 'expected_ctc', 'graduated_from', 'degree', 'skills', 'resume']

class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ['job', 'candidate_detail', 'recruiter_detail', 'profile', 'about']
        widgets = {
            'job': forms.HiddenInput(),
            'candidate_detail': forms.HiddenInput(),
            'recruiter_detail': forms.HiddenInput(),
            'profile': forms.HiddenInput(),
        }