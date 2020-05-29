from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event, Attendance, Verification
from .forms import AttendanceAuthenticateForm, AttendanceVerificationForm
from django.utils import timezone
from django.conf import settings
from django.forms import formset_factory
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.

# View for homepage. NO LONGER USED BUT KEPT FOR REFERENCE
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
                messages.error(request, f'Unauthorised')
                return redirect('main-home')
            auth_hash = form.cleaned_data['auth_hash'] # Extract auth hash from form data. Type = UUID
            if Event.objects.filter(auth_uuid=auth_hash).exists(): # Check that an event with that authentication hash actually exists
                event = Event.objects.get(auth_uuid=auth_hash)
                if event.happening_now(): # Check if event is currently happening (cannot authenticate unless event is currently happening)
                    if event.attendees.filter(user=user).exists(): # Check if the student is supposed to be attending the event
                        if Attendance.objects.filter(student=user.student, event=event).exists(): # If event already authenticated
                            messages.info(request, f'Attendance already authenticated')
                            return redirect(event.get_absolute_url()) # Redirect to event-detail page of authenticated event
                        else:
                            auth = Attendance.objects.create(student=user.student, event=event, auth_time=timezone.now())
                            auth.save()
                            event.register_taken = False # Need to retake register if another student has authenticated their attendance
                            event.save()
                            messages.success(request, f'Attendance authenticated successfully!') # one time success message
                            return redirect(event.get_absolute_url()) # Redirect to event-detail page of authenticated event
                    else: 
                        messages.error(request, f'Unauthorised authentication hash') # Display one time error message - student has tried to authenticate attendance at an event they aren't supposed to be attending
                        return redirect('main-home') # If there is any kind of error, redirect back to form page
                else: 
                    messages.error(request, f'Event is not happening now')
                    return redirect('main-home')
            else:
                messages.error(request, f'Invalid authentication hash')
                return redirect('main-home')
        else: 
            messages.error(request, f'Error Decoding QR Code')
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

# Generate electronic register for staff members to verify who was present at their event
@login_required
def take_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    student_auths = Attendance.objects.filter(event=event).order_by('student__user__first_name', 'student__user__last_name') # Extract queryset of authentications, ordered by student's first name
    count = student_auths.count()
    register_formset = formset_factory(AttendanceVerificationForm, extra=count) # Create formset

    # Create list of dictionaries which contains previously submitted register information (if any)
    initial = []
    for auth in student_auths:
        initial.append(
            {'mark_attendance': Verification.objects.filter(student=auth.student, event=event).exists()}
        )

    # Only staff event leader or admin user should be able to access register
    if event.leader.user == request.user or request.user.groups.filter(name="Admin").exists():
        if event.event_type == 'LE': # Register does not need to be taken at lectures
            messages.info(request, f'Register does not need to be taken at a lecture')
            return redirect(event.get_absolute_url())
        else: # Tutorials, study groups and exams require a register to be taken
            if event.started(): # Only allow register to be taken if event has started
                if request.method == 'POST': # If the request is a POST request, process the form's data
                    formset = register_formset(request.POST)
                    student_list = zip(formset, student_auths)
                    if formset.is_valid():
                        event.register_taken = True # Mark that a register has been taken for this event
                        event.save()
                        for form, auth in student_list:
                            student = auth.student
                            mark = form.cleaned_data.get('mark_attendance') # Obtain data submitted from each form in formset
                            if mark == True:
                                if Verification.objects.filter(student=student, event=event).exists(): # Verification already exists for this particular event and student
                                    verification = Verification.objects.get(student=student, event=event)
                                    verification.verification_time = timezone.now() # Edit that verification object
                                else:
                                    verification = Verification.objects.create(verification_time=timezone.now(), event=event, student=student) # Create Verification object
                                verification.save()
                            else:
                                if Verification.objects.filter(student=student, event=event).exists(): # Verification already exists for this particular event and student
                                    verification = Verification.objects.get(student=student, event=event)
                                    verification.delete() # Delete verification object if student was not present at that event
                        messages.success(request, f'Register saved successfully!')
                        return redirect(event.get_absolute_url())
                else: # If this is a GET (or any other) request, create a blank formset
                    student_list = zip(register_formset(initial=initial), student_auths) # Initialise formset with previous register data (if any)
            else: # Event hasn't started yet
                messages.error(request, f'Event has not started yet')
                return redirect(event.get_absolute_url())
        
        context = {
                'formset': register_formset(),
                'list': student_list,
                'event': event,
        }

        return render(request, 'main/take_register.html', context)

    else: # Logged in user is not an admin user / staff leader
        return HttpResponse(status=403)
    

