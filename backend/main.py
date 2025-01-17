"""
Book Search Service API

This module implements a FastAPI-based backend service for querying book recommendations
and extended book data using OpenAI's GPT-based language model and the Open Library API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from types import SimpleNamespace
from typing import Union

from better_profanity import profanity


from chatgpt_client import ChatGPTClient
from data_models import (
    ResponseNoMatchesFound,
    ResponseProfanityFound,
    QueryRequest,
    Book,
    ResponseWithBooks
)
from open_library import BookSearchApp
from utils import ParseResponse


# Create your FastAPI application
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

gpt_client = ChatGPTClient()
profanity.load_censor_words()
parser = ParseResponse()


@app.post(
    "/search-books",
    response_model=Union[
        ResponseWithBooks,
        ResponseNoMatchesFound,
        ResponseProfanityFound
    ]
)
async def search_books(request: QueryRequest):
    """
    Book search API endpoint.

    This endpoint processes user book search queries and provides appropriate responses based on the query. 
    It performs the following steps:
        1. Checks for profanity in the query.
        2. Uses ChatGPT to generate a list of book recommendations.
        3. Fetches extended book data from OpenLibrary for each recommended book.
        4. Returns a structured response.

    Args:
        request (QueryRequest): The user's search query and session information.

    Returns:
        Union[ResponseWithBooks, ResponseNoMatchesFound, ResponseProfanityFound]:
            - ResponseWithBooks: A response containing a list of recommended books and further assistance.
            - ResponseNoMatchesFound: A response indicating no matches were found for the query.
            - ResponseProfanityFound: A response indicating that profanity was detected in the query.

    Raises:
        HTTPException: If an unexpected error occurs during the request processing.
    """

    # 1) Profanity check
    if profanity.contains_profanity(request.query):
        return ResponseProfanityFound(
            profanity_found=(
                "Please note that this Book Search service is moderated "
                "and does not tolerate the use of profanity."
            )
        )

    # 2) Get ChatGPT's response (asynchronously)
    raw_response = await gpt_client.send_prompt(request.session_id, request.query)
    parsed = parser.run(raw_response)

    # 3a) If ChatGPT returned a JSON with "books"
    if parsed.is_json and "books" in parsed.data:
        # Rehydrate into Pydantic Book models
        books = [Book(**item) for item in parsed.data["books"]]
        response_with_books = ResponseWithBooks(
            books=books,
            further_chat=parsed.data["further_chat"]
        )

        book_app = BookSearchApp(
            response_with_books=response_with_books
        )

        try:
            # 4) Call the async method that fetches data concurrently
            result = await book_app.search_books()
            return result
        except:
            return response_with_books

    # 5) If ChatGPT returned a JSON with "no_matches_found"
    if parsed.is_json and "no_matches_found" in parsed.data:
        return ResponseNoMatchesFound(**parsed.data)
    return response_with_books
