from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages  # <-- Add this import
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
            # Add error message if form is invalid
            messages.error(request, "Please correct the errors below.")
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
@login_required
def profile_view(request):
    return render(request, 'blog/user_profile.html')