# database.py

import chromadb
from chromadb.utils import embedding_functions
import base64

# Initialize ChromaDB client
chroma_client = chromadb.Client()

# Create or get the collection
collection = chroma_client.get_or_create_collection(
    name="wardrobe_items",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
)

def store_item(description, image_bytes):
    # Convert image to base64 for storage
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Store in ChromaDB
    collection.add(
        documents=[description],
        metadatas=[{"image": image_base64}],
        ids=[f"item_{collection.count() + 1}"]
    )

def get_all_items():
    # Retrieve all items from the collection
    results = collection.get(include=['metadatas', 'documents'])
    
    items = []
    for i, doc in enumerate(results['documents']):
        items.append({
            'description': doc,
            'image': base64.b64decode(results['metadatas'][i]['image'])
        })
    
    return items

def search_items(query, n_results=5):
    # Search for similar items
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=['metadatas', 'documents']
    )
    
    items = []
    for i, doc in enumerate(results['documents'][0]):
        items.append({
            'description': doc,
            'image': base64.b64decode(results['metadatas'][0][i]['image'])
        })
    
    return items

# Example usage:
# store_item("A red t-shirt with a crew neck", image_bytes)
# all_items = get_all_items()
# similar_items = search_items("casual blue shirt")