# List events with outstanding registers for a staff leader
class StaffRegisterListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'main/register_list.html' # Override the template to search for, default = <app>/<model>_<viewtype>.html (main/event_list.html)
    context_object_name = 'events' # Specify what variable name the objects in the list should be called, so they are looped as they were when using the function based view in the template
    paginate_by = 5 # number of events to display per page

    # Override default get_queryset to obtain a more specific queryset to be listed on the page
    # Only view events with outstanding registers led by the logged in user (staff leader)
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Staff').exists():
            return Event.objects.filter(leader=user.staff, start_time__lte=timezone.now(), register_taken=False).exclude(event_type="LE").order_by('-start_time')
        elif user.groups.filter(name='Admin').exists(): # Admin users can view all events
            return Event.objects.filter(start_time__lte=timezone.now(), register_taken=False).exclude(event_type="LE").order_by('-start_time')
    
    # Test function for UserPassesTest mixin
    def test_func(self):
        user = self.request.user
        if user.groups.filter(name="Admin") or user.groups.filter(name="Staff"):
            return True
        else:
            return False

# List events with completed registers for a staff leader
class StaffCompletedRegisterListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'main/past_register_list.html' # Override the template to search for, default = <app>/<model>_<viewtype>.html (main/event_list.html)
    context_object_name = 'events' # Specify what variable name the objects in the list should be called, so they are looped as they were when using the function based view in the template
    paginate_by = 5 # number of events to display per page

    # Override default get_queryset to obtain a more specific queryset to be listed on the page
    # Only view events with outstanding registers led by the logged in user (staff leader)
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Staff').exists():
            return Event.objects.filter(leader=user.staff, start_time__lte=timezone.now(), register_taken=True).exclude(event_type="LE").order_by('-start_time')
        elif user.groups.filter(name='Admin').exists(): # Admin users can view all events
            return Event.objects.filter(start_time__lte=timezone.now(), register_taken=True).exclude(event_type="LE").order_by('-start_time')
    
    # Test function for UserPassesTest mixin
    def test_func(self):
        user = self.request.user
        if user.groups.filter(name="Admin") or user.groups.filter(name="Staff"):
            return True
        else:
            return False


