from django.urls import path
from . import views
from .views import BookListView, LibraryDetailView

urlpatterns = [
    path('book-list/', views.book_list, name='book_list'),
]


urlpatterns = [
    # URL for the list of books
    path('books/', BookListView.as_view(), name= 'book-list'),

    # URL for pointing to the LibraryDetailView
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]