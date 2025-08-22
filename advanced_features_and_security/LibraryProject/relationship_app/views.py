from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from .models import Book, Author
from .forms import BookForm
from django.db import transaction



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
    author = book.author  # capture the related author

    if request.method == 'POST':
        with transaction.atomic():
            book.delete()
            author.delete()
        return redirect('relationship_app:book-list')

    return render(
        request,
        'relationship_app/book_confirm_delete.html',
        {'book': book}
    )

