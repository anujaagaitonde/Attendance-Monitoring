from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path(path name, path route (view), route name)
    path('', views.home, name='main-home'),
]