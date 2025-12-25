"""
Test script to run sample queries and verify RAG system works.
"""

from src.groundx_client import GroundXClient
from src.rag_engine import RAGEngine

print("\n" + "="*60)
print("  Testing ITNB RAG System")
print("="*60 + "\n")

# Initialize
groundx_client = GroundXClient()
groundx_client.get_or_create_bucket()

rag_engine = RAGEngine(groundx_client=groundx_client)

# Test queries
test_queries = [
    "What does ITNB do?",
    "What is Sovereign Cloud?",
    "What services does ITNB offer?",
]

for i, query in enumerate(test_queries, 1):
    print(f"\n{'-'*60}")
    print(f"Query {i}: {query}")
    print(f"{'-'*60}\n")

    try:
        result = rag_engine.query(query)

        print(f"Answer:\n{result['answer']}\n")

        print(f"Sources:")
        for source in result.get('sources', []):
            print(f"  - {source}")

        print(f"\nMetadata:")
        print(f"  Latency: {result.get('latency', 0):.2f}s")
        print(f"  Chunks: {result.get('chunks_used', 0)}")
        print(f"  Model: {result.get('model', 'Unknown')}")

    except Exception as e:
        print(f"ERROR: {e}")

print("\n" + "="*60)
print("  Testing Complete!")
print("="*60 + "\n")