# Show attendance record for the past two weeks for each student
def attendance_record(request, username):
    user = get_object_or_404(User, username=username)

    # Only staff / admin can view attendance record of other students. Students can view their own attendance record
    if request.user.groups.filter(name="Admin").exists() or request.user.groups.filter(name="Staff").exists() or request.user == user:            
        
        # Only students will have an attendance record
        if user.groups.filter(name="Students"):
            cutoff = timezone.now() - timezone.timedelta(days=14) # set 2 week time threshold

            # Calculate attendance information
            # Lectures
            lec_count = Event.objects.filter(event_type="LE", attendees=user.student, start_time__gt=cutoff).count()
            lec_auths_count = Attendance.objects.filter(student=user.student, event__event_type="LE", event__start_time__gt=cutoff).count()
            if not lec_count == 0:
                perc_lec_auths = round(lec_auths_count / lec_count * 100, 1) # Calculate lecture attendance as a % of lectures authenticated
            else:
                perc_lec_auths = 'N/A'
            
            lec_context = {
                'num': lec_count,
                'auths_count': lec_auths_count,
                'perc_auths': perc_lec_auths
            }

            # Tutorials
            tut_count = Event.objects.filter(event_type="TU", attendees=user.student, start_time__gt=cutoff).count()
            tut_auths_count = Attendance.objects.filter(student=user.student, event__event_type="TU", event__start_time__gt=cutoff).count()
            tut_regs_count = Verification.objects.filter(student=user.student, event__event_type="TU", event__start_time__gt=cutoff).count()
            if not tut_count == 0:
                perc_tut_auths = round(tut_auths_count / tut_count * 100, 1) # Calculate tutorial attendance as a % of tutorials authenticated
                perc_tut_regs = round(tut_regs_count / tut_count * 100, 1) # Calculate tutorial attendance as a % of tutorials registered by staff
            else:
                perc_tut_auths = 'N/A'
                perc_tut_regs = 'N/A'

            tut_context = {
                'num': tut_count,
                'auths_count': tut_auths_count,
                'regs_count': tut_regs_count,
                'perc_auths': perc_tut_auths,
                'perc_regs': perc_tut_regs
            }

            # Exams
            exam_count = Event.objects.filter(event_type="EX", attendees=user.student, start_time__gt=cutoff).count()
            exam_auths_count = Attendance.objects.filter(student=user.student, event__event_type="EX", event__start_time__gt=cutoff).count()
            exam_regs_count = Verification.objects.filter(student=user.student, event__event_type="EX", event__start_time__gt=cutoff).count()
            if not exam_count == 0:
                perc_exam_auths = round(exam_auths_count / exam_count * 100, 1) # Calculate exam attendance as a % of exams authenticated, rounded to 1 dp
                perc_exam_regs = round(exam_regs_count / exam_count * 100, 1) # Calculate exam attendance as a % of exams registered by staff
            else:
                perc_exam_auths = 'N/A'
                perc_exam_regs = 'N/A'

            exam_context = {
                'num': exam_count,
                'auths_count': exam_auths_count,
                'regs_count': exam_regs_count,
                'perc_auths': perc_exam_auths,
                'perc_regs': perc_exam_regs
            }

            # Study Groups / Lab sessions
            sg_count = Event.objects.filter(event_type="SG", attendees=user.student, start_time__gt=cutoff).count()
            sg_auths_count = Attendance.objects.filter(student=user.student, event__event_type="SG", event__start_time__gt=cutoff).count()
            sg_regs_count = Verification.objects.filter(student=user.student, event__event_type="SG", event__start_time__gt=cutoff).count()
            if not sg_count == 0:
                perc_sg_auths = round(sg_auths_count / sg_count * 100, 1) # Calculate study group attendance as a % of study groups authenticated
                perc_sg_regs = round(sg_regs_count / sg_count * 100, 1) # Calculate exam study group as a % of study groups registered by staff
            else:
                perc_sg_auths = 'N/A'
                perc_sg_regs = 'N/A'
            
            sg_context = {
                'num': sg_count,
                'auths_count': sg_auths_count,
                'regs_count': sg_regs_count,
                'perc_auths': perc_sg_auths,
                'perc_regs': perc_sg_regs
            }

            # Overall
            event_count_auth = lec_count + tut_count + exam_count + sg_count
            event_count_regs = tut_count + exam_count + sg_count # Lectures are not verified by staff members
            auths_count = lec_auths_count + tut_auths_count + exam_auths_count + sg_auths_count
            regs_count = tut_regs_count + exam_regs_count + sg_regs_count
            if not event_count_auth == 0:
                perc_auths = round(auths_count / event_count_auth * 100, 1)
            else:
                perc_auths = 'N/A'
            if not event_count_regs == 0:
                perc_regs = round(regs_count / event_count_regs * 100, 1)
            else:
                perc_regs = 'N/A'

            total_context = {
                'num_auth': event_count_auth,
                'num_reg': event_count_regs,
                'auths_count': auths_count,
                'regs_count': regs_count,
                'perc_auths': perc_auths,
                'perc_regs': perc_regs
            }

            context = {
                'requested_user': user,
                'lec': lec_context,
                'tut': tut_context,
                'exam': exam_context,
                'sg': sg_context,
                'total': total_context
            }

            return render(request, 'main/attendance_record.html', context)
                        
        else:
            return HttpResponse(status=404) # 404 = Page not found (attendance record only exists if the requested user is a student)
    else:
        return HttpResponse(status=403)


