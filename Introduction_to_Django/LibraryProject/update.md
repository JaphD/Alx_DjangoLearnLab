>>> book = Book.objects.get(id=1)
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()

>>> Book.objects.get(id=1)
# Expected Output:
# Nineteen Eighty-Four (1949)
