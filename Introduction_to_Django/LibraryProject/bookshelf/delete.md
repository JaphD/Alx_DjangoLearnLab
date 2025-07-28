>>> book = Book.objects.get(id=1)
>>> book.delete()
# Expected Output:
# (1, {'bookshelf.Book': 1})

>>> Book.objects.all()
# Expected Output:
# <QuerySet []>
