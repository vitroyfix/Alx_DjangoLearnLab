from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(TestCase):
    """Unit tests for Book API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book", publication_year=2020, author=self.author
        )

    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Book", str(response.data))

    def test_get_single_book(self):
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Book")

    def test_filter_books(self):
        response = self.client.get('/api/books/?publication_year=2020')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_books(self):
        response = self.client.get('/api/books/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
