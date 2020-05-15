from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    context = {
        'title': 'Success',
        'random_text': 'Display random text'
    }

    # render: (request, path of template in templates dir, context - passes data into template)
    return render(request, 'main/home.html', context)
