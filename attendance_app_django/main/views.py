from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event, Attendance
from .forms import AttendanceAuthenticateForm
from django.utils import timezone
from django.conf import settings

# Create your views here.

# View for homepage. Most likely will be scanner
def home(request):
    context = {
        'title': 'Success',
        'random_text': 'Scanner'
    }

    # render: (request, path of template in templates dir, context - passes data into template)
    return render(request, 'main/home.html', context)

# Displays event details (inherits from generic DetailView). Requires login to access (uses mixin instead of decorator because class-based view)
class EventDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Event

    # Function for UserPassesTestMixin: logged in user can only access this view if they pass the test
    # Only a staff leader, student attendee or admin should be able to view the event details
    def test_func(self):
        event = self.get_object()
        if self.request.user == event.leader.user:
            return True
        elif event.attendees.filter(user=self.request.user):
            return True
        elif self.request.user.groups.filter(name='Admin').exists():
            return True
        else:
            return False


# Class-based My Events page: lists events a user is attending. Inherits from generic ListView
# Default = show upcoming events
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'main/events.html' # Override the template to search for, default = <app>/<model>_<viewtype>.html (main/event_list.html)
    context_object_name = 'events' # Specify what variable name the objects in the list should be called, so they are looped as they were when using the function based view in the template
    paginate_by = 5 # number of events to display per page

    # Override default get_queryset to obtain a more specific queryset to be listed on the page
    # Only view events the logged in user is attending
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Students').exists():
            return Event.objects.filter(attendees=user.student, end_time__gte=timezone.now()).order_by('start_time') # Upcoming events (includes current events) have end time > current time
        elif user.groups.filter(name='Staff').exists():
            return Event.objects.filter(leader=user.staff,end_time__gte=timezone.now()).order_by('start_time')
        elif user.groups.filter(name='Admin').exists(): # Admin users can view all events
            return Event.objects.filter(end_time__gte=timezone.now()).order_by('start_time')

# Class-based My Events page: lists events a user is attending. Inherits from generic ListView
# Show past events
class PastEventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'main/past_events.html' # Override the template to search for, default = <app>/<model>_<viewtype>.html (main/event_list.html)
    context_object_name = 'events' # Specify what variable name the objects in the list should be called, so they are looped as they were when using the function based view in the template
    paginate_by = 5 # number of events to display per page

    # Override default get_queryset to obtain a more specific queryset to be listed on the page
    # Only view events the logged in user has attended
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Students').exists():
            return Event.objects.filter(attendees=user.student, end_time__lte=timezone.now()).order_by('-start_time') # Past events have end time < current time. Display in reverse chronological order
        elif user.groups.filter(name='Staff').exists():
            return Event.objects.filter(leader=user.staff,end_time__lte=timezone.now()).order_by('-start_time')
        elif user.groups.filter(name='Admin').exists(): # Admin users can view all events
            return Event.objects.filter(end_time__lte=timezone.now()).order_by('-start_time')

# View another user's (students) upcoming events
class UserEventListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'main/user_events.html'
    context_object_name = 'events'
    paginate_by = 5

    # Show upcoming events of user with username in URL
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) # Class based view so requires kwargs.get to extract from URL
        return Event.objects.filter(attendees=user.student, end_time__gte=timezone.now()).order_by('start_time')
    
    # Only allow logged in user to access view if they are not a Student
    def test_func(self):
        active_user = self.request.user
        if active_user.groups.filter(name="Admin") or active_user.groups.filter(name="Staff"):
            return True
        else:
            return False
    
    # Send user object of user with username in URL to template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username')) # Class based view so requires kwargs.get to extract from URL
        context['requested_user'] = user
        return context

