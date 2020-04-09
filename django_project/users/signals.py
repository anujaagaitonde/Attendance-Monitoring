from django.db.models.signals import post_save # import post_save model which is activated when an object is saved
# import sender and receiver of signal
from django.contrib.auth.models import User
from django.dispatch import receiver
# import profile class
from .models import Profile

# When a post_save signal is due to a new user being created, create a new profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs): # create new profile with instance = the user that was created
    # if the user was created, create a new profile with the instance of the user that was created
    if created:
        Profile.objects.create(user=instance)

# Save the user profile once it has been created
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
