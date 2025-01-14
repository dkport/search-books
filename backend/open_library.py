"""
Open Library Integration for Book Search Enrichment

This module provides functionality to interact with the Open Library API to 
enrich book search results with additional metadata. It is designed to work 
in conjunction with a book recommendation system, adding detailed information 
to books recommended by another service (e.g., ChatGPT).
"""

import httpx

from data_models import Book, ResponseWithBooks


class FetchBookData:
    """
    Fetches book information and ratings from Open Library using the
    search.json endpoint
    """

    @staticmethod
    def run(isbn_list):
        """
        Fetches book information.

        Args:
            isbn_list (list of str): A list of ISBNs to query.

        Returns:
            dict: A dictionary containing information about each book indexed by ISBN, including ratings.
        """
        base_url = "https://openlibrary.org/search.json"
        results = {}

        try:
            for isbn in isbn_list:
                # Query the search endpoint for the specific ISBN
                params = {"isbn": isbn}

                response = httpx.get(base_url, params=params, timeout=8.0)
                response.raise_for_status()
                data = response.json()

                if data.get("docs"):
                    # Use the first match as the result
                    book_info = data["docs"][0]

                    average = book_info.get("ratings_average", "")
                    if average:
                        average = round(average, 2)

                    results[isbn] = {                    
                        "title": book_info.get("title", "N/A"),
                        "author_name": book_info.get("author_name", "")[0],
                        "ratings_average": str(average),
                        "ratings_count": str(book_info.get("ratings_count", "")),
                        "number_of_pages_median": str(book_info.get("number_of_pages_median", "")),
                        "first_publish_year": str(book_info.get("first_publish_year", "")),
                        "ratings_average": str(book_info.get("ratings_average", "")),
                        "ratings_count": str(book_info.get("ratings_count", "")),
                        "ratings_count_1": str(book_info.get("ratings_count_1", "")),
                        "ratings_count_2": str(book_info.get("ratings_count_2", "")),
                        "ratings_count_3": str(book_info.get("ratings_count_3", "")),
                        "ratings_count_4": str(book_info.get("ratings_count_4", "")),
                        "ratings_count_5": str(book_info.get("ratings_count_5", ""))      
                    } 

        except httpx.RequestError as e:
            print(f"An error occurred while making the request: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")

        return results


class BookSearchApp:
    """
    Application to perform book searches and enrich results using the Open Library API.

    Attributes:
        service (OpenLibraryService): The service used to interact with the Open Library API.
        response_with_books (ResponseWithBooks): The initial response containing books to be enriched.
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
                res["brief_description"] = book.brief_description
                res["isbn"] = book.isbn

                enriched_book = Book(**res)
                result.append(enriched_book)

        return ResponseWithBooks(
            books=result,
            further_chat=self.response_with_books.further_chat
        )
