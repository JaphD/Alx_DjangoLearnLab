from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
herbert_books = Book.objects.filter(author__name='Frank Herbert')

for book in herbert_books:
    print(book.title)

orwell_books = Book.objects.filter(author__name='George Orwell')

for book in orwell_books:
    print(book.title)

tolkien_books = Book.objects.filter(author__name='J.R.R. Tolkien')

for book in tolkien_books:
    print(book.title)

# List all books in a library
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

# Retrieve the librarian for a library
librarian1 = library1.librarian
print(librarian1)

librarian2 = library2.librarian
print(librarian2)
