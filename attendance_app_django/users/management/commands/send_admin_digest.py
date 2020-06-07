from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from main.models import Event, Attendance

class Command(BaseCommand):
    help = 'Sends attendance digest emails to admin users'

    # Business logic to send attendance digest emails
    def handle(self, *args, **kwargs):
        td = timezone.timedelta(days=14) # Used to extract events from the past 2 weeks
        cutoff = timezone.now() - td
        # Produce list of all students
        user_list = User.objects.filter(groups__name="Students").order_by('first_name', 'last_name')
        students = ''
        for user in user_list:
            # Count events a student was supposed to attend in the past 2 weeks
            total_events = Event.objects.filter(attendees = user.student, start_time__gt = cutoff).count()
            # Count events a student authenticated their attendance at
            total_auths = Attendance.objects.filter(student = user.student, event__start_time__gt = cutoff).count()
            num_events_missed = total_events - total_auths
            # Only list the student in the email if they have missed more than 5 events in the past 2 weeks
            if num_events_missed >= 5:
                # Add student's name to students list
                students += user.first_name + str(' ') + user.last_name + '\n'
        # Prepare email messages
        admin_list = User.objects.filter(groups__name="Admin")
        dl = []
        for admin in admin_list:
            message = 'Dear '+str(admin.username)+',\n\nThe following students have missed more than 5 events in the past two weeks:\n\n'+ students + '\n Please log in to the Imperial Attendance App to view their attendance records.\n\nRegards, \n\nImperial Attendance App'
            data = ('Weekly Attendance Digest', message, 'imperialattendance@gmail.com', [str(admin.email)])
            dl.append(data)
        dt = tuple(dl)
        send_mass_mail(dt)
