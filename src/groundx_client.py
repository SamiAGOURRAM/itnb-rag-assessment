"""
GroundX API Client for document ingestion and retrieval.

This module provides a clean interface to the GroundX API for:
- Bucket management
- Document ingestion
- Semantic search and retrieval
"""

from pathlib import Path
from typing import List, Dict, Optional
import time

from groundx import GroundX, Document

from config import groundx_config, SCRAPED_DIR


class GroundXClient:
    """
    Client for interacting with GroundX API.

    Handles bucket management, document ingestion, and search operations
    with proper error handling and logging.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize GroundX client.

        Args:
            api_key: GroundX API key (defaults to config)
        """
        self.api_key = api_key or groundx_config.api_key
        if not self.api_key:
            raise ValueError("GroundX API key is required")

        self.client = GroundX(api_key=self.api_key)
        self.bucket_id: Optional[int] = None
        self.bucket_name = groundx_config.bucket_name

    def get_or_create_bucket(self) -> int:
        """
        Get existing bucket or create new one.

        This implements idempotent bucket creation - if the bucket exists,
        it retrieves the ID; otherwise, it creates a new bucket.

        Returns:
            Bucket ID

        Raises:
            Exception: If bucket creation/retrieval fails
        """
        try:
            print(f"\n{'='*60}")
            print(f"Initializing GroundX Bucket: {self.bucket_name}")
            print(f"{'='*60}\n")

            # Try to list existing buckets
            buckets_response = self.client.buckets.list()

            # Check if our bucket exists
            existing_bucket = None
            if hasattr(buckets_response, 'buckets'):
                for bucket in buckets_response.buckets:
                    if bucket.name == self.bucket_name:
                        existing_bucket = bucket
                        break

            if existing_bucket:
                self.bucket_id = existing_bucket.bucket_id
                print(f"  ✓ Found existing bucket")
                print(f"    - Bucket ID: {self.bucket_id}")
                print(f"    - Bucket Name: {self.bucket_name}")
            else:
                # Create new bucket
                print(f"  ○ Creating new bucket: {self.bucket_name}")
                create_response = self.client.buckets.create(name=self.bucket_name)

                # Response structure: response.bucket.bucket_id
                self.bucket_id = create_response.bucket.bucket_id
                print(f"  ✓ Bucket created successfully")
                print(f"    - Bucket ID: {self.bucket_id}")

            print(f"\n{'='*60}\n")
            return self.bucket_id

        except Exception as e:
            print(f"  ✗ Error with bucket management: {str(e)}")
            raise

    def delete_bucket(self):
        """
        Delete the entire bucket and all its contents.

        This is useful for starting fresh with clean data.
        """
        if not self.bucket_id:
            print("  ○ No bucket to delete")
            return

        try:
            print(f"\n{'='*60}")
            print(f"Deleting Bucket: {self.bucket_name}")
            print(f"{'='*60}\n")

            self.client.buckets.delete(bucket_id=self.bucket_id)
            print(f"  ✓ Bucket deleted successfully")
            print(f"    - Bucket ID: {self.bucket_id}")

            self.bucket_id = None

            print(f"\n{'='*60}\n")

        except Exception as e:
            print(f"  ✗ Error deleting bucket: {str(e)}")
            raise

    def ingest_documents(self, file_paths: List[Path] = None) -> Dict[str, any]:
        """
        Ingest documents into GroundX bucket.

        Args:
            file_paths: List of file paths to ingest (defaults to all scraped files)

        Returns:
            Dictionary with ingestion results

        Raises:
            Exception: If ingestion fails
        """
        if not self.bucket_id:
            self.get_or_create_bucket()

        # Default to all scraped markdown files
        if file_paths is None:
            file_paths = list(SCRAPED_DIR.glob("*.md"))

        if not file_paths:
            print("  ⚠ No files found to ingest")
            return {"status": "no_files", "count": 0}

        print(f"\n{'='*60}")
        print(f"Ingesting Documents to GroundX")
        print(f"{'='*60}\n")
        print(f"  Bucket ID: {self.bucket_id}")
        print(f"  Documents: {len(file_paths)} files")
        print()

        try:
            # Prepare documents for ingestion using GroundX Document class
            documents = []
            for file_path in file_paths:
                # Extract source URL from markdown frontmatter
                source_url = ""
                try:
                    content = file_path.read_text(encoding='utf-8')
                    if content.startswith('---'):
                        frontmatter_end = content.find('---', 3)
                        if frontmatter_end > 0:
                            frontmatter = content[3:frontmatter_end]
                            for line in frontmatter.split('\n'):
                                if line.startswith('source_url:'):
                                    source_url = line.split('source_url:')[1].strip()
                                    break
                except Exception:
                    pass  # Silently fail if can't extract source URL

                documents.append(
                    Document(
                        bucket_id=self.bucket_id,
                        file_name=file_path.name,
                        file_path=str(file_path),
                        file_type="txt",  # Markdown as text
                        search_data={"source_url": source_url} if source_url else {}
                    )
                )

            print(f"  ○ Extracted source URLs from {len([d for d in documents if d.search_data])} documents")

            # Ingest documents using the correct API method
            print(f"  ○ Uploading documents...")
            ingest_response = self.client.ingest(documents=documents)

            # Extract process ID from response
            process_id = ingest_response.ingest.process_id

            print(f"  ✓ Ingestion started successfully")
            print(f"    - Process ID: {process_id}")
            print(f"    - Documents: {len(file_paths)} files")

            # Wait a moment for processing
            print(f"\n  ○ Waiting for documents to be processed...")
            time.sleep(10)  # Give it more time to process

            print(f"\n{'='*60}\n")

            return {
                "status": "success",
                "process_id": process_id,
                "count": len(file_paths),
                "bucket_id": self.bucket_id,
            }

        except Exception as e:
            print(f"  ✗ Ingestion failed: {str(e)}")
            raise

    def search(self, query: str, n: int = 5) -> List[Dict[str, any]]:
        """
        Search for relevant documents in GroundX.

        Args:
            query: Search query
            n: Number of results to return

        Returns:
            List of search results with content and metadata

        Raises:
            Exception: If search fails
        """
        if not self.bucket_id:
            raise ValueError("Bucket not initialized. Call get_or_create_bucket() first.")

        try:
            # Perform search
            search_response = self.client.search.content(
                id=self.bucket_id,
                query=query,
                n=n
            )

            # Parse results - response structure: search_response.search.results
            results = []
            if hasattr(search_response, 'search') and hasattr(search_response.search, 'results'):
                for result in search_response.search.results:
                    # Extract source URL from search_data if available, otherwise use default source_url
                    source_url = ""
                    if hasattr(result, 'search_data') and result.search_data:
                        source_url = result.search_data.get('source_url', '')
                    if not source_url and hasattr(result, 'source_url'):
                        source_url = result.source_url

                    results.append({
                        "text": result.text if hasattr(result, 'text') else "",
                        "score": result.score if hasattr(result, 'score') else 0.0,
                        "source_url": source_url,
                        "chunk_id": result.chunk_id if hasattr(result, 'chunk_id') else "",
                    })

            return results

        except Exception as e:
            print(f"  ✗ Search failed: {str(e)}")
            raise


def test_groundx_client():
    """Test function for GroundX client."""
    client = GroundXClient()

    # Test bucket creation
    bucket_id = client.get_or_create_bucket()
    print(f"Bucket ID: {bucket_id}")

    # Test ingestion
    result = client.ingest_documents()
    print(f"Ingestion result: {result}")

    # Test search
    search_results = client.search("What does ITNB do?", n=3)
    for i, result in enumerate(search_results, 1):
        print(f"\nResult {i}:")
        print(f"  Score: {result['score']}")
        print(f"  Source: {result['source_url']}")
        print(f"  Text: {result['text'][:200]}...")


if __name__ == "__main__":
    test_groundx_client()
