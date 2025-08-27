from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

# DetailView: Retrieve single book

class ListView(generics.ListAPIView):
    """
    GET /books/<pk>/
    
    Returns the details of a single book by primary key (id).
    Permissions: Public (AllowAny)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['publication_year']
    ordering = ['-publication_year']


class DetailView(generics.RetrieveAPIView):
    """
    POST /books/create/
    
    Creates a new book instance.
    Permissions: Public (AllowAny)
    Custom behavior:
    - Validates that book title is unique (case-insensitive)
    - Ensures publication year is not in the future (max 2025 in this example)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# CreateView: Add a new book

class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Custom validation: Check for duplicate titles (case-insensitive)
        title = serializer.validated_data.get('title')
        if Book.objects.filter(title__iexact=title).exists():
            raise ValueError("A book with this title already exists.")
        
        # Example of extra business logic: Publication year cannot be in the future
        if serializer.validated_data.get('publication_year') > 2025:
            raise ValueError("Publication year cannot be in the future.")
        
        serializer.save()  # Save the book instance

# UpdateView: Modify an existing book

class UpdateView(generics.UpdateAPIView):
    """
    PATCH /books/<pk>/update/ or PUT /books/<pk>/update/
    
    Updates an existing book instance.
    Permissions: Authenticated users only
    Custom behavior:
    - Title cannot be empty
    - Author cannot be changed once the book is created
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # Custom validation: Don't allow title to be empty
        if 'title' in data and not data['title'].strip():
            return Response(
                {"error": "Title cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extra rule: Cannot change author after creation
        if 'author' in data and data['author'] != str(instance.author.id):
            return Response(
                {"error": "You cannot change the author of a book once created."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().update(request, *args, **kwargs)

# DeleteView: Remove a book

class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]