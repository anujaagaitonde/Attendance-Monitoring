from django.contrib import admin
from django.urls import path
from . import views
from .views import EventDetailView, EventListView, PastEventListView, UserEventListView, UserPastEventListView, GenerateQR, StaffRegisterListView, StaffCompletedRegisterListView

urlpatterns = [
    # path(path name, path route (view), route name)
    path('', views.get_attendance_auth, name='main-home'), # Scanner to enter auth hash
    path('events/', EventListView.as_view(), name='my-events'), # Default = upcoming events
    path('events/past/', PastEventListView.as_view(), name='my-past-events'),
    path('registers/', StaffRegisterListView.as_view(), name='outstanding-registers'),
    path('registers/completed/', StaffCompletedRegisterListView.as_view(), name='completed-registers'),
    path('<str:username>/events/', UserEventListView.as_view(), name='user-events'),
    path('<str:username>/events/past/', UserPastEventListView.as_view(), name='user-past-events'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'), # DetailView by default expects the pk of the object's whose details are to be shown to be part of the URL path
    path('event/<int:pk>/QR/', GenerateQR.as_view(), name='event-QR'), # Display QR code for event
    path('event/<int:pk>/register/', views.take_register, name='event-register'), # Electronic register for each event
]