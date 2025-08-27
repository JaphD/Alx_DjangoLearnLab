import datetime
from rest_framework import serializers
from .models import Book, Author


# Translates Book model instances to JSON and handles input validation.

class BookSerializer(serializers.ModelSerializer):
    class Meta:
          # Specifies which model this serializer represents.

          model = Book

           # Defines which model fields will be included in serialized representations.

          fields = ['id', 'title', 'publication_year', 'author']


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']


