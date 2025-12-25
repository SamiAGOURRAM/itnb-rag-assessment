"""
Web Crawler using Breadth-First Search (BFS) strategy.

This module implements an intelligent web crawler that:
- Uses BFS to systematically discover pages
- Respects domain and locale boundaries
- Implements politeness policies
- Converts HTML to Markdown with metadata
- Preserves source URLs for citation
"""

import asyncio
import time
from collections import deque
from pathlib import Path
from typing import Set, Optional
from urllib.parse import urljoin, urlparse
import hashlib
import re

from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from bs4 import BeautifulSoup

from config import crawler_config, SCRAPED_DIR


class ITNBCrawler:
    """
    Breadth-First Search web crawler for ITNB website.

    This crawler implements a systematic BFS approach to discover and extract
    content from the ITNB website while respecting domain boundaries and
    implementing politeness policies.
    """

    def __init__(self, base_url: str = None):
        """
        Initialize the crawler.

        Args:
            base_url: Starting URL for crawling (defaults to config)
        """
        self.base_url = base_url or crawler_config.base_url
        self.allowed_domain = crawler_config.allowed_domain
        self.required_locale = crawler_config.required_locale
        self.max_pages = crawler_config.max_pages

        # BFS data structures
        self.frontier: deque[str] = deque([self.base_url])
        self.visited: Set[str] = set()
        self.successful_pages: list[dict] = []

        # Rate limiting
        self.request_delay = crawler_config.request_delay
        self.last_request_time = 0

    def _normalize_url(self, url: str) -> str:
        """
        Normalize URL by removing fragments and trailing slashes.

        Args:
            url: URL to normalize

        Returns:
            Normalized URL
        """
        # Remove fragment
        url = url.split("#")[0]
        # Remove trailing slash for consistency
        if url.endswith("/") and url != self.base_url:
            url = url[:-1]
        return url

    def _is_valid_url(self, url: str) -> bool:
        """
        Validate if URL should be crawled based on filtering rules.

        Args:
            url: URL to validate

        Returns:
            True if URL is valid for crawling, False otherwise
        """
        parsed = urlparse(url)

        # Domain lock: Must be within allowed domain
        if self.allowed_domain not in parsed.netloc:
            return False

        # Locale lock: Must contain required locale in path
        if self.required_locale not in parsed.path:
            return False

        # Noise reduction: Filter out non-content extensions
        if any(parsed.path.lower().endswith(ext) for ext in crawler_config.excluded_extensions):
            return False

        # Filter out administrative paths
        if any(excluded in parsed.path.lower() for excluded in crawler_config.excluded_paths):
            return False

        return True

    def _extract_links(self, html: str, current_url: str) -> Set[str]:
        """
        Extract and validate links from HTML content.

        Args:
            html: HTML content
            current_url: Current page URL for resolving relative links

        Returns:
            Set of valid absolute URLs
        """
        soup = BeautifulSoup(html, "html.parser")
        links = set()

        for anchor in soup.find_all("a", href=True):
            href = anchor["href"]

            # Convert relative URLs to absolute
            absolute_url = urljoin(current_url, href)
            normalized_url = self._normalize_url(absolute_url)

            # Validate and add to links
            if self._is_valid_url(normalized_url) and normalized_url not in self.visited:
                links.add(normalized_url)

        return links

    def _url_to_filename(self, url: str) -> str:
        """
        Convert URL to a safe filename.

        Args:
            url: URL to convert

        Returns:
            Safe filename for storing content
        """
        # Create a hash of the URL for uniqueness
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]

        # Extract path for readability
        parsed = urlparse(url)
        path = parsed.path.strip("/").replace("/", "_")

        # Create readable filename
        if path:
            filename = f"{path}_{url_hash}.md"
        else:
            filename = f"index_{url_hash}.md"

        return filename

    def _create_markdown_with_metadata(self, url: str, markdown_content: str, title: str = "") -> str:
        """
        Prepend metadata header to markdown content.

        This ensures every document has traceable source information
        for accurate LLM citations.

        Args:
            url: Source URL
            markdown_content: Extracted markdown content
            title: Page title (optional)

        Returns:
            Markdown content with metadata header
        """
        metadata = f"""---
source_url: {url}
title: {title or "ITNB Page"}
crawled_at: {time.strftime("%Y-%m-%d %H:%M:%S")}
---

# {title or "ITNB Content"}

"""
        return metadata + markdown_content

    async def _crawl_page(self, url: str, crawler: AsyncWebCrawler) -> Optional[dict]:
        """
        Crawl a single page and extract content.

        Args:
            url: URL to crawl
            crawler: AsyncWebCrawler instance

        Returns:
            Dictionary with page data or None if failed
        """
        try:
            # Politeness policy: Rate limiting
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            if time_since_last_request < self.request_delay:
                await asyncio.sleep(self.request_delay - time_since_last_request)

            self.last_request_time = time.time()

            # Crawl the page
            print(f"  Crawling: {url}")
            result = await crawler.arun(url=url)

            if not result.success:
                print(f"  ✗ Failed to crawl: {url}")
                return None

            # Extract title
            soup = BeautifulSoup(result.html, "html.parser")
            title = soup.find("title")
            title_text = title.get_text().strip() if title else ""

            # Get markdown content
            markdown_content = result.markdown

            # Create markdown with metadata
            final_markdown = self._create_markdown_with_metadata(
                url=url,
                markdown_content=markdown_content,
                title=title_text
            )

            # Save locally
            filename = self._url_to_filename(url)
            filepath = SCRAPED_DIR / filename
            filepath.write_text(final_markdown, encoding="utf-8")

            print(f"  ✓ Saved: {filename}")

            # Extract new links for BFS frontier
            new_links = self._extract_links(result.html, url)

            return {
                "url": url,
                "title": title_text,
                "filepath": str(filepath),
                "markdown": final_markdown,
                "new_links": new_links,
            }

        except Exception as e:
            print(f"  ✗ Error crawling {url}: {str(e)}")
            return None

    async def crawl(self) -> list[dict]:
        """
        Execute BFS crawl of ITNB website.

        Returns:
            List of successfully crawled page data
        """
        print(f"\n{'='*60}")
        print(f"Starting BFS Crawl of {self.base_url}")
        print(f"{'='*60}\n")

        async with AsyncWebCrawler(verbose=False) as crawler:
            while self.frontier and (self.max_pages is None or len(self.visited) < self.max_pages):
                # BFS: Process from front of queue
                current_url = self.frontier.popleft()

                # Skip if already visited
                if current_url in self.visited:
                    continue

                # Mark as visited
                self.visited.add(current_url)

                # Crawl the page
                page_data = await self._crawl_page(current_url, crawler)

                if page_data:
                    self.successful_pages.append(page_data)

                    # Add new links to frontier (BFS: append to end)
                    for link in page_data["new_links"]:
                        if link not in self.visited and link not in self.frontier:
                            self.frontier.append(link)

        print(f"\n{'='*60}")
        print(f"Crawl Complete!")
        print(f"  Pages Visited: {len(self.visited)}")
        print(f"  Successfully Scraped: {len(self.successful_pages)}")
        print(f"  Files Saved: {SCRAPED_DIR}")
        print(f"{'='*60}\n")

        return self.successful_pages


async def run_crawler() -> list[dict]:
    """
    Convenience function to run the crawler.

    Returns:
        List of crawled page data
    """
    crawler = ITNBCrawler()
    return await crawler.crawl()


if __name__ == "__main__":
    # Test the crawler
    asyncio.run(run_crawler())
