Social Media API Documentation
Overview
This is a comprehensive guide to the Social Media API, a RESTful service built with Django and Django REST Framework. The API enables core social media functionalities, including user authentication, profile management, and the ability for users to create and interact with posts and comments. It now includes features for users to follow other users and view a personalized feed. The system uses token-based authentication to secure endpoints and enforces permissions to protect user data.

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
Authentication and User Management
The following endpoints manage user authentication, profiles, and relationships.

User Model Changes
The custom User model in accounts/models.py has been updated to include a self-referential many-to-many relationship. The followers field represents who is following the user, while the following field (created automatically by the related_name) represents the users the current user follows.

Python

class User(AbstractUser):
    # ...
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    # ...
Follow a User
Method: POST

URL: /api/accounts/follow/<int:user_id>/

Permissions: IsAuthenticated

Description: Allows the authenticated user to follow another user specified by user_id.

Example Request:

Bash

POST /api/accounts/follow/2/ HTTP/1.1
Host: localhost:8000
Authorization: Token <your_token>
Response (200 OK):

JSON

{
    "status": "You are now following jerryd25"
}
Unfollow a User
Method: POST

URL: /api/accounts/unfollow/<int:user_id>/

Permissions: IsAuthenticated

Description: Allows the authenticated user to unfollow another user.

Example Request:

Bash

POST /api/accounts/unfollow/2/ HTTP/1.1
Host: localhost:8000
Authorization: Token <your_token>
Response (200 OK):

JSON

{
    "status": "You have unfollowed jerryd25"
}
Posts, Comments, and Feeds
These endpoints manage user-generated content, including the new personalized feed.

Access the User Feed
Method: GET

URL: /api/feed/

Permissions: IsAuthenticated

Description: Retrieves a paginated list of posts from all users that the authenticated user is following. Posts are ordered by most recent first.

Example Request:

Bash

GET /api/feed/ HTTP/1.1
Host: localhost:8000
Authorization: Token <your_token>
Response (200 OK):

JSON

{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 4,
            "author": { "id": 2, "username": "jerryd25", ... },
            "title": "User B's post 2",
            "content": "This is a post from the user you follow.",
            "created_at": "2025-09-07T18:54:44.574593Z",
            "comments": []
        },
        {
            "id": 3,
            "author": { "id": 2, "username": "jerryd25", ... },
            "title": "User B's post 1",
            "content": "This is a post from the user you follow.",
            "created_at": "2025-09-07T18:54:34.134462Z",
            "comments": []
        }
    ]
}
Other Post and Comment Endpoints
GET /api/posts/: List all posts.

POST /api/posts/: Create a new post.

GET/PUT/PATCH/DELETE /api/posts/<id>/: Manage a single post.

GET/POST /api/posts/<post_id>/comments/: List or create comments on a post.

GET/PUT/PATCH/DELETE /api/posts/<post_id>/comments/<id>/: Manage a single comment.

Permissions & Rules
Authentication: All endpoints except register and login require a valid token in the Authorization header.

Ownership: The IsOwnerOrReadOnly permission ensures that users can only PUT, PATCH, or DELETE their own posts and comments.

Following: Users can only modify their own following list.