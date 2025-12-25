"""Quick system test with a single query."""
from src.health_check import run_health_check
from src.groundx_client import GroundXClient
from src.rag_engine import RAGEngine, flush_langfuse

print("Testing complete RAG system...")
print()

# Run health check
healthy = run_health_check()

if not healthy:
    print("\n❌ Health check failed!")
    exit(1)

# Initialize
print("\n🔧 Initializing RAG Engine...")
groundx_client = GroundXClient()
groundx_client.get_or_create_bucket()

rag_engine = RAGEngine(groundx_client=groundx_client)
print("✓ System ready!\n")

# Test query
print("="*60)
print("Testing Query: 'What does ITNB do?'")
print("="*60)

result = rag_engine.query("What does ITNB do?")

print(f"\n🤖 Answer:\n{result['answer']}\n")
print(f"📚 Sources:")
for i, source in enumerate(result.get('sources', []), 1):
    print(f"  {i}. {source}")

print(f"\n⚡ Response Time: {result.get('latency', 0):.2f}s")
print(f"📊 Chunks Used: {result.get('chunks_used', 0)}")
print(f"🤖 Model: {result.get('model', 'Unknown')}")

# Flush Langfuse traces
flush_langfuse()

print("\n" + "="*60)
print("✓ Test completed successfully!")
print("="*60)
