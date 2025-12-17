#!/usr/bin/env python3
"""
Retrieval Pipeline Testing Tool

A command-line interface for testing and validating vector retrieval
from Qdrant using stored embeddings.
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

from models.retrieval import RetrievalService
from config.settings import settings


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="RAG Retrieval Pipeline Testing Tool")
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
        # Initialize the retrieval service
        retrieval_service = RetrievalService()

        # Check Qdrant connection before proceeding
        if not retrieval_service.qdrant_client.is_connection_available():
            print(f"Error: Cannot connect to Qdrant at {retrieval_service.qdrant_client.url}", file=sys.stderr)
            return 3

        # Validate that the collection exists
        if not retrieval_service.validate_collection(args.collection):
            print(f"Error: Collection '{args.collection}' does not exist or is not accessible", file=sys.stderr)
            return 1

        # Run the retrieval
        start_time = time.time()
        results = retrieval_service.retrieve(
            query=args.query,
            collection_name=args.collection,
            top_k=args.top_k
        )
        total_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        results["execution_time_ms"] = total_time

        # Log results if requested
        if args.log_results:
            log_results(results)

        # Print results based on format
        if args.output == "json":
            print(json.dumps(results, indent=2))
        else:  # text format
            print_text_results(results)

        return 0
    except ConnectionError as ce:
        print(f"Error: Connection issue - {str(ce)}", file=sys.stderr)
        return 3  # Connection error
    except PermissionError as pe:
        print(f"Error: Authorization issue - {str(pe)}", file=sys.stderr)
        return 3  # Authentication error
    except ValueError as ve:
        # Check for specific edge cases
        if "Collection" in str(ve) and "does not exist" in str(ve):
            print(f"Error: Collection '{args.collection}' does not exist or is not accessible", file=sys.stderr)
            return 1  # General error
        elif "dimension" in str(ve).lower() or "dim:" in str(ve):
            print("Error: Vector dimension mismatch. The Cohere model embedding dimension doesn't match the Qdrant collection's expected dimension.", file=sys.stderr)
            print("Please ensure your Cohere model generates embeddings with the same dimensionality as used when the Qdrant collection was created.", file=sys.stderr)
            return 4  # Dimension mismatch error
        else:
            print(f"Error: Invalid input - {str(ve)}", file=sys.stderr)
            return 1  # General error
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        error_code = 3  # General error
        if "Connection" in str(e) or "Authentication" in str(e):
            error_code = 3  # Connection/authentication error
        elif "Configuration" in str(e):
            error_code = 2  # Configuration error
        elif "dimension" in str(e).lower() or "dim:" in str(e):
            error_code = 4  # Dimension mismatch error

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

    log_filename = f"{log_dir}/retrieval_results_{int(results['timestamp'])}.json"
    with open(log_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    logger.info(f"Results logged to {log_filename}")


if __name__ == "__main__":
    sys.exit(main())