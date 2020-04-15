from django.contrib import admin
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views

urlpatterns = [
    # path name, path route (view), route name
    path('', PostListView.as_view(), name='main-home'), # empty path within /main app redirects to homepage of main. Refer to this routing using name 'main-home'
    # Each post is supposed to have a unique url 'path/post_no'
    # The <pk> variable extracts the primary key from the post, and tells Django that we expect this primary key (or whatever follows post/) to be an integer value. This is appended to the URL so it can be used directly by the class based view
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # vbl name pk was used because this is what DetailView expects by default
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), # pk also needed because we need to know which post to update
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='main-about'),
]