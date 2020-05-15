from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Profile view
@login_required # Decorator means user can only access profile page if they are logged in
def profile(request):

    # If form is submitted (possibly with new data), instantiate form with post data
    if request.method =='POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile) # profile update form - needs to contain image file
        # Check form validity - only save form if valid
        if p_form.is_valid():
            p_form.save()
            # display one time success message, uses fstring
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # redirect here to satisfy post-get-redirect pattern. Once a post request has been submitted, it should be changed to a post request to avoid submitting the same info twice
    # Otherwise instantiate form with existing data
    else:
        p_form = ProfileUpdateForm(instance = request.user.profile)

    # Store forms in context dictionary to pass to template
    context = {
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)