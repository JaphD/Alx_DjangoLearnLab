from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import login_required

@login_required
def list_books_view(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})
