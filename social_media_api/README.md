Social Media API Documentation

Overview
This document provides a comprehensive guide to the Social Media API, a RESTful service built with Django and Django REST Framework. The API enables core social media functionalities, including user authentication, profile management, and the ability for users to create and interact with posts and comments. The system uses token-based authentication to secure endpoints and enforces permissions to protect user data.

Component	Technology	Description
Framework	Django, Django REST Framework	The core backend and API development framework.
Authentication	TokenAuthentication	A secure method where users exchange credentials for a unique, secret key to access protected resources.
Database	SQLite (default)	A lightweight, file-based database for development.
URL Routing	DRF Routers & Nested Routers	Automatically generates URL patterns for efficient endpoint management, including hierarchical routes for comments.
Setup and Configuration
To get the API running locally, follow these steps:

Install Dependencies: Make sure you have the required libraries.

Bash

pip install django djangorestframework django-filter drf-nested-routers
Configure settings.py: Update your project's settings.py to include the new apps and configurations.

Python

INSTALLED_APPS = [
    # ... existing Django apps
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'rest_framework_nested',
    'accounts',
    'posts',
]
AUTH_USER_MODEL = 'accounts.User'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication'],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend', 'rest_framework.filters.SearchFilter'],
}
Apply Migrations: This will create the necessary database tables for all apps, including accounts and posts.

Bash

python manage.py makemigrations
python manage.py migrate
Run the Server: Start the local development server to access the API at http://localhost:8000.

Bash

python manage.py runserver
Authentication Endpoints
These endpoints are used to manage user authentication and profiles. Endpoints that require authentication must have the header Authorization: Token <your_token>.

POST /api/accounts/register/ - Register a New User
Permissions: AllowAny

Description: Creates a new user account and automatically generates a token for immediate use.

Body:

JSON

{
  "username": "jane_doe",
  "email": "jane@example.com",
  "password": "strong-password",
  "bio": "I'm a developer building a social media app."
}
Response (201 Created): Returns the user's data and the authentication token.

JSON

{
  "user": { "id": 1, "username": "jane_doe", "email": "jane@example.com", ... },
  "token": "aeb49644f1a659797ed81bf3e9330b6442b1f094"
}
POST /api/accounts/login/ - Authenticate a User
Permissions: AllowAny

Description: Authenticates a user with a username and password and returns their existing token.

Body:

JSON

{
  "username": "jane_doe",
  "password": "strong-password"
}
Response (200 OK): Returns the user's data and their token.

GET/PATCH /api/accounts/profile/ - Manage User Profile
Permissions: IsAuthenticated

Description: Retrieves or updates the currently authenticated user's profile information.

Body (PATCH example):

JSON

{
  "bio": "A passionate developer and API enthusiast."
}
Posts and Comments Endpoints
These endpoints manage user-generated content. All are protected and require a valid authentication token. The IsOwnerOrReadOnly permission ensures users can only modify their own content.

GET /api/posts/ - List All Posts
Permissions: IsAuthenticated

Description: Fetches a paginated list of all posts.

Query Parameters:

?search=hello: Searches posts where the title or content contains "hello".

?author=1: Filters posts to show only those by the user with ID 1.

Response (200 OK): A paginated list of posts, including nested comments for each post.

POST /api/posts/ - Create a Post
Permissions: IsAuthenticated

Description: Creates a new post for the authenticated user.

Body:

JSON

{
  "title": "My First Post",
  "content": "This is a great day for building APIs."
}
Response (201 Created): Returns the newly created post object.

GET/PUT/PATCH/DELETE /api/posts/<id>/ - Manage a Single Post
Permissions: IsAuthenticated

Description: Allows retrieval, full update, partial update, or deletion of a specific post.

Rules: PUT, PATCH, and DELETE requests are only allowed if the authenticated user is the author of the post.

GET /api/posts/<post_id>/comments/ - List Comments
Permissions: IsAuthenticated

Description: Fetches all comments associated with a specific post.

POST /api/posts/<post_id>/comments/ - Create a Comment
Permissions: IsAuthenticated

Description: Creates a new comment on a specific post. The comment is automatically linked to the authenticated user.

Body:

JSON

{
  "content": "I love this post!"
}
Response (201 Created): Returns the newly created comment object.

GET/PUT/PATCH/DELETE /api/posts/<post_id>/comments/<id>/ - Manage a Single Comment
Permissions: IsAuthenticated

Description: Allows retrieval, update, or deletion of a specific comment on a specific post.

Rules: PUT, PATCH, and DELETE requests are only allowed if the authenticated user is the author of the comment.