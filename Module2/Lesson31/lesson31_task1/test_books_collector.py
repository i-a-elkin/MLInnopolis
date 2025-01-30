"""Lesson31 Task1: Implementation the TestBooksCollector class."""

import unittest
from books_collector import BooksCollector


class TestBooksCollector(unittest.TestCase):
    """Unit tests for the BookCollector class."""

    def setUp(self):
        """Initialization before each test"""
        self.collector = BooksCollector()

    def test_add_new_book(self):
        """Checking a new book"""
        self.collector.add_new_book("Гарри Поттер")
        self.assertIn("Гарри Поттер", self.collector.books_genre)
        self.assertIsNone(self.collector.books_genre["Гарри Поттер"])

    def test_add_existing_book(self):
        """Verification of re -adding a book (should not be added)"""
        self.collector.add_new_book("Властелин колец")
        self.collector.add_new_book("Властелин колец")
        self.assertEqual(len(self.collector.books_genre), 1)

    def test_set_book_genre_valid(self):
        """Checking the installation of the correct genre"""
        self.collector.add_new_book("Гарри Поттер")
        self.collector.set_book_genre("Гарри Поттер", "Фэнтези")
        self.assertEqual(self.collector.get_book_genre("Гарри Поттер"), "Фэнтези")

    def test_set_book_genre_invalid(self):
        """Checking the setting of an incorrect genre (should not be set)"""
        self.collector.add_new_book("Матрица")
        self.collector.set_book_genre("Матрица", "Роман")
        self.assertIsNone(self.collector.get_book_genre("Матрица"))

    def test_get_books_with_specific_genre(self):
        """Checking the list of books on genre"""
        self.collector.add_new_book("Гарри Поттер")
        self.collector.set_book_genre("Гарри Поттер", "Фэнтези")
        self.collector.add_new_book("Властелин колец")
        self.collector.set_book_genre("Властелин колец", "Фэнтези")
        books = self.collector.get_books_with_specific_genre("Фэнтези")
        self.assertEqual(set(books), {"Гарри Поттер", "Властелин колец"})

    def test_get_books_genre_empty(self):
        """Checks that the method returns an empty dictionary if there are no books"""
        self.assertEqual(
            self.collector.get_books_genre(), {}, "An empty dictionary is expected"
        )

    def test_get_books_genre_with_books(self):
        """Checks that the method returns the correct dictionary of books and their genres"""
        self.collector.add_new_book("Гарри Поттер")
        self.collector.set_book_genre("Гарри Поттер", "Фэнтези")

        self.collector.add_new_book("Властелин колец")
        self.collector.set_book_genre("Властелин колец", "Фэнтези")

        expected_result = {"Гарри Поттер": "Фэнтези", "Властелин колец": "Фэнтези"}
        self.assertEqual(
            self.collector.get_books_genre(),
            expected_result,
            "Dictionary of books with genres must be the same",
        )

    def test_get_books_for_children(self):
        """Checking a list of books suitable for children"""
        self.collector.add_new_book("Гарри Поттер")
        self.collector.set_book_genre("Гарри Поттер", "Фэнтези")
        self.collector.add_new_book("Матрица")
        self.collector.set_book_genre("Матрица", "Научная фантастика")
        children_books = self.collector.get_books_for_children()
        self.assertEqual(children_books, ["Гарри Поттер"])

    def test_add_book_in_favorites(self):
        """Checking the addition of a book to favorites"""
        self.collector.add_new_book("Гарри Поттер")
        self.collector.add_book_in_favorites("Гарри Поттер")
        self.assertIn("Гарри Поттер", self.collector.get_list_of_favorites_books())

    def test_add_nonexistent_book_in_favorites(self):
        """Checking the addition of a non -existing book to favorites (should not be added)"""
        self.collector.add_book_in_favorites("Non -existing book")
        self.assertNotIn(
            "Non -existing book", self.collector.get_list_of_favorites_books()
        )

    def test_delete_book_from_favorites(self):
        """Checking a book removal from the favorites"""
        self.collector.add_new_book("Гарри Поттер")
        self.collector.add_book_in_favorites("Гарри Поттер")
        self.collector.delete_book_from_favorites("Гарри Поттер")
        self.assertNotIn("Гарри Поттер", self.collector.get_list_of_favorites_books())

    def test_get_list_of_favorites_books(self):
        """Checking the list of favorite books"""
        self.collector.add_new_book("Гарри Поттер")
        self.collector.add_new_book("Властелин колец")
        self.collector.add_book_in_favorites("Гарри Поттер")
        self.assertEqual(self.collector.get_list_of_favorites_books(), ["Гарри Поттер"])


if __name__ == "__main__":
    unittest.main()
