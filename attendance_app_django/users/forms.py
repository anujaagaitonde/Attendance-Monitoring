from django import forms
from django.contrib.auth.models import User
from .models import Profile

# Update profile (image)
class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['image']