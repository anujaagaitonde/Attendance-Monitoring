from django.db import models
from datetime import datetime
from django.utils import timezone
from users.models import Student, Staff

# Create your models here.

# Return one hour ahead of now to add default to end_time of event
def one_hour_ahead():
    return timezone.now() + timezone.timedelta(hours=1)


# Event model
class Event(models.Model):
    title = models.CharField(max_length = 100)
    start_time = models.DateTimeField(default = timezone.now) # if no start time specified, set as null in DB
    end_time = models.DateTimeField(default = one_hour_ahead)
    location = models.CharField(max_length = 100, null = True)
    leader = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name = 'staff_leader') # Leader must be a staff member
    attendees = models.ManyToManyField(Student, related_name='student_attendees')

    # Print event object as its event title
    def __str__(self): 
        return self.title