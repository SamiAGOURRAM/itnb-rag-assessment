"""
Clean re-ingestion script.

Deletes the existing bucket and creates a fresh one with proper source URLs.
"""

from src.groundx_client import GroundXClient

def main():
    print("\n" + "="*60)
    print("  CLEAN RE-INGESTION")
    print("  Deleting old bucket and creating fresh data")
    print("="*60 + "\n")

    client = GroundXClient()

    # Step 1: Get existing bucket
    print("Step 1: Finding existing bucket...")
    client.get_or_create_bucket()

    # Step 2: Delete bucket completely
    print("\nStep 2: Deleting existing bucket (this removes all old data)...")
    client.delete_bucket()

    # Step 3: Create fresh bucket
    print("\nStep 3: Creating fresh bucket...")
    client.get_or_create_bucket()

    # Step 4: Ingest all documents with proper source URLs
    print("\nStep 4: Ingesting documents with proper source URLs...")
    result = client.ingest_documents()

    print("\n" + "="*60)
    print(f"✅ Clean re-ingestion completed!")
    print(f"   - Documents ingested: {result.get('count', 0)}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
