"""
Script to ingest your own book documents into the Qdrant vector database for the RAG system.
This script will read all text files in the 'books' directory and process them.
"""

import os
import time
import logging
from typing import List, Dict, Any
from pathlib import Path

# Add the backend directory to the path to import our modules
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

from clients.cohere_client import CohereClient
from clients.qdrant_client import QdrantClientWrapper
from config.settings import settings


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def chunk_text(text: str, max_chunk_size: int = 512) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: The text to chunk
        max_chunk_size: Maximum size of each chunk in characters

    Returns:
        List of text chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chunk_size

        # If we're not at the end and we're in the middle of a word, try to find a sentence boundary
        if end < len(text):
            # Look for a sentence break near the end
            sub_text = text[start:end]
            last_sentence_break = max(
                sub_text.rfind('. ') + 2,
                sub_text.rfind('! ') + 2,
                sub_text.rfind('? ') + 2
            )

            if last_sentence_break > len(sub_text) // 2:  # Only use if it's not too close to the start
                end = start + last_sentence_break
            else:
                # If no good sentence break found, look for a word boundary
                last_space = sub_text.rfind(' ')
                if last_space > len(sub_text) // 2:
                    end = start + last_space

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move to the next chunk, with some overlap
        start = end - max_chunk_size // 4  # 25% overlap

    return chunks


def read_book_documents(book_dir: str = "books") -> List[Dict[str, Any]]:
    """
    Read book documents from the specified directory to index in the vector database.
    Supports .txt and .md files.

    Args:
        book_dir: Directory containing book files

    Returns:
        List of document dictionaries with text content and metadata
    """
    documents = []
    
    book_path = Path(book_dir)
    if not book_path.exists():
        logger.warning(f"Directory '{book_dir}' does not exist. Creating it...")
        book_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Please add your book files (txt, md) to the '{book_dir}' directory.")
        return documents

    # Get all .txt and .md files from the books directory
    book_files = list(book_path.glob("*.txt")) + list(book_path.glob("*.md"))
    
    if not book_files:
        logger.warning(f"No text or markdown files found in '{book_dir}' directory.")
        logger.info(f"Please add your book files (with .txt or .md extensions) to the '{book_dir}' directory.")
        return documents

    for book_file in book_files:
        try:
            logger.info(f"Reading book file: {book_file}")
            
            # Read the content of the book file
            with open(book_file, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            if len(text_content.strip()) == 0:
                logger.warning(f"Skipping empty file: {book_file}")
                continue
                
            # Create document entry
            document = {
                "text": text_content,
                "source": str(book_file.name),
                "title": book_file.stem,  # filename without extension
                "url": f"file://{book_file}",
                "page_number": 1
            }
            
            documents.append(document)
            logger.info(f"Loaded {len(text_content)} characters from {book_file.name}")
            
        except Exception as e:
            logger.error(f"Error reading file {book_file}: {str(e)}")
            continue

    return documents


def ingest_documents(collection_name: str = None):
    """
    Main function to ingest your book documents into Qdrant.

    Args:
        collection_name: Name of the Qdrant collection to use
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION

    logger.info(f"Starting document ingestion into collection: {collection_name}")

    try:
        # Initialize clients - use the same model as specified in settings
        cohere_client = CohereClient(model_name=settings.COHERE_MODEL)
        qdrant_client = QdrantClientWrapper()  # This will use the default vector size of 4096

        # Ensure the collection exists with the correct vector dimensions
        qdrant_client.ensure_collection_exists(collection_name, recreate_if_exists=True)  # Recreate to ensure correct size

        # Read documents from your books directory
        documents = read_book_documents("books")
        
        if not documents:
            logger.error("No documents found to ingest. Please add .txt or .md files to the 'books' directory.")
            return

        logger.info(f"Loaded {len(documents)} documents for ingestion")

        # Process and index each document
        all_chunks_and_embeddings = []

        for doc_idx, doc in enumerate(documents):
            logger.info(f"Processing document {doc_idx + 1}/{len(documents)}: {doc['title']}")

            # Chunk the document text
            chunks = chunk_text(doc["text"], max_chunk_size=512)
            logger.info(f"  Chunked document into {len(chunks)} chunks")

            # Generate embeddings for chunks
            chunk_texts = [chunk for chunk in chunks]
            embeddings = cohere_client.generate_embeddings(chunk_texts)

            # Verify embedding dimensions are consistent
            if embeddings:
                logger.info(f"    First embedding dimension: {len(embeddings[0])}")

            # Prepare points for Qdrant
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                # Use a numeric ID as Qdrant expects numeric or UUID IDs
                point_id = doc_idx * 1000 + i  # Create unique numeric ID
                point = {
                    "id": point_id,
                    "vector": embedding,
                    "payload": {
                        "text": chunk,
                        "source": doc["source"],
                        "title": doc["title"],
                        "url": doc["url"],
                        "page_number": doc["page_number"],
                        "doc_id": doc_idx,
                        "chunk_id": i
                    }
                }
                all_chunks_and_embeddings.append(point)

        # Upload all points to Qdrant
        logger.info(f"Uploading {len(all_chunks_and_embeddings)} vectors to Qdrant...")

        points = []
        for item in all_chunks_and_embeddings:
            from qdrant_client.http import models
            point = models.PointStruct(
                id=item["id"],
                vector=item["vector"],
                payload=item["payload"]
            )
            points.append(point)

        # Upload in batches
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            qdrant_client.client.upsert(
                collection_name=collection_name,
                points=batch
            )
            logger.info(f"  Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")
            time.sleep(0.1)  # Small delay to avoid overwhelming the API

        logger.info(f"Successfully ingested {len(all_chunks_and_embeddings)} vectors into collection '{collection_name}'")
        logger.info(f"Documents indexed: {len(documents)}")

    except Exception as e:
        logger.error(f"Error during document ingestion: {str(e)}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest your book documents into the Qdrant vector database")
    parser.add_argument("--collection", type=str, default=settings.QDRANT_COLLECTION,
                        help=f"Name of the Qdrant collection to use (default: '{settings.QDRANT_COLLECTION}')")

    args = parser.parse_args()

    ingest_documents(args.collection)