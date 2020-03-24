from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path name, path route
    path('', views.home, name='main-home'), # empty path within /main app redirects to homepage of main. Refer to this routing using name 'main-home'
    path('about/', views.about, name='main-about'),
]