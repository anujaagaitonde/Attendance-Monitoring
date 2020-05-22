from django import forms
from .models import Attendance

# Authenticate attendance
class AttendanceAuthenticateForm(forms.Form):
    auth_hash = forms.UUIDField(label='Authentication Hash') # Input is valid if it is a valid UUID

