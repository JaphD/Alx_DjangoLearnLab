from django.urls import path
from .views import list_books_view

app_name = 'relationship_app'

urlpatterns = [
    path('book-list/', list_books_view, name='book-list')
]