"""Test conversational memory feature."""
from src.groundx_client import GroundXClient
from src.rag_engine import RAGEngine
from config import llm_config

print("\n" + "="*60)
print("  Testing Conversational Memory")
print("="*60 + "\n")

print(f"Memory Enabled: {llm_config.use_conversation_memory}")
print(f"Max History: {llm_config.max_history_messages} message pairs\n")

# Initialize
print("Initializing...")
import io
import contextlib

with contextlib.redirect_stdout(io.StringIO()):
    groundx_client = GroundXClient()
    groundx_client.get_or_create_bucket()
    rag_engine = RAGEngine(groundx_client=groundx_client)

print("✓ System ready!\n")

# Simulate conversation
conversation_history = []

print("="*60)
print("Query 1: What does ITNB do?")
print("="*60)
result1 = rag_engine.query("What does ITNB do?")
print(f"\nAnswer: {result1['answer'][:200]}...\n")

# Store first exchange
conversation_history.append({
    "question": "What does ITNB do?",
    "answer": result1['answer']
})

print("="*60)
print("Query 2 (Follow-up): Tell me more about their cloud services")
print("="*60)

# Test WITH memory
if llm_config.use_conversation_memory:
    print("\n[WITH MEMORY - Passing conversation history]")
    result2_with_memory = rag_engine.query(
        "Tell me more about their cloud services",
        conversation_history=conversation_history
    )
    print(f"\nAnswer: {result2_with_memory['answer'][:300]}...\n")
else:
    print("\n[Memory is DISABLED in config]")

# Test WITHOUT memory
print("\n[WITHOUT MEMORY - No conversation history]")
result2_without_memory = rag_engine.query("Tell me more about their cloud services")
print(f"\nAnswer: {result2_without_memory['answer'][:300]}...\n")

print("="*60)
print("✓ Test complete!")
print("="*60)
print("\nComparison:")
print("- WITH memory: Should understand 'their' refers to ITNB")
print("- WITHOUT memory: May ask 'whose cloud services?'")
print("\nNote: Both will work, but WITH memory provides better context.")
