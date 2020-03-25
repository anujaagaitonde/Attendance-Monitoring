from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    # if the request has a POST method, then we want to instantiate a form which has the request.POST data
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # the data obtained could be any type of post data, so we want to validate that it's the fields and data from the form we expect
        if form.is_valid():
            form.save() # save the user
            username = form.cleaned_data.get('username') # extracted form data is stored in cleaned_data dictionary
            # display one time success message, uses fstring
            messages.success(request, f'Your account has been created. Please log in.')
            return redirect('login')
    # Otherwise just create a blank form
    else:
        form = UserRegisterForm()
    # request, template path, context as dictionary
    return render(request, 'users/register.html', {'form': form})

# Profile view
@login_required # Decorator means user can only access profile page if they are logged in
def profile(request):
    return render(request, 'users/profile.html')