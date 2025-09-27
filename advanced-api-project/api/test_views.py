from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="tester", password="testpass123")
        self.client.login(username="tester", password="testpass123")

        # Create a book
        self.book = Book.objects.create(
            title="Test Driven Development",
            author="Kent Beck",
            publication_year=2003
        )

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data[0])   # ✅ Check response.data
        self.assertEqual(response.data[0]["title"], "Test Driven Development")

    def test_create_book(self):
        url = reverse("book-create")
        data = {"title": "Clean Code", "author": "Robert C. Martin", "publication_year": 2008}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Clean Code")  # ✅ response.data check

    def test_update_book(self):
        url = reverse("book-update", args=[self.book.id])
        data = {"title": "Updated TDD", "author": "Kent Beck", "publication_year": 2005}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated TDD")  # ✅ response.data check

    def test_delete_book(self):
        url = reverse("book-delete", args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
