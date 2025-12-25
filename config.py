"""
Configuration management for ITNB RAG Assessment.

This module centralizes all configuration settings, environment variables,
and constants used throughout the application.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
SCRAPED_DIR = DATA_DIR / "scraped"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"

# Ensure directories exist
SCRAPED_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class CrawlerConfig:
    """Configuration for the web crawler."""

    base_url: str = "https://www.itnb.ch/en"
    allowed_domain: str = "itnb.ch"
    required_locale: str = "/en/"
    max_concurrent_requests: int = 3
    request_delay: float = 1.0  # Politeness policy: 1 second between requests
    excluded_extensions: tuple = (".css", ".js", ".pdf", ".jpg", ".png", ".gif", ".svg", ".ico")
    excluded_paths: tuple = ("/contact", "/login", "/admin", "/api")
    max_pages: Optional[int] = 50  # Safety limit to prevent infinite crawling


@dataclass
class GroundXConfig:
    """Configuration for GroundX API."""

    api_key: str = os.getenv("GROUNDX_API_KEY", "")
    bucket_name: str = "itnb-knowledge-base"
    base_url: str = "https://api.groundx.ai/api"


@dataclass
class LLMConfig:
    """Configuration for LLM API (OpenAI-compatible)."""

    model_name: str = os.getenv("OPENAI_MODEL_NAME", "openai/inference-llama4-maverick")
    api_base: str = os.getenv("OPENAI_API_BASE", "https://maas.ai-2.kvant.cloud")
    api_key: str = os.getenv("OPENAI_API_KEY", "sk-E4CQTJ7DRMNt88yzgaOLfg")
    temperature: float = 0.3  # Lower temperature for more factual responses
    max_tokens: int = 1000
    top_k: int = 5  # Number of chunks to retrieve from GroundX

    # Conversational memory settings
    use_conversation_memory: bool = os.getenv("USE_CONVERSATION_MEMORY", "true").lower() == "true"
    max_history_messages: int = 5  # Keep last N message pairs (user + assistant)


@dataclass
class LangfuseConfig:
    """Configuration for Langfuse observability."""

    public_key: str = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret_key: str = os.getenv("LANGFUSE_SECRET_KEY", "")
    host: str = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    enabled: bool = bool(public_key and secret_key)  # Auto-enable if keys present

    @property
    def is_configured(self) -> bool:
        """Check if Langfuse is properly configured."""
        return bool(self.public_key and self.secret_key)


# Global configuration instances
crawler_config = CrawlerConfig()
groundx_config = GroundXConfig()
llm_config = LLMConfig()
langfuse_config = LangfuseConfig()


def validate_config() -> tuple[bool, list[str]]:
    """
    Validate that all required configuration is present.

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    if not groundx_config.api_key:
        errors.append("GROUNDX_API_KEY environment variable is required")

    if not llm_config.api_key:
        errors.append("OPENAI_API_KEY environment variable is required")

    return len(errors) == 0, errors


def print_config_status() -> None:
    """Print configuration status for debugging."""
    print("=== Configuration Status ===")
    print(f"GroundX API: {'✓ Configured' if groundx_config.api_key else '✗ Missing API Key'}")
    print(f"LLM API: {'✓ Configured' if llm_config.api_key else '✗ Missing API Key'}")
    print(f"Langfuse: {'✓ Enabled' if langfuse_config.is_configured else '○ Disabled (Optional)'}")
    print(f"Data Directory: {SCRAPED_DIR}")
    print("=" * 30)
