from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post # import post model from DB (. because this file and models.py are in the same directory)

# Create your views here.

# NO LONGER USED BUT KEPT FOR REFERENCE
# Take in a HTTP request as input and return a HTTP response which displays 
def home(request):
    # all relevant data stored in context dictionary (contains posts which is a list of dictionaries)
    context = {
        # key = posts
        'posts': Post.objects.all() # load posts into home view from Post model
    }
    # render: (request, path of template in templates dir, context - passes data into template)
    return render(request, 'main/home.html', context)

# Class based view for homepage (inherits from ListView type)
class PostListView(ListView):
    model = Post
    template_name = 'main/home.html' # Override the template to search for, default = <app>/<model>_<viewtype>.html (main/post_list.html)
    context_object_name = 'posts' # Specify what variable name the objects in the list should be called, so they are looped as they were when using the function based view in the template
    ordering = ['-date_posted'] # Displays posts in chronological order, with most recent post on the top
    paginate_by = 5 # number of posts to display per page

# Display posts written by specific user passed in URL
class UserPostListView(ListView):
    model = Post
    template_name = 'main/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) # extract username from URL
        return Post.objects.filter(author=user).order_by('-date_posted') # need to override this too

# Post details (inherits from DetailView type)
class PostDetailView(DetailView):
    model = Post

# Create a new post (inherits first from LoginRequiredMixin and then from CreateView). This requires the user to log in before they can create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # set author of post to current logged in user
    def form_valid(self, form):
        # set the author of the new post instance as the currently logged in user
        form.instance.author = self.request.user
        return super().form_valid(form) # this is a method on the parent class that would've been performed anyway, but since we're overriding the method we need to specify it manually


# Update post - almost exactly the same as creating a post but requires logged in user to be the post author (inherits UserPassesTestMixim)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # validate form
    def form_valid(self, form):
        # set the author of the new post instance as the currently logged in user
        form.instance.author = self.request.user
        return super().form_valid(form) # this is a method on the parent class that would've been performed anyway, but since we're overriding the method we need to specify it manually

    # Function run by UserPassesTestMixin to ensure the logged in user is the same as the post author before allowing them to update the post
    def test_func(self):
        post = self.get_object() # method returns current post instance
        if self.request.user == post.author:
            return True # pass test if logged in user = post author
        return False # else fail test - logged in user cannot update post


# Delete post - also requires user to be logged in and the logged in user to be the post author
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    # make sure logged in user is post author
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    success_url = '/'


def about(request):
    return render(request, 'main/about.html', {'title': 'About'})
