"""
Prompt Augmentation for Book Search Queries

This module provides utilities to generate detailed and structured prompts for 
querying a book recommendation system (e.g., ChatGPT). The generated prompts 
ensure that responses adhere to a specific JSON format, making it easier to 
parse and use the results in downstream applications.
"""


# --- Prompt Augmentor ---
class AugmentPrompt:
    """
    A utility class to generate augmented prompts for book search queries.

    This class provides a static method to create a well-structured prompt 
    for querying a book recommendation system (e.g., ChatGPT). The prompt 
    ensures that the system returns responses in a specific JSON format 
    tailored to the needs of the application.

    Features:
    ----------
    - Generates prompts that require responses in JSON format.
    - Specifies the structure of the JSON response, including required fields.
    - Handles special cases, such as no matches found.
    """

    @staticmethod
    def generate(prompt: str) -> str:
        """
        Generate an augmented prompt for a book search query.

        This method constructs a detailed prompt that instructs the system 
        to return a JSON-formatted response with specific fields, including:
        - A list of books with their title, author name, and a brief description.
        - A message offering further assistance.

        Special Instructions:
        - If no books match the query, the response should include a 
          "no_matches_found" field explaining why no recommendations could be made.
        - The response must not include markdown, triple backticks, or any 
          other non-JSON formatting.

        Args:
            prompt (str): The user's book search query.

        Returns:
            str: A detailed prompt string tailored for the book recommendation system.
        """

        return f"""
Provide an answer to the following book search query:

'{prompt}'.

Important: If the above query mentions "a book" or "one book" - then return info about only 1 book.

Important: Return the response in plain JSON format.

The JSON must include:
1. A field called "books" with a value that is a list of dictionaries.
   Each dictionary should have the following fields:
   - "title" (which will contain book title)
   - "author_name"
   - "isbn"
   - "brief_description" (about 50 words).

2. An additional field, "further_chat" that contains a message offering further assistance in finding suitable books. Be creative to choose a proper text in this field. It should be relevant to the current request.

Special cases:
- If there are no books to recommend, respond in JSON with the field "no_matches_found" - in which explain why you couldn't find any books for this query.

Ensure the response:
- Contains only JSON as plain text.
- Does not include markdown or triple backticks under any circumstances.
"""
