"""
Data Models for Book Search API

This module defines data models used for request validation, response structuring, 
and error handling in a book search API. The models are implemented using `pydantic`, 
ensuring type validation and easy integration with FastAPI or other Python frameworks.
"""


from pydantic import BaseModel
from typing import List, Optional


class ResponseNoMatchesFound(BaseModel):
    """
    Represents a response indicating that no matches were found for the book search query.

    Attributes:
        no_matches_found (str): A message explaining why no books were found.
    """
    no_matches_found: str


class ResponseProfanityFound(BaseModel):
    """
    Represents a response indicating that profanity was detected in the search
    query.

    Attributes:
        profanity_found (str): A message informing the user about the presence
        of profanity in their query.
    """
    profanity_found: str


class QueryRequest(BaseModel):
    """
    Represents a book search query submitted by user.

    Attributes:
        session_id (str): A unique identifier for the user session.
        query (str): The search query entered by the user.
    """
    session_id: str
    query: str


class Book(BaseModel):
    """
    Represents a book and its associated metadata.

    Attributes:
        title (str): The title of the book.
        author_name (str): The name of the book's author.
        brief_description (str): A short description of the book.
        isbn (Optional[str]): The median number of pages in the book.
        number_of_pages_median (Optional[str]): Median number of pages.
        first_publish_year (Optional[str]): Year the book was first published.
        ratings_average (Optional[str]): The average user rating for the book.
        ratings_count (Optional[str]): The total number of user ratings.
        ratings_count_1 (Optional[str]): The count of 1-star ratings.
        ratings_count_2 (Optional[str]): The count of 2-star ratings.
        ratings_count_3 (Optional[str]): The count of 3-star ratings.
        ratings_count_4 (Optional[str]): The count of 4-star ratings.
        ratings_count_5 (Optional[str]): The count of 5-star ratings.
    """
    title: str
    author_name: str
    brief_description: str
    isbn: Optional[str]
    number_of_pages_median: Optional[str] = None
    first_publish_year: Optional[str] = None
    ratings_average: Optional[str] = None
    ratings_count: Optional[str] = None
    ratings_count_1: Optional[str] = None
    ratings_count_2: Optional[str] = None
    ratings_count_3: Optional[str] = None
    ratings_count_4: Optional[str] = None
    ratings_count_5: Optional[str] = None


class ResponseWithBooks(BaseModel):
    """
    Represents a response containing a list of books and an optional
    follow-up message.

    Attributes:
        books (List[Book]): A list of books recommended based on the user's
        query.
        further_chat (Optional[str]): A follow-up message offering additional
        assistance or information.
    """
    books: List[Book]
    further_chat: Optional[str] = None
