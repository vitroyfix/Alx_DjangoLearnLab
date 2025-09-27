from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(title="Test Book", publication_year=2020, author=self.author)

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        url = reverse("book-create")
        data = {"title": "New Book", "publication_year": 2022, "author": self.author.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # unauthenticated

    def test_filter_books_by_title(self):
        url = reverse("book-list") + "?title=Test Book"
        response = self.client.get(url)
        self.assertContains(response, "Test Book")

    def test_order_books(self):
        Book.objects.create(title="Another Book", publication_year=2018, author=self.author)
        url = reverse("book-list") + "?ordering=publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
