from django.db import models
from django.utils import timezone # for datetime data
from django.contrib.auth.models import User # import user table from built in django auth
from django.urls import reverse

# Create your models here.

# Each database table is its own model, created by a class with attributes equal to the fields of the DB objects
class Post(models.Model):
    title = models.CharField(max_length = 100) # Limited length title field
    content = models.TextField() # Unlimited length (multiple lines) text field
    date_posted = models.DateTimeField(default = timezone.now) # 'now' is a function within timezone, but we don't want to call it yet, hence no ()
    author = models.ForeignKey(User, on_delete = models.CASCADE) # Join to users table on authors field using foreign key mapping. on_delete arg means that if a user is deleted, their post is also deleted

    def __str__(self):
        return self.title
    
    # return absolute url of 'post-detail' page for post instance created so that redirect occurs after creating a new post
    def get_absolute_url(self):
        # to get specific post-detail URL, need to pass post instance primary key
        return reverse('post-detail', kwargs={'pk': self.pk})

