from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book

BOOKS_URL = reverse("book-list")


def sample_book(**params):
    defaults = {
        "title": "Test Book",
        "author": "Test Author",
        "cover": "HARD",
        "inventory": 5,
        "daily_fee": "1.50",
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_books(self):
        sample_book()
        res = self.client.get(BOOKS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_book_unauthorized(self):
        payload = {
            "title": "Test",
            "author": "Author",
            "cover": "HARD",
            "inventory": 5,
            "daily_fee": "1.50",
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="test12345",
        )
        self.client.force_authenticate(self.admin)

    def test_create_book(self):
        payload = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "cover": "HARD",
            "inventory": 5,
            "daily_fee": "1.50",
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_delete_book(self):
        book = sample_book()
        url = reverse("book-detail", args=[book.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    