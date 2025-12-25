"""
Main entry point for ITNB RAG Assessment.

This orchestrates the complete pipeline:
1. Configuration validation
2. Web crawling (optional)
3. Document ingestion (optional)
4. Interactive chat interface

Usage:
    python main.py                    # Start chat (assumes data already ingested)
    python main.py --crawl            # Crawl website first, then chat
    python main.py --ingest           # Ingest existing files, then chat
    python main.py --full-pipeline    # Crawl + Ingest + Chat
    python main.py --crawl-only       # Only crawl, don't start chat
    python main.py --ingest-only      # Only ingest, don't start chat
"""

import argparse
import asyncio
import sys
from pathlib import Path

from config import validate_config, print_config_status, SCRAPED_DIR
from src.crawler import run_crawler
from src.groundx_client import GroundXClient
from src.cli import run_chat


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="ITNB RAG Assessment - Web Scraping, Ingestion, and Q&A System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                      # Start chat interface
  python main.py --full-pipeline      # Run complete pipeline: crawl, ingest, chat
  python main.py --crawl --ingest     # Crawl and ingest, then start chat
  python main.py --crawl-only         # Only perform crawling
  python main.py --ingest-only        # Only perform ingestion
        """
    )

    parser.add_argument(
        "--crawl",
        action="store_true",
        help="Crawl ITNB website before starting chat"
    )

    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Ingest documents to GroundX before starting chat"
    )

    parser.add_argument(
        "--full-pipeline",
        action="store_true",
        help="Run complete pipeline: crawl, ingest, then chat"
    )

    parser.add_argument(
        "--crawl-only",
        action="store_true",
        help="Only crawl the website (don't start chat)"
    )

    parser.add_argument(
        "--ingest-only",
        action="store_true",
        help="Only ingest documents (don't start chat)"
    )

    return parser.parse_args()


async def run_crawl_phase():
    """Execute web crawling phase."""
    print("\n" + "🕷️  "*20)
    print("PHASE 1: Web Crawling")
    print("🕷️  "*20 + "\n")

    try:
        pages = await run_crawler()
        print(f"\n✅ Crawling completed: {len(pages)} pages scraped\n")
        return True
    except Exception as e:
        print(f"\n❌ Crawling failed: {str(e)}\n")
        return False


def run_ingest_phase():
    """Execute document ingestion phase."""
    print("\n" + "📤 "*20)
    print("PHASE 2: Document Ingestion")
    print("📤 "*20 + "\n")

    try:
        # Check if we have files to ingest
        files = list(SCRAPED_DIR.glob("*.md"))
        if not files:
            print("⚠️  No markdown files found in data/scraped/")
            print("   Run with --crawl first to scrape website content\n")
            return False

        # Initialize GroundX client
        client = GroundXClient()

        # Get or create bucket
        client.get_or_create_bucket()

        # Ingest documents
        result = client.ingest_documents(files)

        if result["status"] == "success":
            print(f"\n✅ Ingestion completed: {result['count']} documents uploaded\n")
            return True
        else:
            print(f"\n⚠️  Ingestion status: {result['status']}\n")
            return False

    except Exception as e:
        print(f"\n❌ Ingestion failed: {str(e)}\n")
        return False


def run_chat_phase():
    """Execute interactive chat phase."""

    try:
        run_chat()
    except Exception as e:
        print(f"\n❌ Chat failed: {str(e)}\n")
        return False


def main():
    """Main orchestrator function."""

    # Parse arguments
    args = parse_arguments()

    # Validate configuration
    is_valid, errors = validate_config()

    if not is_valid:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"   - {error}")
        print("\nPlease set required environment variables and try again.")
        print("See .env.example for reference.\n")
        sys.exit(1)

    print_config_status()

    # Determine what to run
    should_crawl = args.crawl or args.full_pipeline or args.crawl_only
    should_ingest = args.ingest or args.full_pipeline or args.ingest_only
    should_chat = not (args.crawl_only or args.ingest_only)

    try:
        # Phase 1: Crawling
        if should_crawl:
            success = asyncio.run(run_crawl_phase())
            if not success:
                print("⚠️  Crawling failed. Continuing anyway...\n")

        # Phase 2: Ingestion
        if should_ingest:
            success = run_ingest_phase()
            if not success:
                print("⚠️  Ingestion failed. Continuing anyway...\n")

        # Phase 3: Chat
        if should_chat:
            run_chat_phase()

        print("\n" + "="*60)
        print("  Session Complete")
        print("="*60 + "\n")

    except KeyboardInterrupt:
        print("\n\n👋 Pipeline interrupted. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
