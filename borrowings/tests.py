from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing

BORROWINGS_URL = reverse("borrowings-list")


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


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_borrowings_unauthorized(self):
        res = self.client.get(BORROWINGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_create_borrowing(self):
        book = sample_book()
        payload = {
            "book": book.id,
            "expected_return_date": "2026-03-30",
        }
        res = self.client.post(BORROWINGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_borrowing_decreases_inventory(self):
        book = sample_book(inventory=3)
        payload = {
            "book": book.id,
            "expected_return_date": "2026-03-30",
        }
        self.client.post(BORROWINGS_URL, payload)
        book.refresh_from_db()
        self.assertEqual(book.inventory, 2)

    def test_create_borrowing_no_inventory(self):
        book = sample_book(inventory=0)
        payload = {
            "book": book.id,
            "expected_return_date": "2026-03-30",
        }
        res = self.client.post(BORROWINGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
