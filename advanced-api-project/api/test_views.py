from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import Book, Author
from .serializers import BookSerializer
from django.contrib.auth.models import User
import json

class BookAPITestCase(TestCase):
    def setUp(self):
        # Set up test data and client
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(title='Test Book', publication_year=2020, author=self.author)
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.id})
        self.update_url = reverse('book-update', kwargs={'pk': self.book.id})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book.id})

    def test_list_books(self):
        # Test GET list endpoint
        response = self.client.get(self.list_url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_authenticated(self):
        # Test POST create endpoint with authentication
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(title='New Book').publication_year, 2024)

    def test_create_book_unauthenticated(self):
        # Test POST create endpoint without authentication
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_duplicate_title(self):
        # Test POST create endpoint with duplicate title
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'Test Book',
            'publication_year': 2021,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_book_future_year(self):
        # Test POST create endpoint with future year
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'Future Book',
            'publication_year': 2026,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_update_book_authenticated(self):
        # Test PATCH update endpoint with authentication
        self.client.login(username='testuser', password='testpass')
        data = {'title': 'Updated Book'}
        response = self.client.patch(self.update_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_update_book_unauthenticated(self):
        # Test PATCH update endpoint without authentication
        data = {'title': 'Unauthorized Update'}
        response = self.client.patch(self.update_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_empty_title(self):
        # Test PATCH update endpoint with empty title
        self.client.login(username='testuser', password='testpass')
        data = {'title': ''}
        response = self.client.patch(self.update_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_update_book_change_author(self):
        # Test PATCH update endpoint with author change
        self.client.login(username='testuser', password='testpass')
        new_author = Author.objects.create(name='New Author')
        data = {'author': new_author.id}
        response = self.client.patch(self.update_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_delete_book_authenticated(self):
        # Test DELETE endpoint with authentication
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_unauthenticated(self):
        # Test DELETE endpoint without authentication
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books(self):
        # Test filtering by author
        response = self.client.get(self.list_url, {'author': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_search_books(self):
        # Test searching by title
        response = self.client.get(self.list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_order_books(self):
        # Test ordering by publication_year
        Book.objects.create(title='Older Book', publication_year=2019, author=self.author)
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Older Book')