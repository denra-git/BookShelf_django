from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.storage.base import Message
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse

from .models import Book, Category


class BookAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user_a",
            password="passa123",
        )

        self.other_user = User.objects.create_user(
            username="user_b",
            password="passb123",
        )

        self.book = Book.objects.create(
            title="book_title",
            author="author",
            owner=self.user,
        )

        self.other_book = Book.objects.create(
            title="other_book",
            author="other_author",
            owner=self.other_user,
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("books:user_book"))

        self.assertRedirects(
            response,
            reverse("users:login") + "?next=/books/",
        )

    def test_authenticated_user_can_access_books(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("books:user_book"))

        self.assertEqual(response.status_code, 200)

    def test_user_can_access_own_book_detail(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "books:book_detail",
                kwargs={"id": self.book.id},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["book"], self.book)

    def test_user_cannot_access_other_users_book_detail(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "books:book_detail",
                kwargs={"id": self.other_book.id},
            )
        )

        self.assertRedirects(
            response,
            reverse("books:user_book"),
        )

    def test_user_can_edit_own_book(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "books:edit_book",
                kwargs={"id": self.book.id},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_user_cannot_edit_other_users_book(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "books:edit_book",
                kwargs={"id": self.other_book.id},
            )
        )

        self.assertRedirects(
            response,
            reverse("books:user_book"),
        )

    def test_user_can_delete_own_book(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "books:delete_book",
                kwargs={"id": self.book.id},
            )
        )

        self.assertRedirects(
            response,
            reverse("books:user_book"),
        )

        self.assertFalse(
            Book.objects.filter(id=self.book.id).exists()
        )

    def test_user_cannot_delete_other_users_book(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "books:delete_book",
                kwargs={"id": self.other_book.id},
            )
        )

        self.assertRedirects(
            response,
            reverse("books:user_book"),
        )

        self.assertTrue(
            Book.objects.filter(id=self.other_book.id).exists()
        )


class BookRelationshipTests(TestCase):
    def test_book_owner_is_correct(self):
        user = User.objects.create_user(
            username="user",
            password="pass123",
        )

        book = Book.objects.create(
            title="title",
            author="author",
            owner=user,
        )

        self.assertEqual(book.owner, user)

    def test_book_can_have_multiple_categories(self):
        user = User.objects.create_user(
            username="user",
            password="pass123",
        )

        book = Book.objects.create(
            title="title",
            author="author",
            owner=user,
        )

        category_1 = Category.objects.create(name="Novel")
        category_2 = Category.objects.create(name="Poetry")

        book.categories.add(category_1, category_2)

        self.assertIn(category_1, book.categories.all())
        self.assertIn(category_2, book.categories.all())


class BookMessageTests(MessagesTestMixin, TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="pass123",
        )

        self.book = Book.objects.create(
            title="title",
            author="author",
            owner=self.user,
        )

    def test_add_book_success_message(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("books:add_book"),
            {
                "title": "new title",
                "author": "new author",
            },
        )

        expected_messages = [
            Message(messages.SUCCESS, ". SUCCESSFULLY ADDED .")
        ]

        self.assertRedirects(
            response,
            reverse("books:user_book"),
        )

        self.assertMessages(
            response,
            expected_messages,
            ordered=True,
        )

    def test_edit_book_success_message(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "books:edit_book",
                kwargs={"id": self.book.id},
            ),
            {
                "title": "edited title",
                "author": "author",
            },
        )

        self.book.refresh_from_db()

        expected_messages = [
            Message(messages.SUCCESS, ". SUCCESSFULLY EDITED .")
        ]

        self.assertRedirects(
            response,
            reverse(
                "books:book_detail",
                kwargs={"id": self.book.id},
            ),
        )

        self.assertEqual(
            self.book.title,
            "edited title",
        )

        self.assertMessages(
            response,
            expected_messages,
            ordered=True,
        )

    def test_delete_book_success_message(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "books:delete_book",
                kwargs={"id": self.book.id},
            )
        )

        expected_messages = [
            Message(messages.SUCCESS, ". SUCCESSFULLY DELETED .")
        ]

        self.assertRedirects(
            response,
            reverse("books:user_book"),
        )

        self.assertFalse(
            Book.objects.filter(id=self.book.id).exists()
        )

        self.assertMessages(
            response,
            expected_messages,
            ordered=True,
        )


class BookFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="pass123",
        )

    def test_book_can_be_created_without_categories(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("books:add_book"),
            {
                "title": "title",
                "author": "author",
            },
        )

        self.assertRedirects(
            response,
            reverse("books:user_book"),
        )

        book = Book.objects.get(
            title="title",
            owner=self.user,
        )

        self.assertEqual(
            book.categories.count(),
            0,
        )

    def test_book_can_be_created_with_multiple_categories(self):
        category_1 = Category.objects.create(name="Novel")
        category_2 = Category.objects.create(name="Fantasy")

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("books:add_book"),
            {
                "title": "title",
                "author": "author",
                "categories": [
                    category_1.id,
                    category_2.id,
                ],
            },
        )

        self.assertRedirects(
            response,
            reverse("books:user_book"),
        )

        book = Book.objects.get(
            title="title",
            owner=self.user,
        )

        self.assertEqual(
            book.categories.count(),
            2,
        )

        self.assertIn(
            category_1,
            book.categories.all(),
        )

        self.assertIn(
            category_2,
            book.categories.all(),
        )


class BookErrorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="pass123",
        )

    def test_nonexistent_book_detail_returns_404(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "books:book_detail",
                kwargs={"id": 313313313},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_nonexistent_book_edit_returns_404(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "books:edit_book",
                kwargs={"id": 313313313},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_nonexistent_book_delete_returns_404(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "books:delete_book",
                kwargs={"id": 313313313},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_book_does_not_allow_get(self):
        book = Book.objects.create(
            title="title",
            author="author",
            owner=self.user,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "books:delete_book",
                kwargs={"id": book.id},
            )
        )

        self.assertEqual(response.status_code, 405)

        self.assertTrue(
            Book.objects.filter(id=book.id).exists()
        )


class BookCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="pass123",
        )

        self.book = Book.objects.create(
            title="title",
            author="author",
            owner=self.user,
        )

    def test_authenticated_user_can_add_book(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("books:add_book"),
            {
                "title": "new title",
                "author": "new author",
            },
        )

        self.assertRedirects(
            response,
            reverse("books:user_book"),
        )

        self.assertTrue(
            Book.objects.filter(
                title="new title",
                owner=self.user,
            ).exists()
        )

    def test_user_can_read_book_detail(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "books:book_detail",
                kwargs={"id": self.book.id},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["book"],
            self.book,
        )

    def test_user_can_update_book(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "books:edit_book",
                kwargs={"id": self.book.id},
            ),
            {
                "title": "new title",
                "author": "author",
            },
        )

        self.book.refresh_from_db()

        self.assertRedirects(
            response,
            reverse(
                "books:book_detail",
                kwargs={"id": self.book.id},
            ),
        )

        self.assertEqual(
            self.book.title,
            "new title",
        )