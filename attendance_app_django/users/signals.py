from django.db.models.signals import post_save # import post_save model which is activated when an object is saved
# import sender and receiver of signal
from django.contrib.auth.models import User
from django.dispatch import receiver
# import profile class
from .models import Profile, Student, Staff, Admin

# When a post_save signal is received due to a new user being created, create a new profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs): # create new profile with instance = the user that was created
    # if the user was created, create a new profile with the instance of the user that was created
    if created:
        Profile.objects.create(user=instance)

# Save the user profile once the user object has been saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# When a post_save signal is received due to a User object being saved, create an instance of the User type
@receiver(post_save, sender=User)
def create_user_type_object(sender, instance, **kwargs):
    if instance.groups.filter(name='Students').exists():
        if not Student.objects.filter(user=instance).exists():
            # Create Student object if a user is added to group "Students"
            Student.objects.create(user=instance)
            instance.student.save()
    elif instance.groups.filter(name='Staff').exists():
        if not Staff.objects.filter(user=instance).exists():
            Staff.objects.create(user=instance)
            instance.staff.save()
    elif instance.groups.filter(name='Admin').exists():
        if not Admin.objects.filter(user=instance).exists():
            Admin.objects.create(user=instance)
            instance.admin.save()