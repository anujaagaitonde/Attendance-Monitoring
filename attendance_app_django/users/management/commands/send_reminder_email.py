from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from main.models import Event


class Command(BaseCommand):
    help = 'Sends reminder emails'

    # Business logic to send reminder emails
    def handle(self, *args, **kwargs):
        td = timezone.timedelta(days=7)
        # Used to extract users who haven't logged into the system in the past 7 days
        cutoff = timezone.now() - td
        # Produce lists of all staff members
        user_list = User.objects.filter(groups__name="Staff")
        dt = ()
        for user in user_list:
            dl = list(dt)
            # Only send an email to that user if they have outstanding registers from events that occurred more than one week ago
            num_outstanding_regs = Event.objects.filter(
                leader=user.staff, register_taken=False, start_time__lte= cutoff).exclude(event_type="LE").count()
            if num_outstanding_regs > 1:
                # Create email data
                data = ('Check Imperial Attendance App', 'Dear '+str(user.username)+',\n\nYou have '+str(num_outstanding_regs) +
                        ' registers to complete which are over a week old. Please log in to the Imperial Attendance App to complete them.\n\nRegards, \n\nImperial Attendance App', 'imperialattendance@gmail.com', [str(user.email)])
                dl.append(data)
            # Exception (for email grammar) if there is only one outstanding register
            elif num_outstanding_regs == 1:
                data = ('Check Imperial Attendance App', 'Dear '+str(user.username)+',\n\nYou have '+str(num_outstanding_regs) +
                        ' register to complete which is over a week old. Please log in to the Imperial Attendance App to complete it.\n\nRegards, \n\nImperial Attendance App', 'imperialattendance@gmail.com', [str(user.email)])
                dl.append(data)
            dt = tuple(dl)
        send_mass_mail(dt)
