"""
This module provides functionality for async retrieval of data from an API.
It includes a class, `RetrieveAsync`, which uses async communication to
efficiently fetch data for multiple items, such as book ISBNs, from an
external API.
"""

import asyncio
import httpx
import time
import traceback


class RetrieveAsync:
    """
    A class to retrieve data concurrently using HTTP requests.

    This class is designed to fetch data from an external API for a list of items (e.g., ISBNs)
    while utilizing multithreading for high performance.
    """

    def __init__(self):
        """
        Initializes the RetrieveConcurrent instance.

        Attributes:
            results (dict): A dictionary to store the retrieval status and response for each item.
                            The keys are the item identifiers (e.g., ISBNs), and the values are
                            lists containing the retrieval status (bool) and the HTTP response object.
        """
        self.results = {}

    async def retrieve_data(self, isbn):
        """
        Fetches data for a single item (e.g., ISBN) from the external API.

        Args:
            isbn (str): The identifier for the item to retrieve, such as an
                        ISBN number.

        Side Effects:
            Updates the `results` dictionary with the retrieval status and
            response.

        Notes:
            - The method uses the `httpx` library to send GET requests.
            - If an exception occurs during the request, it logs the error
              and sets the retrieval status to False.
        """
        base_url = "https://openlibrary.org/search.json"
        params = {"isbn": isbn}
        retrieved = False
        response = None
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(base_url, params=params, timeout=5.0)
                retrieved = True
            except Exception as e:
                print(f"Failed to retrieve. Error: {e}")
        self.results[isbn] = [retrieved, response]

    async def retrieve_bunch(self, isbn_list):
        """
        Fetches data for a list of items concurrently.

        Args:
            isbn_list (list of str): A list of item identifiers (e.g., ISBNs)
            to retrieve.

        Returns:
            dict: A dictionary containing the retrieval status and responses
                  for all requested items.

        Side Effects:
            Prints the total elapsed time for retrieving data.
        """
        start_time = time.time()
        tasks = [self.retrieve_data(isbn) for isbn in isbn_list]
        await asyncio.gather(*tasks)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(elapsed_time)
        return self.results