# Show attendance record for all time
def attendance_record_all_time(request, username):
    user = get_object_or_404(User, username=username)

    # Only staff / admin can view attendance record of other students. Students can view their own attendance record
    if request.user.groups.filter(name="Admin").exists() or request.user.groups.filter(name="Staff").exists() or request.user == user:            
        
        # Only students will have an attendance record
        if user.groups.filter(name="Students"):
            # Calculate attendance information
            # Lectures
            lec_count = Event.objects.filter(event_type="LE", attendees=user.student).count()
            lec_auths_count = Attendance.objects.filter(student=user.student, event__event_type="LE").count()
            if not lec_count == 0:
                perc_lec_auths = round(lec_auths_count / lec_count * 100, 1) # Calculate lecture attendance as a % of lectures authenticated
            else:
                perc_lec_auths = 'N/A'
            
            lec_context = {
                'num': lec_count,
                'auths_count': lec_auths_count,
                'perc_auths': perc_lec_auths
            }

            # Tutorials
            tut_count = Event.objects.filter(event_type="TU", attendees=user.student).count()
            tut_auths_count = Attendance.objects.filter(student=user.student, event__event_type="TU").count()
            tut_regs_count = Verification.objects.filter(student=user.student, event__event_type="TU").count()
            if not tut_count == 0:
                perc_tut_auths = round(tut_auths_count / tut_count * 100, 1) # Calculate tutorial attendance as a % of tutorials authenticated
                perc_tut_regs = round(tut_regs_count / tut_count * 100, 1) # Calculate tutorial attendance as a % of tutorials registered by staff
            else:
                perc_tut_auths = 'N/A'
                perc_tut_regs = 'N/A'

            tut_context = {
                'num': tut_count,
                'auths_count': tut_auths_count,
                'regs_count': tut_regs_count,
                'perc_auths': perc_tut_auths,
                'perc_regs': perc_tut_regs
            }

            # Exams
            exam_count = Event.objects.filter(event_type="EX", attendees=user.student).count()
            exam_auths_count = Attendance.objects.filter(student=user.student, event__event_type="EX").count()
            exam_regs_count = Verification.objects.filter(student=user.student, event__event_type="EX").count()
            if not exam_count == 0:
                perc_exam_auths = round(exam_auths_count / exam_count * 100, 1) # Calculate exam attendance as a % of exams authenticated, rounded to 1 dp
                perc_exam_regs = round(exam_regs_count / exam_count * 100, 1) # Calculate exam attendance as a % of exams registered by staff
            else:
                perc_exam_auths = 'N/A'
                perc_exam_regs = 'N/A'

            exam_context = {
                'num': exam_count,
                'auths_count': exam_auths_count,
                'regs_count': exam_regs_count,
                'perc_auths': perc_exam_auths,
                'perc_regs': perc_exam_regs
            }

            # Study Groups / Lab sessions
            sg_count = Event.objects.filter(event_type="SG", attendees=user.student).count()
            sg_auths_count = Attendance.objects.filter(student=user.student, event__event_type="SG").count()
            sg_regs_count = Verification.objects.filter(student=user.student, event__event_type="SG").count()
            if not sg_count == 0:
                perc_sg_auths = round(sg_auths_count / sg_count * 100, 1) # Calculate study group attendance as a % of study groups authenticated
                perc_sg_regs = round(sg_regs_count / sg_count * 100, 1) # Calculate exam study group as a % of study groups registered by staff
            else:
                perc_sg_auths = 'N/A'
                perc_sg_regs = 'N/A'
            
            sg_context = {
                'num': sg_count,
                'auths_count': sg_auths_count,
                'regs_count': sg_regs_count,
                'perc_auths': perc_sg_auths,
                'perc_regs': perc_sg_regs
            }

            # Overall
            event_count_auth = lec_count + tut_count + exam_count + sg_count
            event_count_regs = tut_count + exam_count + sg_count # Lectures are not verified by staff members
            auths_count = lec_auths_count + tut_auths_count + exam_auths_count + sg_auths_count
            regs_count = tut_regs_count + exam_regs_count + sg_regs_count
            if not event_count_auth == 0:
                perc_auths = round(auths_count / event_count_auth * 100, 1)
            else:
                perc_auths = 'N/A'
            if not event_count_regs == 0:
                perc_regs = round(regs_count / event_count_regs * 100, 1)
            else:
                perc_regs = 'N/A'

            total_context = {
                'num_auth': event_count_auth,
                'num_reg': event_count_regs,
                'auths_count': auths_count,
                'regs_count': regs_count,
                'perc_auths': perc_auths,
                'perc_regs': perc_regs
            }

            context = {
                'requested_user': user,
                'lec': lec_context,
                'tut': tut_context,
                'exam': exam_context,
                'sg': sg_context,
                'total': total_context
            }

            return render(request, 'main/attendance_record_all_time.html', context)
                        
        else:
            return HttpResponse(status=404) # 404 = Page not found (attendance record only exists if the requested user is a student)
    else:
        return HttpResponse(status=403)