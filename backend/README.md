# Book Info Backend

This repository contains the backend service for the "Book Info" application. The backend provides an API to search for books based on user queries.

## Running the Backend

To run the backend, you can use Docker. Make sure you have Docker installed on your machine.

### Steps to Run the Backend

1. Navigate to the `book-info/backend` directory.
2. Ensure that a Docker-compatible application (e.g., Docker Desktop, Docker Engine) is running.
3. docker build -t book-info-frontend-prod .
3. Run the following command to start the backend container:

   Option 1 (docker):

   ```bash
   docker run -d -p 8000:8000 --name search-books-backend -e OPENAI_API_KEY="<your-ChatGPT-API-Key>" search-books-backend
   ```

   **Note:** Replace the `OPENAI_API_KEY` value with your actual API key.

   Option 2 (using uvicorn. **Note:** You should install libs from **requirements.txt** in advance):

   ```bash
   OPENAI_API_KEY="<your-ChatGPT-API-Key>" uvicorn main:app --host 0.0.0.0 --port 8000 --workers 5
   ```

4. Verify that the container is running by checking the logs or accessing the API.

## Using the Search API

The backend exposes an endpoint to search for books. You can use `curl` to make a POST request to this endpoint.

### Example Request

```bash
curl -X POST http://localhost:8000/search-books \
   -H "Content-Type: application/json" \
   -d '{"query": "3 books about adventures and nature", "session_id": "777"}'
```

### Example Response

```json
{
  "books": [
    {
      "title": "Into the Wild",
      "author_name": "Jon Krakauer",
      "brief_description": "This captivating book chronicles the real-life story of Christopher McCandless, a young man who abandons society to live in the Alaskan wilderness, highlighting themes of adventure, nature, and the search for personal meaning.",
      "number_of_pages_median": 224,
      "first_publish_year": 1996,
      "ratings_average": 3.83,
      "ratings_count": 64,
      "ratings_count_1": 2,
      "ratings_count_2": 4,
      "ratings_count_3": 11,
      "ratings_count_4": 33,
      "ratings_count_5": 14
    },
    {
      "title": "Wild",
      "author_name": "Cheryl Strayed",
      "brief_description": "A thrilling memoir about Cheryl Strayed's 1,100-mile solo hike along the Pacific Crest Trail, delving into her encounters with the rugged beauty of nature and her journey of self-discovery and healing.",
      "number_of_pages_median": 318,
      "first_publish_year": 2012,
      "ratings_average": 3.0,
      "ratings_count": 1,
      "ratings_count_1": 0,
      "ratings_count_2": 0,
      "ratings_count_3": 1,
      "ratings_count_4": 0,
      "ratings_count_5": 0
    },
    {
      "title": "A Walk in the Woods",
      "author_name": "Bill Bryson",
      "brief_description": "This humorous and insightful book follows Bill Bryson's attempt to hike the Appalachian Trail, weaving in the natural history and challenges of trekking through some of America's most untouched landscapes.",
      "number_of_pages_median": 328,
      "first_publish_year": 1997,
      "ratings_average": 3.95,
      "ratings_count": 59,
      "ratings_count_1": 2,
      "ratings_count_2": 0,
      "ratings_count_3": 14,
      "ratings_count_4": 26,
      "ratings_count_5": 17
    }
  ],
  "further_chat": "If you're ready for more thrilling tales or seeking stories from different terrains, just let me know. Adventure awaits with countless trails to explore through the pages!"
}
```

## Notes

- Ensure that the `OPENAI_API_KEY` environment variable is set correctly for the backend to function.
- The example response demonstrates the kind of book information returned by the API, including titles, authors, descriptions, and ratings.

