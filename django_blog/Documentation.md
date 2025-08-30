Django Blog Authentication System Documentation
Overview

This authentication system handles user registration, login, logout, and profile management using Django’s built-in authentication framework with custom enhancements:

Custom registration form (CustomUserCreationForm)

Login via username (or email if extended)

Logout with CSRF protection

Profile view with update functionality (email, bio, profile picture)

Flash messages for feedback

Authentication Features & How They Work
1. User Registration

Purpose: Allow new users to create an account.
Flow:

GET /register/ → Renders the registration form.

POST /register/ → Validates data:

If valid → creates new user → redirects to login page.

If invalid → reloads form with error messages.

Uses CustomUserCreationForm (extends UserCreationForm).

Key Code:

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/registration.html', {'form': form})

2. User Login

Purpose: Authenticate and log in an existing user.
Flow:

GET /login/ → Renders login page.

POST /login/:

Extracts identifier (username or email) and password.

Uses authenticate() to validate credentials.

If valid → logs in user → redirects to profile page.

If invalid → shows error message.

Key Code:

def login_view(request):
    identifier = ""
    if request.method == "POST":
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        user = authenticate(request, username=identifier, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('blog:user_profile')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    return render(request, 'blog/login.html', {'identifier': identifier})

3. Logout

Purpose: End user session securely.
Flow:

POST /logout/:

Calls logout(request).

Renders logout confirmation page.

Key Code:

from django.views.decorators.http import require_POST

@require_POST
def logout_view(request):
    logout(request)
    return render(request, 'blog/logout.html')


Important: Logout uses POST for CSRF safety.

4. Profile Management

Purpose: Allow authenticated users to view and update their profile.
Flow:

GET /profile/ → Shows user details + update form.

POST /profile/ → Updates user email, bio, and profile picture.

Key Code:

@login_required
def profile_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

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

Security Measures

CSRF Protection on all forms.

@login_required on profile view.

Logout restricted to POST requests.

User-bound form instances prevent tampering (cannot edit another user’s data).

Password validation enforced by Django’s built-in validators.

Session security features: SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE (in production).

Testing Instructions
Manual Testing

Perform these steps in a browser or via tools like Postman:

Registration

Navigate to /register/.

Fill form with:

Valid data → should redirect to login.

Invalid data (mismatched passwords) → should show error.

Login

Navigate to /login/.

Enter valid credentials → should redirect to profile.

Enter invalid credentials → should show error message.

Logout

Log in, then submit logout form.

Confirm session ends (profile page redirects to login).

Profile Update

Log in and go to /profile/.

Change email, upload an image, and submit.

Check success message and updated data.

Try accessing profile as anonymous → should redirect to login.