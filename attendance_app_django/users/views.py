from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Student

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

    # Syntax render(request, template path, context)
    return render(request, 'users/profile.html', context)


# View another user's profile (only available to staff / admin user)
@login_required
def user_profile(request, username):

    user = get_object_or_404(User, username=username) # extract username from URL   
    
    # If the logged in user is trying to view their own profile, redirect to profile view
    if request.user.groups.filter(name="Admin").exists() or request.user.groups.filter(name="Staff").exists():
        context = {
            'user': user
        }
        return render(request, 'users/user_profile.html', context)
    else:
        return HttpResponse(status=403)  # Students shouldn't be able to see other profiles
