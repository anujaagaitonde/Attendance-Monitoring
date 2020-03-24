from django.shortcuts import render

# Create your views here.

# Create posts dummy data - list of dictionaries which contain data about each post
posts = [
    {
        'author': 'Anuja Gaitonde',
        'title': 'Blog post 1',
        'content': 'This is my first post!',
        'date_posted': 'March 24th, 2020',
    },
    {
        'author': 'Raunak Gaitonde',
        'title': 'Blog post 2',
        'content': 'Hello Anuja!',
        'date_posted': 'March 25th, 2020',
    }
]

# Take in a HTTP request as input and return a HTTP response which displays 
def home(request):
    # all relevant dummy data stored in context dictionary (contains posts which is a list of dictionaries)
    context = {
        # key = posts
        'posts': posts
    }
    # render: (request, path of template in templates dir, context - passes data into template)
    return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html', {'title': 'About'})
