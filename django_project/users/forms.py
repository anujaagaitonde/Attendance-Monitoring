from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Creates a form which inherits from the user creation form and adds an email field
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() # default state = required field
    
    # meta class gives us a nested namespace for configurations and keeps the configurations in one place
    class Meta:
        # Specify model (DB table) that we want the form to interact with
        model = User 
        # Fields shown on form, and in what order
        fields = ['username','email','password1','password2']