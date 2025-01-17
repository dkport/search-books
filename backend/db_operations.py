"""
Module for handling MongoDB operations with SOLID principles.
This module includes:
- MongoDBClient: Handles direct interactions with MongoDB.
- JsonRepository: Manages saving and retrieving JSON objects using MongoDBClient.
"""

from datetime import datetime, timezone
from pymongo import MongoClient, ASCENDING


class MongoDBClient:
    """
    A client for interacting with a MongoDB collection.

    Attributes:
        client (MongoClient): The MongoDB client instance.
        db (Database): The MongoDB database instance.
        collection (Collection): The MongoDB collection instance.
    """

    def __init__(self, connection_string, database_name, collection_name):
        """
        Initialize the MongoDBClient with connection details.

        :param connection_string: The MongoDB connection string.
        :param database_name: The name of the MongoDB database.
        :param collection_name: The name of the MongoDB collection.
        """
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self._ttl = 2 * 24 * 60 * 60
        self._create_ttl_index()

    def _create_ttl_index(self):
        """
        Create a TTL index on the `timestamp` field to expire documents.
        If the index already exists with different options, it will be dropped and recreated.
        """
        existing_indexes = list(self.collection.list_indexes())
        for index in existing_indexes:
            if index.get("name") == "timestamp_1":
                # Check if the current index matches the desired expireAfterSeconds
                if index.get("expireAfterSeconds") != self._ttl:
                    print("Dropping existing TTL index with different options...")
                    self.collection.drop_index("timestamp_1")
                    break

        # Create the new TTL index
        self.collection.create_index(
            [("timestamp", ASCENDING)],
            expireAfterSeconds=self._ttl
        )
        print("TTL index created or updated successfully.")

    def save_document(self, document):
        """
        Save a document to the MongoDB collection.

        :param document: The document to save.
        :return: The ID of the inserted document.
        """
        result = self.collection.insert_one(document)
        return result.inserted_id

    def find_document(self, query):
        """
        Find a document in the MongoDB collection by query.

        :param query: The query to find the document.
        :return: The document if found, otherwise None.
        """
        return self.collection.find_one(query)


class Repository:
    """
    A repository for managing JSON objects using a MongoDBClient.

    Attributes:
        db_client (MongoDBClient): The MongoDB client for database operations.
    """

    def __init__(self, db_client):
        """
        Initialize the JsonRepository with a MongoDB client.

        :param db_client: An instance of MongoDBClient.
        """
        self.db_client = db_client

    def save_json(self, session_id, json_data):
        """
        Save a JSON object to the MongoDB collection. If a document with the same
        session_id exists, it will be updated; otherwise, a new document will be inserted.

        :param session_id: Unique session identifier.
        :param json_data: JSON object to save.
        """
        query = {"session_id": session_id}
        update = {
            "$set": {
                "data": json_data,
                "timestamp": datetime.now(timezone.utc)
            }
        }
        result = self.db_client.collection.update_one(query, update, upsert=True)
        
        if result.upserted_id:
            print(f"Document inserted with ID: {result.upserted_id}")
        else:
            print(f"Document updated for session_id: {session_id}")

    def retrieve_json(self, session_id):
        """
        Retrieve a JSON object from the MongoDB collection by session_id.

        :param session_id: Unique session identifier.
        :return: JSON object or None if not found.
        """
        document = self.db_client.find_document({"session_id": session_id})
        if document:
            return document.get("data")
        else:
            print("No document found for the given session_id.")
            return None


class DBOperations:
    """
    Application class to demonstrate usage of MongoDBClient and JsonRepository.
    """

    def __init__(self):
        """
        Initialize the application with MongoDB connection details.

        :param connection_string: The MongoDB connection string.
        :param database_name: The name of the MongoDB database.
        :param collection_name: The name of the MongoDB collection.
        """
        self.connection_string = "mongodb://localhost:27017/"
        self.database_name = "search_books"
        self.collection_name = "correspondence"
        self.db_client = MongoDBClient(
            self.connection_string,
            self.database_name,
            self.collection_name)
        self.json_repo = Repository(self.db_client)

    def upsert(self, session_id, data):
        """Update/Insert data"""
        self.json_repo.save_json(session_id, data)

    def retrieve(self, session_id):
        """Retrieve the JSON object"""
        doc = self.json_repo.retrieve_json(session_id)
        return doc if doc else {}
