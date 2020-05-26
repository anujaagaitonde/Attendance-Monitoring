from django import forms

# Authenticate attendance
class AttendanceAuthenticateForm(forms.Form):
    auth_hash = forms.UUIDField(label='Authentication Hash') # Input is valid if it is a valid UUID

# Staff verification of students
class AttendanceVerificationForm(forms.Form):
    mark_attendance = forms.BooleanField(label='') # Boolean input to mark attendance of student


