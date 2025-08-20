from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def home_view(request):
    return render(request, 'base.html', {'year': now().year})

# User register
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'bookshelf/register.html', {'form': form})


# User Login
def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get('identifier')  # email OR username
        password = request.POST.get('password')

        user = authenticate(request, username=identifier, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('bookshelf:profile')
        
    return render(request, 'bookshelf/login.html', {'identifier': identifier})


# User Logout → Redirect to logout.html
def logout_view(request):
    logout(request)
    return render(request, 'bookshelf/logout.html')

@login_required
def profile_view(request):
    return render(request, 'bookshelf/profile.html')