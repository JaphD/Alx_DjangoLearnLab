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
    return render(request, 'blog/register.html', {'form': form})

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


Blog Post Management (CRUD) — Feature Documentation
1. Overview

This feature allows users to create, read, update, and delete blog posts in the Django Blog project.

Post model: Stores blog post data (title, content, published_date, author).

CRUD operations: Implemented using Django class-based views (CBVs).

Templates: Provides a user-friendly interface for all operations.

Permissions: Ensures only authorized users can create/edit/delete posts.

2. Models
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


Notes:

author links each post to a registered user.

get_absolute_url() is used to redirect users after creating/updating a post.

3. Views

PostListView: Displays all blog posts to any user.

PostDetailView: Displays a single post. Public access.

PostCreateView: Allows authenticated users to create a new post. Author is set automatically.

PostUpdateView: Only the author can edit their own posts.

PostDeleteView: Only the author can delete their own posts.

Example: Create View

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

4. URLs
Operation	URL Pattern	View Name
List posts	/posts/	post_list
Post detail	/posts/<pk>/	post_detail
Create new post	/posts/new/	post_create
Edit post	/posts/<pk>/edit/	post_update
Delete post	/posts/<pk>/delete/	post_delete
5. Templates

post_list.html – shows all posts with title and snippet.

post_detail.html – full post view with edit/delete options if author.

post_form.html – used for create and update posts.

post_confirm_delete.html – confirmation page for deletion.

Notes:

Templates include CSRF tokens and Django messages.

Links for editing/deleting only appear for the post author.

6. Permissions & Access Control

Create post: Only authenticated users.

Update/Delete post: Only the post author.

View posts (list/detail): Public (no login required).

Enforced via LoginRequiredMixin and UserPassesTestMixin.

7. How to Use

View posts: Navigate to /posts/.

Read post: Click on a post title to view details.

Create post:

Log in.

Go to /posts/new/.

Fill in title & content, submit.

Edit post:

Navigate to your post’s detail page.

Click Edit (visible only to author).

Delete post:

Navigate to your post’s detail page.

Click Delete → Confirm deletion.

8. Testing Guidelines

Manual Testing:

Try creating a post as a logged-in user.

Attempt editing/deleting as a different user (should be blocked).

Check that posts are visible in list and detail views for all users.


Comment System — System Documentation

This document describes how the comment system works in the blog app: how comments are stored, how users add/edit/delete them, visibility and permissions, how to test, and common implementation notes.

Summary

Comments are attached to Post entries (many comments → one post).

Authenticated users can create, edit, and delete their own comments.

Anyone (authenticated or not) can read comments on a post’s detail page.

The code uses a Comment model, a CommentForm, class-based views (Create/Update/Delete), and templates integrated into the post_detail template.

Model (data)
# blog/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:post_detail', kwargs={'pk': self.post.pk})


Notes

related_name='comments' → access via post.comments.all().

get_absolute_url() redirects to the post detail after comment creation/edit/delete.

Run migrations after adding this model:

python manage.py makemigrations blog
python manage.py migrate

Form
# blog/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }
        labels = {'content': ''}


Validation & suggestions

Add server-side validation if you want (e.g., min/max length).

Keep the form minimal; author and post are set in the view (never from user input).

Views (behavior & code)

Use class-based views with permissions:

# blog/views.py (snippets)
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Comment, Post
from .forms import CommentForm

# Add comment - typically used for POST from post_detail form
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    # template_name not required if form is posted from post_detail, but available if you want a standalone page
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']   # link to Post by id from URL
        return super().form_valid(form)

# Edit comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

# Delete comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        return self.get_object().author == self.request.user

# Ensure PostDetailView adds a blank CommentForm to the context so post_detail.html can render the inline form
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .forms import CommentForm
        context['comment_form'] = CommentForm()
        return context


Behavior notes

CommentCreateView expects post_id in URL kwargs (/posts/<post_id>/comments/new/).

LoginRequiredMixin ensures only logged-in users can create/edit/delete.

