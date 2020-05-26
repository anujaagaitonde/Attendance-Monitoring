# Adds additional extras to use in templates - this Python logic is separate from the rest of the project Python code so it doesn't make the template vulnerable to external attacks
from django import template

register = template.Library() # Performs logic required in template in view

# Can let template check if specified user has authenticated their attendance at a specified event
@register.filter(name='attendance_authenticated')
def attendance_authenticated(event, user):
    from main.models import Attendance
    return Attendance.objects.filter(event=event, student=user.student).exists()

@register.filter(name='auth_time')
def auth_time(event, user):
    from main.models import Attendance
    attendance = Attendance.objects.get(event=event, student=user.student)
    return attendance.auth_time