from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Library, Book
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Implement Function-based view
def book_list(request):
    """
    A view to list all books in the database.
    """
    # Query the database to get all Book objects
    books = Book.objects.all()

    # Create a list of strings, one for each book, using list comprehension
    book_list_items = [f"{book.title} by {book.author.name}" for book in books]

    # Join the list of strings into a single string with newlines
    book_list_text = "\n".join(book_list_items)

    # Return an HttpResponse with the formatted text
    return HttpResponse(book_list_text, content_type="text/plain")

class list_books(ListView):
    model = Book
    template_name = 'relationship_app/list_books.html'
    context_object_name = 'books'

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Views for user authentication
# Registration View
def register(request):
    """Handles user registration."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:login')
    else:
        # If it's a GET request, create a blank form
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})
    

