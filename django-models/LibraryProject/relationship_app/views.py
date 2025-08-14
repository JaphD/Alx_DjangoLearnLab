from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Library, Book, Author
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test, permission_required



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
# User Registration
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# User Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  
            return redirect('relationship_app:book-list')
            
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


# User Logout → Redirect to logout.html
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')


#Role check functions
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Views for each role

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {
        'username': request.user.username,
        'role': 'Admin'
    })

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {
        'username': request.user.username,
        'role': 'Librarian'
    })


@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {
        'username': request.user.username,
        'role': 'Member'
    })

# Add a book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        publication_year = request.POST.get('publication_year')

        # Get or create the Author object
        author, _ = Author.objects.get_or_create(name=author_name)

        Book.objects.create(
            title=title, 
            author=author, 
            publication_year=publication_year
        )
        return redirect('relationship_app:book_list')
    
    return render(request, 'relationship_app/add_book.html')

# Edit a book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        publication_year = request.POST.get('publication_year')

        # Update title & year
        book.title = title
        book.publication_year = publication_year

        # Get or create Author instance
        author, _ = Author.objects.get_or_create(name=author_name)
        book.author = author

        book.save()
        return redirect('relationship_app:book_list')
    return render(request, 'relationship_app/edit_book.html', {'book': book})

# Delete a book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:book_list')
    return render(request, 'relationship_app/delete_book.html', {'book': book})



    

