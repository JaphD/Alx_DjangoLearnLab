>>> book = Book.objects.get(id=1)
>>> print(book)
# Expected Output:
# 1984 (1949)

>>> Book.objects.all()
# Expected Output:
# <QuerySet [<Book: 1984 (1949)>]>
