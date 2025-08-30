from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile, Post, Comment, Tag
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class PostForm(forms.ModelForm):
    # user-friendly field to add tags as comma-separated names
    tags = forms.CharField(
        required=False,
        help_text='Comma-separated tags (e.g. django, python, tutorial).',
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content']

    def clean_tags(self):
        raw = self.cleaned_data.get('tags', '')
        # Normalize: split by comma, strip whitespace, remove empties, lowercase unique
        names = [t.strip() for t in raw.split(',') if t.strip()]
        # optionally enforce a max number or max length per tag
        unique_names = []
        for n in names:
            if n.lower() not in [u.lower() for u in unique_names]:
                unique_names.append(n)
        return unique_names

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }
        labels = {
            'content': '',
        }