UserPassesTestMixin ensures only the comment author can edit/delete.

URLs

Add the comment routes to blog/urls.py:

from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns += [
    path('posts/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]


URL design rationale

posts/<post_id>/comments/new/ is intuitive for creating a comment for a specific post.

Editing/deleting uses the comment pk because those operations act on the comment resource.

Templates / Integration
In post_detail.html (integrated)

Include the post content first, then the comments section and the inline form:

<!-- Post content (title, content, meta) -->
<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>
<p>By {{ post.author }}</p>

<hr>

<h2>Comments</h2>
{% for comment in post.comments.all %}
  <div class="comment">
    <p><strong>{{ comment.author.username }}</strong> &middot; {{ comment.created_at|date:"M j, Y H:i" }}</p>
    <p>{{ comment.content|linebreaks }}</p>
    {% if user == comment.author %}
      <p>
        <a href="{% url 'blog:comment_update' comment.pk %}">Edit</a> |
        <a href="{% url 'blog:comment_delete' comment.pk %}">Delete</a>
      </p>
    {% endif %}
  </div>
{% empty %}
  <p>No comments yet.</p>
{% endfor %}

{% if user.is_authenticated %}
  <h3>Add a comment</h3>
  <form method="post" action="{% url 'blog:comment_create' post.pk %}">
    {% csrf_token %}
    {{ comment_form.as_p }}
    <button type="submit">Post Comment</button>
  </form>
{% else %}
  <p><a href="{% url 'blog:login' %}">Login</a> to post a comment.</p>
{% endif %}

comment_form.html (standalone create/edit):
{% extends "blog/base.html" %}
{% block content %}
  <h2>{% if form.instance.pk %}Edit Comment{% else %}Add Comment{% endif %}</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
  </form>
  <a href="{{ form.instance.post.get_absolute_url }}">Cancel</a>
{% endblock %}

comment_confirm_delete.html:
{% extends "blog/base.html" %}
{% block content %}
  <h2>Delete Comment</h2>
  <p>Are you sure you want to delete this comment?</p>
  <p>{{ object.content }}</p>
  <form method="post">
    {% csrf_token %}
    <button type="submit">Yes, delete</button>
  </form>
  <a href="{{ object.post.get_absolute_url }}">Cancel</a>
{% endblock %}


Important

Always include {% csrf_token %} in comment forms.

The inline form posts to comment_create URL; the create view handles the POST and redirects back to the post.

Permissions & Visibility (Rules)

Read visibility: All comments for a post are displayed on the post detail page: post.comments.all(). (If you later add moderation/drafts, filter accordingly.)

Create: Only authenticated users can create comments (LoginRequiredMixin). Attempting to POST while anonymous results in a redirect to login.

Edit/Delete: Only the comment’s author may edit or delete it. This is enforced by UserPassesTestMixin with test_func checking comment.author == request.user.

CSRF: All comment form submissions must include CSRF tokens (Django templates do this via {% csrf_token %}).

Data integrity: post and author are set server-side (never from user input).

Security & Validation

Escape output: Template output uses {{ comment.content }} (Django auto-escapes). If you render HTML, sanitize it to avoid XSS.

CSRF protection: Forms include CSRf tokens, as required.

Rate limiting / spam: Not included by default — consider throttling or using a 3rd-party service to prevent abuse.

Input validation: Add validation (min/max length) in CommentForm if required.

Soft delete: If you want recoverable comments, implement a is_deleted boolean instead of hard delete.

Admin

Register Comment in blog/admin.py:

from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    search_fields = ('author__username', 'content')

Testing
Manual tests

Open a post detail (e.g., /posts/1/) as an anonymous user: comments must be visible, inline form replaced with link to login.

Login, visit the same post, fill inline comment form, submit — you should be redirected back to the post and see the new comment.

As the comment author, click Edit → modify and save → change persists.

As the comment author, click Delete → confirm → comment removed and redirected back to post.

As a different authenticated user, try to access the edit/delete URLs for someone else’s comment → should be blocked/redirected.