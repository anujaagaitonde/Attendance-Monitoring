from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event
from django.utils import timezone

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
    
    # Only allow logged in user to access view if they are not a Student
    def test_func(self):
        active_user = self.request.user
        if active_user.groups.filter(name="Admin") or active_user.groups.filter(name="Staff"):
            return True
        else:
            return False