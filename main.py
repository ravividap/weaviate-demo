"""
Weaviate Demo - Basic Operations
This script demonstrates basic CRUD operations and vector search with Weaviate.
"""

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery
import os
from langchain_openai import AzureOpenAIEmbeddings


def get_azure_openai_embedding(text):
    """Generate an embedding using an Azure OpenAI deployment."""
    required_env_vars = (
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
        "AZURE_OPENAI_API_KEY",
    )
    missing_env_vars = [name for name in required_env_vars if not os.environ.get(name)]
    if missing_env_vars:
        raise RuntimeError(
            "Missing required Azure OpenAI environment variables: "
            + ", ".join(missing_env_vars)
        )

    embeddings_client = AzureOpenAIEmbeddings(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/"),
        azure_deployment=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    )
    return embeddings_client.embed_query(text)


def connect_to_weaviate():
    """Connect to Weaviate instance."""
    print("Connecting to Weaviate at http://localhost:8080...")
    client = weaviate.connect_to_local(host="localhost", port=8080)
    print("✓ Connected to Weaviate successfully!")
    return client


def create_schema(client):
    """Create a collection schema for storing articles."""
    print("\n=== Creating Schema ===")
    
    # Delete collection if it exists
    if client.collections.exists("Article"):
        client.collections.delete("Article")
        print("Deleted existing Article collection")
    
    # Create collection
    articles = client.collections.create(
        name="Article",
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="content", data_type=DataType.TEXT),
            Property(name="author", data_type=DataType.TEXT),
            Property(name="category", data_type=DataType.TEXT),
        ],
        vectorizer_config=Configure.Vectorizer.none()
    )
    
    print("✓ Created 'Article' collection with properties: title, content, author, category")
    return articles


def create_data(client):
    """Insert sample data into the collection (CREATE operation)."""
    print("\n=== Creating Data (INSERT) ===")
    
    articles = client.collections.get("Article")
    
    # Sample articles
    sample_articles = [
        {
            "title": "Introduction to Vector Databases",
            "content": "Vector databases are specialized databases designed to store and query high-dimensional vectors efficiently.",
            "author": "John Doe",
            "category": "Technology"
        },
        {
            "title": "Getting Started with Weaviate",
            "content": "Weaviate is an open-source vector database that allows you to store data objects and vector embeddings.",
            "author": "Jane Smith",
            "category": "Tutorial"
        },
        {
            "title": "Machine Learning Basics",
            "content": "Machine learning is a subset of artificial intelligence that focuses on building systems that learn from data.",
            "author": "Bob Johnson",
            "category": "AI"
        },
        {
            "title": "Python for Data Science",
            "content": "Python has become the de facto language for data science due to its rich ecosystem of libraries.",
            "author": "Alice Williams",
            "category": "Programming"
        }
    ]
    
    # Insert data with vectors
    inserted_uuids = []
    for article in sample_articles:
        vector = get_azure_openai_embedding(f"{article['title']}\n{article['content']}")
        
        uuid = articles.data.insert(
            properties=article,
            vector=vector
        )
        inserted_uuids.append(uuid)
        print(f"✓ Inserted article: '{article['title']}' with UUID: {uuid}")
    
    return inserted_uuids


def read_data(client):
    """Query and retrieve data (READ operation)."""
    print("\n=== Reading Data (QUERY) ===")
    
    articles = client.collections.get("Article")
    
    # Fetch all articles
    print("\nFetching all articles:")
    response = articles.query.fetch_objects(limit=10)
    
    for i, obj in enumerate(response.objects, 1):
        print(f"\n{i}. {obj.properties['title']}")
        print(f"   Author: {obj.properties['author']}")
        print(f"   Category: {obj.properties['category']}")
        print(f"   UUID: {obj.uuid}")
    
    return response.objects


def read_data_with_filter(client):
    """Query data with filters."""
    print("\n=== Reading Data with Filters ===")
    
    articles = client.collections.get("Article")
    
    # Filter by category
    print("\nFiltering articles by category='Technology':")
    response = articles.query.fetch_objects(
        filters=weaviate.classes.query.Filter.by_property("category").equal("Technology"),
        limit=10
    )
    
    for obj in response.objects:
        print(f"✓ {obj.properties['title']} (Category: {obj.properties['category']})")
    
    return response.objects


