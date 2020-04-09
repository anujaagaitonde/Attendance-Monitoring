from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

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

    # If form is submitted (possibly with new data), instantiate form with post data
    if request.method =='POST':
        u_form = UserUpdateForm(request.POST, instance = request.user) # user update form
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile) # profile update form - needs to contain image file
        # Check form validity - only save form if both are valid
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # display one time success message, uses fstring
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # redirect here to satisfy post-get-redirect pattern. Once a post request has been submitted, it should be changed to a post request to avoid submitting the same info twice
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    # Store forms in context dictionary to pass to template
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)