# Static file to list database queries from YT tutorial 5 - won't actually run
from main.models import Post # import posts table
from django.contrib.auth.models import User # import user table from django built in auth table

# query to extract all users in a QuerySet object
User.objects.all()

# extract the first user
User.objects.first()

# extract the last user
User.objects.last()

# extract user filtered by particular username, n.b. this only extracts one user inside the QuerySet object since usernames are unique. 
# If the filter selection is not unique then all occurrences will be stored in the QuerySet object
User.objects.filter(username='agaitonde')

# Extract actual user object and store in variable, filtered by username (there is only one user object in the returned QuerySet object above)
user = User.objects.filter(username='agaitonde').first()

# Can also identify user by id which is the primary key pk
user.id # returns the same as
user.pk

# Return all posts as QuerySet object
Post.objects.all()

# create new post by author = user
post_1 = Post(title='Blog 1', content='First post content', author = user) # n.b. we do not need to add time data because this is set as default to now
# creates a new post object but we need to actually save it to the DB
post_1.save()

# Once new posts are created, query post details
# extract first post
post = Post.objects.first()
post.content # returns post content
post.date_posted # returns datetime object
post.author # returns user object
# can also access details about authors
post.author.email

# Django contains an easy way access all posts created by a particular user
user.post_set # returns unintuitive object, instead use
user.post_set.all()

# alternative way to create a post by user (now no need to save)
user.post_set.create(title='Blog 3', content = 'Third post content!')


