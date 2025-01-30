"""Lesson31 Task1: Implementation the BooksCollector class."""


class BooksCollector:
    """A class for managing a collection of books, their genres, and favorite books."""

    def __init__(self):
        self.books_genre = {}
        self.favorites = []
        self.genre = [
            "Фантастика",
            "Фэнтези",
            "Научная фантастика",
            "Детектив",
            "Драма",
            "Приключения",
        ]
        self.genre_age_rating = ["Фантастика", "Фэнтези", "Приключения"]

    def add_new_book(self, book_name):
        """Adds a book to a dictionary without an indication of the genre"""
        if book_name and book_name not in self.books_genre:
            self.books_genre[book_name] = None

    def set_book_genre(self, book_name, genre):
        """Sets the genre for the book if the genre is permissible"""
        if book_name in self.books_genre and genre in self.genre:
            self.books_genre[book_name] = genre

    def get_book_genre(self, book_name):
        """Returns the genre of the book"""
        return self.books_genre.get(book_name)

    def get_books_with_specific_genre(self, genre):
        """Returns a list of books of this genre"""
        return [
            book for book, book_genre in self.books_genre.items() if book_genre == genre
        ]

    def get_books_genre(self):
        """Returns the entire dictionary of books with their genres"""
        return self.books_genre

    def get_books_for_children(self):
        """Returns a list of books that are suitable for children"""
        return [
            book
            for book, genre in self.books_genre.items()
            if genre in self.genre_age_rating
        ]

    def add_book_in_favorites(self, book_name):
        """Adds a book to favorites"""
        if book_name in self.books_genre and book_name not in self.favorites:
            self.favorites.append(book_name)

    def delete_book_from_favorites(self, book_name):
        """Deleted a book from the favorites"""
        if book_name in self.favorites:
            self.favorites.remove(book_name)

    def get_list_of_favorites_books(self):
        """Returns a list of favorites books"""
        return self.favorites
