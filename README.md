# Weaviate Demo - Basic Operations

A basic Python application demonstrating fundamental CRUD operations and vector search with Weaviate vector database.

## Features

This demo application showcases:
- **CREATE**: Insert data objects with vector embeddings
- **READ**: Query and retrieve data with and without filters
- **UPDATE**: Modify existing data objects
- **DELETE**: Remove data objects
- **Vector Search**: Perform similarity searches using vector embeddings
- **Schema Management**: Create and manage collections

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ravividap/weaviate-demo.git
cd weaviate-demo
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Start Weaviate Instance

Start a local Weaviate instance using Docker Compose:

```bash
docker-compose up -d
```

This will start Weaviate on `http://localhost:8080`

### 2. Run the Demo Application

Execute the main script to see all basic operations in action:

```bash
python main.py
```

The script will:
1. Connect to the local Weaviate instance
2. Create a schema for storing articles
3. Insert sample articles with vector embeddings
4. Query and display all articles
5. Filter articles by category
6. Update an article's properties
7. Perform vector similarity search
8. Delete an article
9. Display final statistics

### 3. Stop Weaviate Instance

When you're done, stop the Weaviate instance:

```bash
docker-compose down
```

To also remove the data volume:

```bash
docker-compose down -v
```

## Project Structure

```
weaviate-demo/
├── main.py              # Main application with all operations
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker configuration for Weaviate
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## What's Demonstrated

### Schema Creation
Creates a collection called "Article" with properties: title, content, author, and category.

### Data Operations
- **Insert**: Add 4 sample articles with placeholder vectors
- **Query**: Fetch all articles and display their properties
- **Filter**: Query articles by specific category
- **Update**: Modify article properties (content and category)
- **Delete**: Remove an article from the collection

### Vector Search
Performs similarity search using vector embeddings to find related articles.

## Customization

To customize the demo for your use case:

1. **Modify the schema** in the `create_schema()` function to add/remove properties
2. **Add your data** in the `create_data()` function
3. **Use real embeddings** instead of placeholder vectors (integrate with OpenAI, Cohere, etc.)
4. **Add more operations** like batch operations, complex filters, or aggregations

## Learn More

- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [Weaviate Python Client](https://weaviate.io/developers/weaviate/client-libraries/python)
- [Vector Databases Explained](https://weaviate.io/blog/what-is-a-vector-database)

## License

MIT