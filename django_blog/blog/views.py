from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages  # <-- Add this import
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.decorators import login_required

# Renders the main blog homepage
def blog_view(request):
    return render(request, 'blog/base.html', {}) 

# Handles user registration
def register_view(request):
    if request.method == "POST":
        # Bind form with POST data
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save new user and redirect to login page
            form.save()
            return redirect('blog:login')
        else:
            # Add error message if form is invalid
            messages.error(request, "Please correct the errors below.")
    else:
        # Display empty registration form
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Handles user login
def login_view(request):
    # Initialize identifier to avoid NameError if GET request
    identifier = ""
    if request.method == "POST":
        # Get identifier (username or email) and password from POST data
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        # Attempt to authenticate user
        user = authenticate(request, username=identifier, password=password)
        if user is not None and user.is_active:
            # Log in and redirect to profile page
            login(request, user)
            messages.success(request, "Login successful!")  # Confirmation message
            return redirect('blog:user_profile')
        else:
            # Add error message for invalid credentials
            messages.error(request, "Invalid credentials. Please try again.")

    # Render login page, passing back identifier for convenience
    return render(request, 'blog/login.html', {'identifier': identifier})

# Logs out the user and renders logout confirmation page
def logout_view(request):
    logout(request)
    return render(request, 'blog/logout.html')

# Renders the user profile page; requires authentication
def profile_view(request):
    user = request.user
    # Get or create profile for user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('blog:user_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'blog/user_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# List View - shows all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # custom template
    context_object_name = 'posts'
    ordering = ['-published_date']

# Detail View - single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# Create View - only authenticated users
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Redirect to the detail page of the newly created post
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

# Update View - only post author can edit
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete View - only post author can delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author