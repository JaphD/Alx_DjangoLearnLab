from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
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
        # Display empty registration form
        form = CustomUserCreationForm()
    return render(request, 'blog/registration.html', {'form': form})

# Handles user login
def login_view(request):
    # Initialize identifier to avoid NameError if GET request
    identifier = ""
    if request.method == "POST":
        # Get identifier (username or email) and password from POST data
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=identifier, password=password)
        if user is not None and user.is_active:
            # Log in and redirect to profile page
            login(request, user)
            return redirect('blog:user_profile')
        
    # Render login page, passing back identifier for convenience
    return render(request, 'blog/login.html', {'identifier': identifier})

# Logs out the user and renders logout confirmation page
def logout_view(request):
    logout(request)
    return render(request, 'blog/logout.html')

# Renders the user profile page; requires authentication
@login_required
def profile_view(request):
    return render(request, 'blog/user_profile.html')