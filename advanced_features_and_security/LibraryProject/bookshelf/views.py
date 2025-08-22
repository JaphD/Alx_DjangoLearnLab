from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Book, Author
from .forms import BookForm

# Create your views here.

def home_view(request):
    return render(request, 'base.html', {'year': now().year})

# User register
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'bookshelf/register.html', {'form': form})


# User Login
def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get('identifier')  # email OR username
        password = request.POST.get('password')

        user = authenticate(request, username=identifier, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('bookshelf:profile')
        
    return render(request, 'bookshelf/login.html', {'identifier': identifier})


# User Logout → Redirect to logout.html
def logout_view(request):
    logout(request)
    return render(request, 'bookshelf/logout.html')

@login_required
def profile_view(request):
    return render(request, 'bookshelf/profile.html')

@permission_required('relationship_app.can_view', raise_exception=True)
def list_books_view(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

@permission_required('relationship_app.can_create', raise_exception=True)
def create_book(request):
    form = BookForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # get author name from the form
        author_name = form.cleaned_data.get('author_name').strip()

        # get or create the author object
        author, _ = Author.objects.get_or_create(name=author_name)

        # build the book object without saving
        book = form.save(commit=False)
        book.author = author
        book.save()

        return redirect('relationship_app:book-list')

    return render(request, 'relationship_app/book_form.html', {'form': form})


@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)

    if request.method == 'POST' and form.is_valid():
        # get the author name from the form
        author_name = form.cleaned_data.get('author_name').strip()

        # get or create the Author instance
        author, _ = Author.objects.get_or_create(name=author_name)

        # save the book instance without committing
        book = form.save(commit=False)
        book.author = author  
        book.save()

        return redirect('relationship_app:book-list')

    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:book-list')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})