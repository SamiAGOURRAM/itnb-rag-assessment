"""
Command-Line Interface for ITNB RAG Chat.

This module provides a simple, interactive chat interface for querying
the ITNB knowledge base through the RAG engine.
"""

import sys
from typing import Optional

from src.rag_engine import RAGEngine, flush_langfuse
from src.groundx_client import GroundXClient
from src.health_check import run_health_check


class ChatCLI:
    """
    Interactive CLI for RAG-powered Q&A.

    Provides a simple command-line interface for users to ask questions
    about ITNB, with answers powered by the RAG engine.
    """

    def __init__(self, rag_engine: Optional[RAGEngine] = None):
        """
        Initialize chat CLI.

        Args:
            rag_engine: RAG engine instance (creates new if not provided)
        """
        self.rag_engine = rag_engine or RAGEngine()
        self.conversation_history = []

    def print_welcome(self):
        """Print welcome message with ASCII art."""
        print("""
  ██╗████████╗███╗   ██╗██████╗      █████╗ ██╗
  ██║╚══██╔══╝████╗  ██║██╔══██╗    ██╔══██╗██║
  ██║   ██║   ██╔██╗ ██║██████╔╝    ███████║██║
  ██║   ██║   ██║╚██╗██║██╔══██╗    ██╔══██║██║
  ██║   ██║   ██║ ╚████║██████╔╝    ██║  ██║██║
  ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚═════╝     ╚═╝  ╚═╝╚═╝
        """)
        print("Welcome! I can answer questions about ITNB AG based on")
        print("the company's website content.")
        print("\nCommands:")
        print("  - Type your question and press Enter")
        print("  - Type '/health' to check system health")
        print("  - Type 'exit' or 'quit' to end the session")
        print("  - Type 'clear' to clear conversation history")
        print("="*60 + "\n")

    def print_sources(self, sources: list):
        """
        Print source URLs in a formatted way.

        Args:
            sources: List of source URLs
        """
        if sources:
            print("\n📚 Sources:")
            for i, source in enumerate(sources, 1):
                print(f"  {i}. {source}")
        else:
            print("\n📚 Sources: None found")

    def print_metadata(self, metadata: dict):
        """
        Print query metadata (latency, chunks used, etc.).

        Args:
            metadata: Dictionary with metadata
        """
        latency = metadata.get("latency", 0)
        chunks = metadata.get("chunks_used", 0)
        model = metadata.get("model", "Unknown")

        print(f"\n⚡ Response Time: {latency:.2f}s | Chunks: {chunks} | Model: {model}")

    def process_query(self, question: str) -> dict:
        """
        Process user question through RAG engine.

        Args:
            question: User question

        Returns:
            Dictionary with answer and metadata
        """
        try:
            # Import config to check if memory is enabled
            from config import llm_config

            # Prepare conversation history if memory is enabled
            history_to_pass = None
            if llm_config.use_conversation_memory and self.conversation_history:
                # Keep only last N messages (sliding window)
                max_history = llm_config.max_history_messages
                history_to_pass = self.conversation_history[-max_history:]

            # Query with optional conversation history
            result = self.rag_engine.query(question, conversation_history=history_to_pass)

            # Store in conversation history
            self.conversation_history.append({
                "question": question,
                "answer": result.get("answer", ""),
                "sources": result.get("sources", []),
            })

            return result
        except Exception as e:
            return {
                "answer": f"❌ Error processing query: {str(e)}",
                "sources": [],
                "latency": 0,
                "chunks_used": 0,
            }

    def handle_command(self, user_input: str) -> bool:
        """
        Handle special commands.

        Args:
            user_input: User input

        Returns:
            True if should continue, False if should exit
        """
        command = user_input.lower().strip()

        if command in ["exit", "quit", "q"]:
            print("\n👋 Thank you for using ITNB Knowledge Base Assistant!")
            print("="*60 + "\n")
            return False

        if command == "clear":
            self.conversation_history = []
            print("\n✓ Conversation history cleared.\n")
            return True

        if command in ["help", "h", "?"]:
            self.print_welcome()
            return True

        if command == "/health":
            print()  # Add spacing
            run_health_check()
            print()  # Add spacing
            return True

        return True

    def run(self):
        """
        Run the interactive chat loop.
        """
        self.print_welcome()

        try:
            while True:
                # Get user input
                try:
                    user_input = input("💬 You: ").strip()
                except EOFError:
                    print("\n")
                    break
                except KeyboardInterrupt:
                    print("\n\n👋 Session interrupted. Goodbye!")
                    break

                # Skip empty input
                if not user_input:
                    continue

                # Handle special commands
                if user_input.lower() in ["exit", "quit", "q", "clear", "help", "h", "?", "/health"]:
                    if not self.handle_command(user_input):
                        break
                    continue

                # Process query
                print("\n🤖 Assistant: ", end="", flush=True)
                result = self.process_query(user_input)

                # Print answer
                print(result["answer"])

                # Print sources (required by assessment)
                self.print_sources(result.get("sources", []))

                # Print metadata
                self.print_metadata(result)

                # Flush Langfuse traces (important for observability)
                flush_langfuse()

                print("\n" + "-"*60 + "\n")

        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            sys.exit(1)


def run_chat():
    """
    Convenience function to start the chat interface.

    Performs health checks before initialization to ensure all
    systems are operational.
    """
    try:
        # Run health checks first
        healthy = run_health_check()

        if not healthy:
            print("\n❌ System health check failed. Please fix the issues above.")
            print("Exiting...")
            sys.exit(1)

        print()  # Add spacing after health check

        # Initialize GroundX client and ensure bucket exists (quietly)
        import io
        import contextlib

        # Suppress bucket initialization output
        with contextlib.redirect_stdout(io.StringIO()):
            groundx_client = GroundXClient()
            groundx_client.get_or_create_bucket()
            rag_engine = RAGEngine(groundx_client=groundx_client)

        # Start chat
        cli = ChatCLI(rag_engine=rag_engine)
        cli.run()

    except KeyboardInterrupt:
        print("\n\n👋 Session interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Failed to initialize chat: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_chat()
