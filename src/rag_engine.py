"""
RAG (Retrieval-Augmented Generation) Engine with Langfuse Observability.

This module implements the core RAG logic:
- Retrieval: Fetching relevant context from GroundX
- Augmentation: Constructing prompts with retrieved context
- Generation: Using LLM to generate answers
- Observability: Optional Langfuse tracing for production monitoring
"""

import time
from typing import Dict, List, Optional
from functools import wraps

from openai import OpenAI

from config import llm_config, langfuse_config
from src.groundx_client import GroundXClient


# Langfuse setup (with safe fallback)
langfuse_client = None
observe_decorator = None

if langfuse_config.is_configured:
    try:
        from langfuse import Langfuse, observe

        langfuse_client = Langfuse(
            public_key=langfuse_config.public_key,
            secret_key=langfuse_config.secret_key,
            host=langfuse_config.host,
        )
        observe_decorator = observe
    except ImportError:
        print("  ○ Langfuse not installed - observability disabled")
    except Exception as e:
        print(f"  ○ Langfuse initialization failed - observability disabled: {str(e)}")


def safe_observe(func):
    """
    Decorator that conditionally applies Langfuse observability.

    If Langfuse is configured and available, it wraps the function with
    the @observe decorator. Otherwise, it executes the function normally.

    This ensures the code works even without Langfuse credentials.
    """
    if observe_decorator is not None:
        try:
            return observe_decorator()(func)
        except Exception:
            pass

    # Fallback: No observability, just run the function
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def flush_langfuse():
    """Flush Langfuse events (important for short-lived scripts)."""
    if langfuse_client is not None:
        try:
            langfuse_client.flush()
        except Exception:
            pass


