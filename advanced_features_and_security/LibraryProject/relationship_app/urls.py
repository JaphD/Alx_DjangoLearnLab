from django.urls import path
from .views import list_books_view, create_book, edit_book, delete_book

app_name = 'relationship_app'

urlpatterns = [
    path('book-list/', list_books_view, name='book-list'),
    path('book-create/', create_book, name='book-create'),
    path('book-edit/<int:pk>/', edit_book, name='book-edit'),
    path('book-delete/<int:pk>/', delete_book, name='book-delete'),
]