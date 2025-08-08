from django.urls import path
from . import views
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('book-list/', views.book_list, name='book_list'),
]


urlpatterns = [
    # URL for the list of books
    path('books/', list_books.as_view(), name= 'book-list'),

    # URL for pointing to the LibraryDetailView
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]