# Adds additional extras to use in templates - this Python logic is separate from the rest of the project Python code so it doesn't make the template vulnerable to external attacks
from django import template

register = template.Library() # Performs logic required in template in view

# Can let template check if specified user has authenticated their attendance at a specified event
@register.filter(name='attendance_authenticated')
def attendance_authenticated(event, user):
    from main.models import Attendance
    return Attendance.objects.filter(event=event, student=user.student).exists()

# Returns time at which user authenticated their attendance at an event
@register.filter(name='auth_time')
def auth_time(event, user):
    from main.models import Attendance
    attendance = Attendance.objects.get(event=event, student=user.student)
    return attendance.auth_time

# Return if a user's attendance at an event requiring verification has been verified
@register.filter(name='attendance_verified')
def attendance_verified(event, user):
    from main.models import Verification
    return Verification.objects.filter(event=event, student=user.student).exists()

# Return time at which a user's attendance at an event was verified
@register.filter(name='verification_time')
def verification_time(event, user):
    from main.models import Verification
    verification = Verification.objects.get(event=event, student=user.student)
    return verification.verification_time