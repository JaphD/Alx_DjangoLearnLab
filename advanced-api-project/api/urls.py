from django.urls import path
from api.views import ListView, DetailView, CreateView, UpdateView, DeleteView


urlpatterns = [
    path('books/', ListView.as_view(), name='book-list'),
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),
    path('books/create/', CreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),
    path('books/update/', UpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),
    path('books/delete/', UpdateView.as_view(), name='book-update'),
]