from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# User profile model
class Profile(models.Model):
    # Create 1-to-1 mapping from Django user to profile. on_delete argument set to CASCADE says that if the user is deleted, their profile should also be deleted (not the other way aroudn)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Profile picture field, allow upload to directory 'profile_pics' otherwise set default image
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        # Print user profile as 'Username Profile'
        return f'{self.user.username} Profile'

    # override pre-existing save method to resize profile image
    def save(self, **kwargs):
        super().save(**kwargs) # access save method of parent class

        # Open image
        img = Image.open(self.image.path)

        # Resize image and overwrite image file
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)



