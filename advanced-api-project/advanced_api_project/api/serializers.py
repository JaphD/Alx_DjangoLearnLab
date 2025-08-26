import datetime
from rest_framework import serializers
from .models import Book, Author


# Translates Book model instances to JSON and handles input validation.

class BookSerializer(serializers.ModelSerializer):
    class Meta:
          # Specifies which model this serializer represents.

          model = Book

           # Defines which model fields will be included in serialized representations.

          fields = ['id', 'title', 'publication_year']

    def validate_publication_year(self, value):
         """
         Field-level validation for 'publication_year'.
         Ensures the year is not in the future
         """
         current_year = datetime.date.today().year

         # If a user tries to submit a year beyond the current one, we reject it.

         if value > current_year:
              raise serializers.ValidationError(
                   "Publication year cannot be in the future."
              )
         
         # Return the validated value so the serializer can proceed.
         return value

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only = True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']


