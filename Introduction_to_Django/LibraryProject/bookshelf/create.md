>>> book = Book.objects.create(
...     title="1984",
...     author="George Orwell",
...     publication_year=1949
... )

>>> Book.objects.all()
# Expected Output:
# <QuerySet [<Book: 1984 (1949)>]>
