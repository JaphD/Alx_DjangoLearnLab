from django.urls import path
from . import views
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import views


app_name = 'relationship_app'

# Class based view
urlpatterns = [
    # For the Function based view
    path('book-list/', views.book_list, name='book_list'),
    
    # URL for the list of books
    path('books/', list_books.as_view(), name= 'book-list'),

    # URL for pointing to the LibraryDetailView
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),

    # Authentication URLs
    path('register/', views.register_view, name='register'),

    #path('login/', views.login_view, name='login'),

    #path('logout/', views.logout_view, name='logout'),

    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]