def update_data(client, uuid):
    """Update existing data (UPDATE operation)."""
    print("\n=== Updating Data (UPDATE) ===")
    
    articles = client.collections.get("Article")
    
    # Update article properties
    print(f"Updating article with UUID: {uuid}")
    articles.data.update(
        uuid=uuid,
        properties={
            "content": "Vector databases are specialized databases designed to store and query high-dimensional vectors efficiently. They are essential for modern AI applications.",
            "category": "Database"
        }
    )
    
    print("✓ Updated article content and category")
    
    # Verify update
    obj = articles.query.fetch_object_by_id(uuid)
    print(f"✓ Verified: '{obj.properties['title']}' now has category='{obj.properties['category']}'")


def delete_data(client, uuid):
    """Delete data (DELETE operation)."""
    print("\n=== Deleting Data (DELETE) ===")
    
    articles = client.collections.get("Article")
    
    # Get article title before deletion
    obj = articles.query.fetch_object_by_id(uuid)
    title = obj.properties['title']
    
    # Delete the article
    articles.data.delete_by_id(uuid)
    print(f"✓ Deleted article: '{title}' (UUID: {uuid})")


def vector_search(client, search_text):
    """Perform vector similarity search."""
    print("\n=== Vector Search ===")
    
    articles = client.collections.get("Article")
    
    query_vector = get_azure_openai_embedding(search_text)
    
    print(f"Performing vector similarity search for: '{search_text}'")
    response = articles.query.near_vector(
        near_vector=query_vector,
        limit=3,
        return_metadata=MetadataQuery(distance=True)
    )
    
    print(f"\nTop 3 similar articles:")
    for i, obj in enumerate(response.objects, 1):
        distance = obj.metadata.distance if obj.metadata.distance else "N/A"
        print(f"{i}. {obj.properties['title']}")
        print(f"   Distance: {distance}")
        print(f"   Author: {obj.properties['author']}")


def get_collection_info(client):
    """Get information about the collection."""
    print("\n=== Collection Information ===")
    
    articles = client.collections.get("Article")
    
    # Get aggregate information
    response = articles.aggregate.over_all(total_count=True)
    print(f"Total articles in collection: {response.total_count}")


def main():
    """Main function to demonstrate all operations."""
    print("=" * 60)

    available_operations = ["create", "read", "filter", "info", "update", "search", "delete"]
    selected_input = input(
        "Choose operations to run (comma-separated, or 'all'): "
    ).strip().lower()
    if not selected_input or selected_input == "all":
        selected_operations = set(available_operations)
    else:
        selected_operations = {op.strip() for op in selected_input.split(",") if op.strip()}
        if not selected_operations:
            raise ValueError("No valid operations were provided. Use 'all' or a comma-separated list.")
        invalid_operations = selected_operations - set(available_operations)
        if invalid_operations:
            raise ValueError(
                f"Invalid operation(s): {', '.join(sorted(invalid_operations))}. "
                f"Valid options: {', '.join(available_operations)}, all"
            )
    print("WEAVIATE DEMO - BASIC OPERATIONS")
    print("=" * 60)
    
    try:
        # Connect to Weaviate
        client = connect_to_weaviate()
        
        uuids = []
        create_schema(client)

        if "create" in selected_operations:
            uuids = create_data(client)

        if "read" in selected_operations:
            read_data(client)

        if "filter" in selected_operations:
            read_data_with_filter(client)

        if "info" in selected_operations:
            get_collection_info(client)

        if "update" in selected_operations:
            if uuids:
                update_data(client, uuids[0])
            else:
                print("Skipping update: no inserted articles available in this run")

        if "search" in selected_operations:
            search_text = input("Enter text to search for similar articles: ").strip()
            if search_text:
                vector_search(client, search_text)
            else:
                print("Skipping search: no query text provided")

        if "delete" in selected_operations:
            if len(uuids) > 1:
                delete_data(client, uuids[-1])
            else:
                print("Skipping delete: no inserted articles available in this run")

        if {"create", "delete", "update", "info"} & selected_operations:
            get_collection_info(client)
        
        print("\n" + "=" * 60)
        print("✓ All operations completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Close connection
        if 'client' in locals():
            client.close()
            print("\n✓ Connection closed")


if __name__ == "__main__":
    main()
