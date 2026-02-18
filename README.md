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

Set your Azure OpenAI embedding configuration:

```bash
export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com"
export AZURE_OPENAI_API_KEY="<your-api-key>"
export AZURE_OPENAI_EMBEDDING_DEPLOYMENT="<your-embedding-deployment-name>"
# Optional (defaults to 2024-02-01)
export AZURE_OPENAI_API_VERSION="2024-02-01"
```

Then execute the main script:

```bash
python main.py
```

The script will prompt you to choose which operations to run (`all` or a comma-separated list such as `create,read,search`).
- For **search**, the script asks for search text at runtime.
- For all other operations, the script uses hard-coded sample article data.

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
- **Insert**: Add 4 sample articles with Azure OpenAI embedding vectors
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
3. **Use your preferred embeddings setup** (this demo uses Azure OpenAI embeddings by default)
4. **Add more operations** like batch operations, complex filters, or aggregations

## Learn More

- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [Weaviate Python Client](https://weaviate.io/developers/weaviate/client-libraries/python)
- [Vector Databases Explained](https://weaviate.io/blog/what-is-a-vector-database)

## License

MIT
