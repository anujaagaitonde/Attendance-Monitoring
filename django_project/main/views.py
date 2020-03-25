from django.shortcuts import render
from .models import Post # import post model from DB (. because this file and models.py are in the same directory)

# Create your views here.

# Take in a HTTP request as input and return a HTTP response which displays 
def home(request):
    # all relevant dummy data stored in context dictionary (contains posts which is a list of dictionaries)
    context = {
        # key = posts
        'posts': Post.objects.all() # load posts into home view sfrom Post model
    }
    # render: (request, path of template in templates dir, context - passes data into template)
    return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html', {'title': 'About'})
