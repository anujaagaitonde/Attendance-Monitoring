from django.db import models
from datetime import datetime
from django.utils import timezone
from users.models import Student, Staff
from django.urls import reverse
import uuid


# Create your models here.

# Return one hour ahead of now to add default to end_time of event
def one_hour_ahead():
    return timezone.now() + timezone.timedelta(hours=1)

# Event model
class Event(models.Model):
    # Type of event
    EVENT_TYPES = (
        ('LE', 'Lecture'),
        ('EX', 'Examination'),
        ('TU', 'Tutorial'),
        ('SG', 'Study Group')
    )

    title = models.CharField(max_length = 100)
    event_type = models.CharField(max_length=2, choices=EVENT_TYPES) # Lecture, tutorial, exam or study group
    start_time = models.DateTimeField(default = timezone.now)
    end_time = models.DateTimeField(default = one_hour_ahead)
    location = models.CharField(max_length = 100, null = True)
    leader = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name = 'staff_leader') # Leader must be a staff member
    attendees = models.ManyToManyField(Student, related_name='student_attendees')
    auth_uuid = models.UUIDField(default=uuid.uuid4, editable = False) # Generates authentication hash
    register_taken = models.BooleanField(default = False)

    # Print event object as its event title
    def __str__(self): 
        return self.title

    # Returns if event is currently happening
    def happening_now(self):
        if timezone.now() >= self.start_time and timezone.now() < self.end_time:
            return True
        else:
            return False
    
    # Returns if event has started
    def started(self):
        if timezone.now() >= self.start_time:
            return True
        else:
            return False
    
    # return absolute url of 'event-detail' page for event instance to redirect to after authentication
    def get_absolute_url(self):
        # to get specific event-detail URL, need to pass event instance primary key
        return reverse('event-detail', kwargs={'pk': self.pk})
        

# Attendance authentication model
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE) # if student is deleted, attendance authentications should be deleted too
    event = models.ForeignKey(Event, on_delete=models.CASCADE) # if event is deleted, attendance authentications should be deleted too
    auth_time = models.DateTimeField(null=True)

    def __str__(self):
        return f'Student {self.student.user.username} attendance at {self.event.title}'
    

# Attendance verification model
class Verification(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_to_verify') # if event is deleted, attendance verifications should also be deleted
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    verification_time = models.DateTimeField(null=True)

    def __str__(self):
        return f'Student {self.student.user.username} verification at {self.event.title}'
