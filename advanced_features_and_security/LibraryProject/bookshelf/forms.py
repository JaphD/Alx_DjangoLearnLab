from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_photo')

        widgets = {
                'date_of_birth': forms.DateInput(
                    attrs={'type': 'date'}  # This tells the browser to show a date picker
                )
            }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_photo')

        widgets = {
                'date_of_birth': forms.DateInput(
                    attrs={'type': 'date'}  # This tells the browser to show a date picker
                )
            }