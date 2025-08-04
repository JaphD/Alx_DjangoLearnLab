from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
herbert_books = Book.objects.filter(author__name='Frank Herbert')

# Initial Implementation
"""
for book in herbert_books:
    print(book.title)

orwell_books = Book.objects.filter(author__name='George Orwell')

for book in orwell_books:
    print(book.title)

tolkien_books = Book.objects.filter(author__name='J.R.R. Tolkien')

for book in tolkien_books:
    print(book.title)

"""
# Implementation for the checker
author_name = 'George Orwell'
author = Author.objects.get(name=author_name)

books_by_author = Book.objects.filter(author=author)

# List all books in a library -- initial Implementation below
"""
library1 = Library.objects.get(name = "Abrehot")
abrehot_books = library1.books.all()

print(f"Books in {library1.name}:")
for book in abrehot_books:
    print(book.title)

library2 = Library.objects.get(name = "Wemezekir")
wemezekir_books = library2.books.all()

print(f"Books in {library2.name}:")
for book in wemezekir_books:
    print(book.title)
"""
# Implementation for the checker
library_name = "Abrehot"
library = Library.objects.get(name=library_name)
        
books = library.books.all()
        
print(f"Books in {library.name}:")
for book in books:
    print(book.title)

# Retrieve the librarian for a library
library1 = Library.objects.get(id=1)
librarian1 = Librarian.objects.get(library= library1)
print(librarian1)


