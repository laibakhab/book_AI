"""
Script to check the contents of the Qdrant collection.
"""

import sys
sys.path.append('.')

from clients.qdrant_client import QdrantClientWrapper
from config.settings import settings

# Initialize Qdrant client
qdrant_client = QdrantClientWrapper()

# Get collection info
collection_name = settings.QDRANT_COLLECTION
print(f"Checking collection: {collection_name}")

try:
    collection_info = qdrant_client.get_collection_info(collection_name)
    if collection_info:
        print(f"Collection exists with info: {collection_info}")
    else:
        print("Could not get collection info")
        
    # Check how many points are in the collection
    from qdrant_client.http import models
    
    # Count points in collection
    count = qdrant_client.client.count(
        collection_name=collection_name
    )
    
    print(f"Number of points in collection: {count.count}")
    
    # Get a sample of points if any exist
    if count.count > 0:
        print("\nSample points from collection:")
        records, _ = qdrant_client.client.scroll(
            collection_name=collection_name,
            limit=3,
            with_payload=True,
            with_vectors=False
        )
        
        for i, record in enumerate(records):
            print(f"Point {i+1}:")
            print(f"  ID: {record.id}")
            print(f"  Payload text (first 100 chars): {record.payload.get('text', '')[:100]}...")
            print(f"  Title: {record.payload.get('title', 'N/A')}")
            print()
    else:
        print("No points found in the collection")
        
except Exception as e:
    print(f"Error accessing collection: {str(e)}")