# View another user's (students) events
class UserPastEventListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'main/user_past_events.html'
    context_object_name = 'events'
    paginate_by = 5

    # Show past events of user with username in URL
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) # Class based view so requires kwargs.get to extract from URL
        return Event.objects.filter(attendees=user.student, end_time__lte=timezone.now()).order_by('-start_time')

    # Send user object of user with username in URL to template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username')) # Class based view so requires kwargs.get to extract from URL
        context['requested_user'] = user
        return context

    
    # Only allow logged in user to access view if they are not a Student
    def test_func(self):
        active_user = self.request.user
        if active_user.groups.filter(name="Admin") or active_user.groups.filter(name="Staff"):
            return True
        else:
            return False

# Authenticate Attendance by entering code into a form
@login_required
def get_attendance_auth(request):
    if request.method == 'POST': # If this is a POST request, we need to process the form's data
        form = AttendanceAuthenticateForm(request.POST) # Create a form instance and populate it with data from the request
        if form.is_valid(): # Check whether input data is valid
            user = request.user # Get logged in user
            if not user.groups.filter(name='Students').exists(): # Student / admin user does not need to authenticate attendance
                print("Unauthorised")
                messages.error(request, f'Unauthorised')
                return redirect('main-home')
            auth_hash = form.cleaned_data['auth_hash'] # Extract auth hash from form data. Type = UUID
            if Event.objects.filter(auth_uuid=auth_hash).exists(): # Check that an event with that authentication hash actually exists
                event = Event.objects.get(auth_uuid=auth_hash)
                if event.happening_now(): # Check if event is currently happening (cannot authenticate unless event is currently happening)
                    if event.attendees.filter(user=user).exists(): # Check if the student is supposed to be attending the event
                        if Attendance.objects.filter(student=user.student, event=event).exists(): # If event already authenticated
                            print("attendance already authenticated")
                            messages.info(request, f'Attendance already authenticated')
                            return redirect(event.get_absolute_url()) # Redirect to event-detail page of authenticated event
                        else:
                            auth = Attendance.objects.create(student=user.student, event=event, auth_time=timezone.now())
                            auth.save()
                            messages.success(request, f'Attendance authenticated successfully!') # one time success message
                            print("Attendance authenticated successfully!")
                            return redirect(event.get_absolute_url()) # Redirect to event-detail page of authenticated event
                    else: 
                        print("Unauthorised auth hash")
                        messages.error(request, f'Unauthorised authentication hash') # Display one time error message - student has tried to authenticate attendance at an event they aren't supposed to be attending
                        return redirect('main-home') # If there is any kind of error, redirect back to form page
                else: 
                    print("event not happening now")
                    messages.error(request, f'Event is not happening now')
                    return redirect('main-home')
            else:
                print("invalid auth hash")
                messages.error(request, f'Invalid authentication hash')
                return redirect('main-home')
    else: # If this is a GET (or any other method), create a blank form
        form = AttendanceAuthenticateForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'main/home.html', context)


# Generate QR code (only available to staff leading the event or admin)
class GenerateQR(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Event
    template_name = 'main/event_QR.html'

    # Overrides method which handles HTTP request and returns HTTP response 
    def dispatch(self, request, *args,  **kwargs):
        event = get_object_or_404(Event, id=self.kwargs.get('pk')) # Get event object corresponding to primary key in URL
        if event.happening_now(): # QR code link is only active if the event is happening now
            return super(GenerateQR, self).dispatch(request, *args, **kwargs)
        else:
            messages.error(self.request, f'Event is not happening now') # Display one-time error message
            return redirect(event.get_absolute_url())
    
    # QR code can only be shown if the logged in user is an admin user or the staff user leading the event
    def test_func(self):
        event = get_object_or_404(Event, id=self.kwargs.get('pk')) # Get event object corresponding to primary key in URL           
        if self.request.user == event.leader.user:
            return True
        elif self.request.user.groups.filter(name='Admin').exists():
            return True
        else:
            return False


def scan_qr(request):
    context = {
        'text': 'Success!'
    }
    return render(request, 'main/scan.html', context)
