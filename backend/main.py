"""
RAG Agent Backend for Question Answering

A command-line interface for testing and validating vector retrieval from Qdrant using stored embeddings.
This tool enables backend engineers and RAG evaluators to test the accuracy and performance of the retrieval pipeline.
"""

import argparse
import os
import time
import json
import logging
import sys
from typing import List, Dict, Any, Optional

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__)))

from clients.cohere_client import CohereClient
from clients.qdrant_client import QdrantClientWrapper
from config.settings import settings


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="RAG Agent Backend - Answer user queries using retrieved book content")
    parser.add_argument("query", type=str, help="The text query to test against the vector database")
    parser.add_argument("-k", "--top-k", type=int, default=settings.DEFAULT_TOP_K, help=f"Number of top results to retrieve (default: {settings.DEFAULT_TOP_K})")
    parser.add_argument("-c", "--collection", type=str, default=settings.QDRANT_COLLECTION, help=f"Name of the Qdrant collection to search (default: '{settings.QDRANT_COLLECTION}')")
    parser.add_argument("-o", "--output", type=str, choices=["text", "json"], default="text", help="Output format (default: text)")
    parser.add_argument("-l", "--log-results", action="store_true", help="Log results to a file for analysis")

    args = parser.parse_args()

    # Validate inputs
    if not args.query.strip():
        print("Error: Query cannot be empty or only whitespace", file=sys.stderr)
        return 1

    if args.top_k < settings.MIN_TOP_K or args.top_k > settings.MAX_TOP_K:
        print(f"Error: Top-K value must be between {settings.MIN_TOP_K} and {settings.MAX_TOP_K}", file=sys.stderr)
        return 1

    # Validate configuration
    if not settings.validate():
        print("Error: Configuration validation failed", file=sys.stderr)
        return 2

    try:
        # Initialize clients
        cohere_client = CohereClient()
        qdrant_client = QdrantClientWrapper()

        # Ensure the collection exists with the correct vector dimensions (4096 for Cohere multilingual model)
        qdrant_client.ensure_collection_exists(args.collection, recreate_if_exists=False)

        # Run the RAG process
        start_time = time.time()

        # Step 1: Generate embedding for the query
        query_embedding = cohere_client.generate_embedding(args.query)

        # Step 2: Search in Qdrant for similar content
        search_results = qdrant_client.search(
            collection_name=args.collection,
            query_vector=query_embedding,
            top_k=args.top_k
        )

        # Step 3: Format the results
        formatted_results = []
        for i, result in enumerate(search_results):
            formatted_result = {
                "rank": i + 1,
                "chunk_id": result["id"],
                "similarity_score": result["score"],
                "text_content": result["payload"].get("text", "")[:200] + "..." if len(result["payload"].get("text", "")) > 200 else result["payload"].get("text", ""),
                "full_content": result["payload"].get("text", ""),
                "source_url": result["payload"].get("url", ""),
                "source_title": result["payload"].get("title", ""),
                "headings": result["payload"].get("headings", []),
                "metadata": {k: v for k, v in result["payload"].items() if k not in ["text", "url", "title", "headings"]}
            }
            formatted_results.append(formatted_result)

        # Calculate execution time
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Prepare the response
        response = {
            "query": args.query,
            "query_embedding_model": cohere_client.model_name,
            "collection": args.collection,
            "top_k": args.top_k,
            "results": formatted_results,
            "execution_time_ms": execution_time,
            "timestamp": time.time()
        }

        # Log results if requested
        if args.log_results:
            log_results(response)

        # Output results based on format
        if args.output == "json":
            print(json.dumps(response, indent=2))
        else:  # text format
            print_text_results(response)

        return 0
    except ConnectionError as ce:
        print(f"Error: Connection issue with external service - {str(ce)}", file=sys.stderr)
        return 3  # Connection error
    except PermissionError as pe:
        print(f"Error: Authentication issue - {str(pe)}", file=sys.stderr)
        return 3  # Authentication error
    except ValueError as ve:
        # Check for specific edge cases
        if "Collection" in str(ve) and "does not exist" in str(ve):
            print(f"Error: Collection '{args.collection}' does not exist or is not accessible", file=sys.stderr)
            return 1  # General error
        else:
            print(f"Error: Invalid input - {str(ve)}", file=sys.stderr)
            return 1  # General error
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        error_code = 1  # General error
        if "Connection" in str(e) or "Authentication" in str(e):
            error_code = 3  # Connection/authentication error
        elif "Configuration" in str(e):
            error_code = 2  # Configuration error

        if args.output == "json":
            error_output = {
                "error": str(e),
                "error_code": error_code,
                "timestamp": time.time()
            }
            print(json.dumps(error_output, indent=2))
        else:
            print(error_msg)
        return error_code


def print_text_results(results: Dict[str, Any]) -> None:
    """
    Print results in text format
    """
    print(f"\nQuery: {results['query']}")
    print(f"Query embedding generated using model: {results['query_embedding_model']}\n")

    print(f"Retrieved {len(results['results'])} results:\n")

    for result in results['results']:
        print(f"{result['rank']}. {result['text_content']} (Score: {result['similarity_score']:.3f})")
        print(f"   Source: {result['source_url']}")
        print(f"   Title: {result['source_title']}")
        if result['headings']:
            print(f"   Headings: {', '.join(result['headings'])}")
        print()

    print(f"Retrieval completed in {results['execution_time_ms']:.2f} ms")


def log_results(results: Dict[str, Any]) -> None:
    """
    Log results to a file for relevance validation
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = f"{log_dir}/rag_results_{int(results['timestamp'])}.json"
    with open(log_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    logger.info(f"Results logged to {log_filename}")


if __name__ == "__main__":
    sys.exit(main())