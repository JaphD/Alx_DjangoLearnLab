from django.db import models

# Create your models here.

# This model represents a writer or creator of books.
class Author(models.Model):
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name

class Book(models.Model):
    # A character field for the book's title.
    title = models.CharField(max_length=125)

    # An integer field to store the year the book was published.
    publication_year = models.IntegerField()

    # A ForeignKey field linking a Book to an Author.
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} by {self.author} was published in {self.publication_year}"