"""
Testing script to validate embedding consistency for the RAG retrieval pipeline.
This script tests the consistency of embeddings generated for the same query multiple times,
and also tests semantic similarity between semantically similar queries.
"""

import sys
import os
import time
from typing import List

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from clients.cohere_client import CohereClient
from config.settings import settings


def test_embedding_consistency():
    """
    Test the consistency of embeddings for the same query across multiple runs.
    """
    print("Testing embedding consistency...")

    # Initialize Cohere client
    cohere_client = CohereClient()

    # Test query
    test_query = "What are the key features of RAG systems?"

    # Check consistency
    is_consistent = cohere_client.check_consistency(test_query, num_runs=5, threshold=0.95)

    print(f"Query: {test_query}")
    print(f"Consistency check (5 runs, threshold 0.95): {'PASS' if is_consistent else 'FAIL'}")

    return is_consistent


def test_semantic_similarity():
    """
    Test semantic similarity between semantically similar queries.
    """
    print("\nTesting semantic similarity between similar queries...")

    # Initialize Cohere client
    cohere_client = CohereClient()

    # Semantically similar queries
    queries = [
        "What are the key features of RAG systems?",
        "What features does RAG have?",
        "Explain the main components of RAG",
        "How does a RAG system work?"
    ]

    print("Testing semantic similarity between related queries:")
    all_similar = True

    for i in range(len(queries)):
        for j in range(i + 1, len(queries)):
            similarity = cohere_client.compare_semantic_similarity(queries[i], queries[j])
            is_similar = similarity > 0.5  # Threshold for semantic similarity
            print(f"  '{queries[i]}' vs '{queries[j]}': {similarity:.3f} ({'SIMILAR' if is_similar else 'NOT SIMILAR'})")
            if not is_similar:
                all_similar = False

    print(f"\nOverall semantic similarity check: {'PASS' if all_similar else 'FAIL'}")

    return all_similar


def test_performance_requirements():
    """
    Test performance requirements: response time under 500ms.
    """
    print("\nTesting performance requirements...")

    try:
        # Initialize retrieval service
        from models.retrieval import RetrievalService
        service = RetrievalService()

        # Check if collection exists
        collection_exists = service.validate_collection(settings.QDRANT_COLLECTION)
        print(f"Collection '{settings.QDRANT_COLLECTION}' exists: {collection_exists}")

        if not collection_exists:
            print(f"WARNING: Collection does not exist. Cannot test performance.")
            return False

        # Define performance test parameters
        test_queries = [
            "What is RAG?",
            "How does retrieval work?",
            "Explain vector search",
            "What are embeddings?",
            "Define Qdrant database"
        ]

        response_times = []
        max_allowed_time = 500  # ms
        all_within_limit = True

        print(f"Testing response times for {len(test_queries)} queries...")

        for i, query in enumerate(test_queries):
            start_time = time.time()
            results = service.retrieve(query=query, top_k=3)
            actual_time = results['execution_time_ms']
            response_times.append(actual_time)

            within_limit = actual_time <= max_allowed_time
            all_within_limit = all_within_limit and within_limit

            status = "PASS" if within_limit else "FAIL"
            print(f"  {i+1}. Query: '{query[:30]}...' - {actual_time:.2f}ms [{status}]")

        avg_response_time = sum(response_times) / len(response_times)
        print(f"  Average response time: {avg_response_time:.2f}ms")
        print(f"  Max allowed: {max_allowed_time}ms")

        # Also check the 95% percentile requirement (SC-002)
        sorted_times = sorted(response_times)
        p95_index = int(0.95 * len(sorted_times))
        p95_time = sorted_times[p95_index] if p95_index < len(sorted_times) else sorted_times[-1]
        p95_within_limit = p95_time <= 500  # Requirement: 95% of requests under 500ms

        print(f"  P95 response time: {p95_time:.2f}ms [{'PASS' if p95_within_limit else 'FAIL'}]")

        overall_pass = all_within_limit and p95_within_limit
        print(f"  Performance test result: {'PASS' if overall_pass else 'FAIL'}")

        return overall_pass

    except Exception as e:
        print(f"Performance test failed: {str(e)}")
        return False


def test_basic_functionality():
    """
    Test basic functionality and metadata retrieval.
    """
    print("\nTesting basic retrieval functionality...")

    try:
        # Initialize retrieval service
        from models.retrieval import RetrievalService
        service = RetrievalService()

        # Test collection validation
        collection_exists = service.validate_collection(settings.QDRANT_COLLECTION)
        print(f"Collection '{settings.QDRANT_COLLECTION}' exists: {collection_exists}")

        if not collection_exists:
            print(f"WARNING: Collection does not exist. Cannot test full retrieval functionality.")
            return False

        # Test with a short query
        test_query = "test"
        results = service.retrieve(query=test_query, top_k=3)

        print(f"Query: {results['query']}")
        print(f"Retrieved {len(results['results'])} results")
        print(f"Execution time: {results['execution_time_ms']:.2f} ms")

        # Check if results have required metadata
        if results['results']:
            first_result = results['results'][0]
            has_metadata = all([
                'source_url' in first_result,
                'source_title' in first_result,
                'headings' in first_result,
                'similarity_score' in first_result
            ])
            print(f"First result has required metadata: {has_metadata}")
        else:
            print("WARNING: No results returned for test query")
            return False

        return True

    except Exception as e:
        print(f"Basic functionality test failed: {str(e)}")
        return False


def main():
    """
    Main function to run all validation tests.
    """
    print("Running retrieval pipeline validation tests...\n")

    # Validate configuration first
    if not settings.validate():
        print("Configuration validation failed. Please check your environment variables.")
        return 1

    # Run all tests
    consistency_result = test_embedding_consistency()
    similarity_result = test_semantic_similarity()
    performance_result = test_performance_requirements()
    functionality_result = test_basic_functionality()

    # Overall result
    all_passed = consistency_result and similarity_result and performance_result and functionality_result

    print(f"\nOverall test result: {'PASS' if all_passed else 'FAIL'}")

    if all_passed:
        print("All validation tests passed!")
        return 0
    else:
        print("Some validation tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())