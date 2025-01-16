"""
Open Library Integration for Book Search Enrichment

This module provides functionality to interact with the Open Library API to 
enrich book search results with additional metadata. It is designed to work 
in conjunction with a book recommendation system, adding detailed information 
to books recommended by another service (e.g., ChatGPT).
"""

from data_models import Book, ResponseWithBooks
from retrieve_concurrent import RetrieveConcurrent

class NumberRetriever:
    """A class for retrieving and formatting numerical values"""

    def __init__(self, data):
        self.data = data

    def number(self, key, is_float=False):
        """Retrieves a numerical value from the data dictionary"""
        res = self.data.get(key, "")
        if is_float and res:
            try:
                res = str(round(float(res), 2))
            except:
                pass
        return str(res)


class FetchBookData:
    """
    Fetches book information and ratings from Open Library using the
    search.json endpoint
    """

    FIELDS = [
        "ratings_count", "number_of_pages_median", "first_publish_year",
        "ratings_count", "ratings_count_1", "ratings_count_2",
        "ratings_count_3", "ratings_count_4", "ratings_count_5"]

    def run(self, isbn_list):
        """
        Fetches book information.

        Args:
            isbn_list (list of str): A list of ISBNs to query.

        Returns:
            dict: A dictionary containing information about each book indexed
            by ISBN, including ratings.
        """

        try:
            retriever = RetrieveConcurrent()
            results = retriever.retrieve_bunch(isbn_list)

            for isbn, data in results.items():
                book_info = {}
                if data[0]:
                    if data[1].status_code == 200:
                        book_info = data[1].json()
                        if "docs" in book_info and book_info["docs"]:
                            book_info = book_info["docs"][0]
                if not book_info:
                    book_info = {}

                get = NumberRetriever(book_info)
                results[isbn] = {
                    "ratings_average": get.number("ratings_average", True)
                }

                for field in self.FIELDS:
                    results[isbn][field] = get.number(field)

        except Exception as e:
            print(f"An error occurred in run method: {e}")

        return results


class BookSearchApp:
    """
    Application to perform book searches and enrich results using the
    Open Library API.

    Attributes:
        service (OpenLibraryService): The service used to interact with
        the Open Library API.
        response_with_books (ResponseWithBooks): The initial response
        containing books to be enriched.
    """

    def __init__(self, response_with_books: ResponseWithBooks):
        """
        Initialize the BookSearchApp with the required services and data.

        Args:
            service (OpenLibraryService): An instance of OpenLibraryService.
            response_with_books (ResponseWithBooks): The initial response with books to be enriched.
        """
        # self.service = service
        self.response_with_books = response_with_books

    async def search_books(self) -> ResponseWithBooks:
        """
        Enrich books in the response using the Open Library API.

        Uses asyncio.gather to fetch metadata for all books concurrently.

        Returns:
            ResponseWithBooks: An updated response containing enriched book data.
        """
        isbn_list = []

        for book in self.response_with_books.books:
            if book.isbn:
                isbn_list.append(book.isbn)
        fetch_book_data = FetchBookData()
        all_book_data = fetch_book_data.run(isbn_list)

        result = []
        for book in self.response_with_books.books:
            if book.isbn and book.isbn in all_book_data:
                res = all_book_data[book.isbn]
                res["title"] = book.title
                res["author_name"] = book.author_name
                res["brief_description"] = book.brief_description
                res["isbn"] = book.isbn

                enriched_book = Book(**res)
                result.append(enriched_book)

        return ResponseWithBooks(
            books=result,
            further_chat=self.response_with_books.further_chat
        )
