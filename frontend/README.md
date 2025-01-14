# React App - Book Info Frontend

This repository contains the React-based frontend for the "Book Info" application. The app is containerized using Docker for easy deployment and runs on port 80.

## Prerequisites

- Docker installed on your machine.

## Building and Running the App

Follow these steps to build and run the React app inside a Docker container:

### Build the Docker Image

Run the following command to build the Docker image:

```bash
docker build -t search-books-frontend .
```

### Run the Docker Container

Run the container and map it to port 80:

```bash
docker run -d -p 80:80 --name search-books-frontend search-books-frontend
```

## Accessing the Application

Once the container is running, open your web browser and navigate to:

```
http://localhost:80
```

You should now see the "Book Info" frontend application.

## Notes

- Ensure port 80 is available on your machine.
- Use `docker ps` to verify the container is running.
- To stop the container, use the following command:

  ```bash
  docker stop search-books-frontend
  ```

- To remove the container, use:

  ```bash
  docker rm search-books-frontend
  ```

Happy searches!

