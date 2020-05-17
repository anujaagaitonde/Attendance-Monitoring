from django.db import models
from PIL import Image
from django.contrib.auth.models import User


# User profile model
class Profile(models.Model):
    # Create 1-to-1 mapping from Django user to profile (1 profile per user). on_delete argument set to CASCADE says that if the user is deleted, their profile should also be deleted (not the other way aroudn)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Profile picture field, allow upload to directory 'profile_pics' (image url) otherwise set default image
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

# Student user model (type of User - each student has a User object (account))
class Student(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE) # Each Student object maps to one account and vice versa
    cid = models.AutoField(primary_key=True) # CIDs have 8 digits
    course = models.CharField(max_length=50, null = True)
    year = models.IntegerField(null=True)
    
    def __str__(self):
        return f'Student {self.user.username}'

# Staff user model (type of User - each staff member has a User object (account))
class Staff(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE) # Each Staff object maps to one account and vice versa
    # Can add any other necessary staff attributes
    
    def __str__(self):
        return f'Staff {self.user.username}'
    
    class Meta:
        verbose_name_plural = 'Staff' # otherwise default in admin page would be 'Staffs'

# Admin user model (type of User - each admin user has a User object (account))
class Admin(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE) # Each Admin object maps to one account and vice versa
    # Can add any other necessary staff attributes
    
    def __str__(self):
        return f'Admin {self.user.username}'