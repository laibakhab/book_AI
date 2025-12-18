"""
Script to ingest documents into the Qdrant vector database for the RAG system.
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


def read_sample_documents() -> List[Dict[str, Any]]:
    """
    Read sample documents to index in the vector database.

    Returns:
        List of document dictionaries with text content and metadata
    """
    documents = []

    # Sample document about artificial intelligence
    ai_doc = {
        "text": """
Artificial Intelligence (AI) is a branch of computer science that aims to create software or machines that exhibit human-like intelligence. This includes learning from experience, understanding natural language, solving problems, and recognizing patterns. AI can be categorized into different types based on capabilities and functionality.

Narrow AI, also known as Weak AI, is designed to perform a narrow task, such as facial recognition or internet searches. Most current AI applications fall into this category. On the other hand, General AI, or Strong AI, would have the ability to understand, learn, and apply knowledge across a wide range of tasks at a level equal to human intelligence.

Machine learning is a subset of AI that allows systems to learn and improve from experience without being explicitly programmed. Deep learning is a subfield of machine learning that uses neural networks with many layers to model and understand complex patterns in data.

Applications of AI are widespread and include virtual assistants, recommendation systems, autonomous vehicles, medical diagnosis, fraud detection, and many more. The technology continues to evolve rapidly, with new breakthroughs happening frequently.
""",
        "source": "ai_introduction.txt",
        "title": "Introduction to Artificial Intelligence",
        "url": "https://example.com/ai-intro",
        "page_number": 1
    }

    # Sample document about machine learning
    ml_doc = {
        "text": """
Machine Learning (ML) is a type of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed. Instead of following static instructions, ML algorithms use statistical techniques to improve their performance based on experience.

There are several types of machine learning: supervised learning, where the model is trained on labeled data; unsupervised learning, where the model identifies patterns in unlabeled data; and reinforcement learning, where the model learns to make decisions by interacting with an environment.

Key concepts in machine learning include features (input variables), labels (output variables), training (the process of fitting the model), and testing (evaluating the model's performance). Common algorithms include linear regression, decision trees, neural networks, and support vector machines.

Machine learning has applications in many fields including image recognition, natural language processing, predictive analytics, and autonomous systems. The field is rapidly evolving with new techniques like transfer learning, where knowledge from one domain is applied to another, and ensemble methods, where multiple models are combined for better performance.
""",
        "source": "ml_fundamentals.txt",
        "title": "Fundamentals of Machine Learning",
        "url": "https://example.com/ml-fundamentals",
        "page_number": 1
    }

    # Sample document about natural language processing
    nlp_doc = {
        "text": """
Natural Language Processing (NLP) is a field of artificial intelligence that focuses on the interaction between computers and humans through natural language. The ultimate objective of NLP is to enable computers to understand, interpret, and respond to human language in a valuable way.

NLP combines computational linguistics with statistical, machine learning, and deep learning models. These technologies enable computers to process human language in the form of text or voice data and understand its full meaning, complete with the speaker's intent and sentiment.

Key tasks in NLP include text classification, sentiment analysis, named entity recognition, machine translation, and question answering. Modern NLP systems use transformer models like BERT, GPT, and their variants, which have achieved remarkable performance on various language understanding tasks.

Applications of NLP are diverse and include chatbots, virtual assistants, language translation services, text summarization tools, and content analysis systems. The field continues to advance with new models that better understand context, nuance, and the subtleties of human communication.
""",
        "source": "nlp_overview.txt",
        "title": "Overview of Natural Language Processing",
        "url": "https://example.com/nlp-overview",
        "page_number": 1
    }

    documents.extend([ai_doc, ml_doc, nlp_doc])

    return documents


def ingest_documents(collection_name: str = None):
    """
    Main function to ingest documents into Qdrant.

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

        # Read documents
        documents = read_sample_documents()
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

    parser = argparse.ArgumentParser(description="Ingest documents into the Qdrant vector database")
    parser.add_argument("--collection", type=str, default=settings.QDRANT_COLLECTION,
                        help=f"Name of the Qdrant collection to use (default: '{settings.QDRANT_COLLECTION}')")

    args = parser.parse_args()

    ingest_documents(args.collection)