class RAGEngine:
    """
    RAG Engine for question-answering over ITNB knowledge base.

    Implements a complete RAG pipeline with:
    - Semantic search via GroundX
    - Context-aware prompt construction
    - LLM-powered answer generation
    - Source citation
    - Optional Langfuse observability
    """

    def __init__(self, groundx_client: GroundXClient = None):
        """
        Initialize RAG engine.

        Args:
            groundx_client: GroundX client instance (creates new if not provided)
        """
        self.groundx_client = groundx_client or GroundXClient()

        # Initialize LLM client (OpenAI-compatible)
        self.llm_client = OpenAI(
            api_key=llm_config.api_key,
            base_url=llm_config.api_base,
        )

        self.model_name = llm_config.model_name
        self.temperature = llm_config.temperature
        self.max_tokens = llm_config.max_tokens
        self.top_k = llm_config.top_k

        # System prompt for the RAG assistant
        self.system_prompt = """You are a helpful AI assistant for ITNB AG, a Swiss cybersecurity and IT company.

Your role is to answer questions based SOLELY on the provided context from the ITNB website.

Guidelines:
- Only use information from the provided context
- If the answer is not in the context, say "I don't have enough information to answer that question based on the available content."
- Be concise and accurate
- Maintain a professional, helpful tone
- Do not add source URLs to your answer - they will be displayed separately
- When conversation history is provided, use it to understand follow-up questions and maintain context
- If a question references previous messages (e.g., "tell me more", "what about that?"), use the conversation history to understand the context
"""

    @safe_observe
    def retrieve_context(self, query: str, top_k: int = None) -> List[Dict[str, any]]:
        """
        Retrieve relevant context from GroundX knowledge base.

        Args:
            query: User query
            top_k: Number of chunks to retrieve (defaults to config)

        Returns:
            List of retrieved chunks with metadata
        """
        k = top_k or self.top_k

        # Search GroundX
        results = self.groundx_client.search(query=query, n=k)

        return results

    def _construct_prompt(self, query: str, context_chunks: List[Dict[str, any]], conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Construct prompt with retrieved context and optional conversation history.

        Args:
            query: User query
            context_chunks: Retrieved context chunks
            conversation_history: Optional list of previous Q&A pairs

        Returns:
            Formatted prompt for LLM
        """
        # Build context section
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            source_url = chunk.get("source_url", "Unknown source")
            text = chunk.get("text", "")
            context_parts.append(f"[Source {i}: {source_url}]\n{text}\n")

        context = "\n".join(context_parts)

        # Build conversation history section (if enabled)
        history_section = ""
        if conversation_history:
            history_parts = []
            for exchange in conversation_history:
                history_parts.append(f"User: {exchange['question']}")
                history_parts.append(f"Assistant: {exchange['answer']}")
            history_section = f"""Previous Conversation:
{chr(10).join(history_parts)}

---

"""

        # Construct full prompt
        prompt = f"""Context from ITNB website:

{context}

---

{history_section}User Question: {query}

Please provide a helpful answer based on the context above.
"""
        return prompt

    @safe_observe
    def generate_answer(self, query: str, context_chunks: List[Dict[str, any]], conversation_history: List[Dict[str, str]] = None) -> Dict[str, any]:
        """
        Generate answer using LLM with retrieved context and optional conversation history.

        Args:
            query: User query
            context_chunks: Retrieved context chunks
            conversation_history: Optional list of previous Q&A pairs

        Returns:
            Dictionary with answer and metadata
        """
        # Construct prompt (with conversation history if provided)
        prompt = self._construct_prompt(query, context_chunks, conversation_history)

        # Call LLM
        start_time = time.time()
        response = self.llm_client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        latency = time.time() - start_time

        # Extract answer
        answer = response.choices[0].message.content

        # Collect unique source URLs
        source_urls = list(set(
            chunk.get("source_url", "")
            for chunk in context_chunks
            if chunk.get("source_url")
        ))

        # Add metadata to Langfuse trace (if available)
        if langfuse_client is not None:
            try:
                from langfuse.decorators import langfuse_context
                langfuse_context.update_current_observation(
                    metadata={
                        "model": self.model_name,
                        "temperature": self.temperature,
                        "chunks_retrieved": len(context_chunks),
                        "sources": source_urls,
                    }
                )
            except Exception:
                pass  # Silently fail if Langfuse context not available

        return {
            "answer": answer,
            "sources": source_urls,
            "latency": latency,
            "model": self.model_name,
            "chunks_used": len(context_chunks),
        }

    @safe_observe
    def query(self, question: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, any]:
        """
        Main RAG query method - end-to-end pipeline.

        Args:
            question: User question
            conversation_history: Optional list of previous Q&A pairs (for conversational context)

        Returns:
            Dictionary with answer, sources, and metadata
        """
        # Step 1: Retrieve relevant context
        context_chunks = self.retrieve_context(question)

        if not context_chunks:
            return {
                "answer": "I couldn't find any relevant information to answer your question.",
                "sources": [],
                "latency": 0,
                "chunks_used": 0,
            }

        # Step 2: Generate answer with LLM (with conversation history if provided)
        result = self.generate_answer(question, context_chunks, conversation_history)

        return result


def test_rag_engine():
    """Test function for RAG engine."""
    print("\n" + "="*60)
    print("Testing RAG Engine")
    print("="*60 + "\n")

    # Initialize
    engine = RAGEngine()

    # Test queries
    test_questions = [
        "What does ITNB do?",
        "What services does ITNB offer?",
    ]

    for question in test_questions:
        print(f"\nQuestion: {question}")
        print("-" * 60)

        result = engine.query(question)

        print(f"\nAnswer:\n{result['answer']}\n")
        print(f"Sources:")
        for source in result['sources']:
            print(f"  - {source}")
        print(f"\nMetadata:")
        print(f"  - Latency: {result['latency']:.2f}s")
        print(f"  - Chunks used: {result['chunks_used']}")
        print("\n" + "="*60)


if __name__ == "__main__":
    test_rag_engine()
