Social Media API

A Django REST Framework API for user authentication and profile management.
Overview

Framework: Django with Django REST Framework
Database: SQLite (default)
Authentication: Token-based (DRF TokenAuthentication)
Endpoints:

POST /api/accounts/register/: Register a user and get a token.
POST /api/accounts/login/: Authenticate and get a token.
GET/PATCH /api/accounts/profile/: Retrieve or update user profile.


User Model

Custom User (accounts.models.User):

Extends AbstractUser
Fields:

bio: Text field (max 500 chars, optional)
profile_picture: Image field (optional)
followers: ManyToMany (asymmetrical, self-referencing)


Setup

Install Dependencies:
bashpip install django djangorestframework

Create Project and App:
bashdjango-admin startproject social_media_api .
python manage.py startapp accounts

Configure settings.py:
pythonINSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'accounts',
]
AUTH_USER_MODEL = 'accounts.User'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication'],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
}

Apply Migrations:
bashpython manage.py makemigrations
python manage.py migrate

Run Server:
bashpython manage.py runserver


Register and Authenticate Users
Register

Method: POST
URL: http://localhost:8000/api/accounts/register/
Headers: Content-Type: application/json
Body:
json{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpassword",
  "bio": "Test bio"
}

Response (201 Created):
json{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "bio": "Test bio",
    "profile_picture": null,
    "followers": []
  },
  "token": "<token>"
}


Login

Method: POST
URL: http://localhost:8000/api/accounts/login/
Headers: Content-Type: application/json
Body:
json{
  "username": "testuser",
  "password": "testpassword"
}

Response (200 OK):
json{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "bio": "Test bio",
    "profile_picture": null,
    "followers": []
  },
  "token": "<token>"
}


Profile

Method: GET (retrieve) or PATCH (update)
URL: http://localhost:8000/api/accounts/profile/
Headers:
textContent-Type: application/json
Authorization: Token <token>

Body (PATCH, optional):
json{
  "bio": "Updated bio"
}

Response (200 OK, GET):
json{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "bio": "Test bio",
  "profile_picture": null,
  "followers": []
}