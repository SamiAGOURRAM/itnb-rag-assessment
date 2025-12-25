"""
System Health Check Module

Performs comprehensive health checks on all system components before
allowing user interaction. This helps identify configuration issues early.
"""

import sys
import os
from typing import Dict, Tuple
from openai import OpenAI
from groundx import GroundX

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import groundx_config, llm_config, langfuse_config


class HealthChecker:
    """Performs health checks on system components."""

    def __init__(self):
        self.results = {}

    def _print_header(self):
        """Print health check header."""
        print("\n" + "="*60)
        print("  🏥 SYSTEM HEALTH CHECK")
        print("="*60 + "\n")

    def _print_check(self, name: str, status: str, message: str = ""):
        """Print individual check result."""
        symbols = {
            "✓": "✓",  # Success
            "✗": "✗",  # Failure
            "⚠": "⚠",  # Warning
        }
        symbol = symbols.get(status, "○")

        if message:
            print(f"{symbol} {name}: {message}")
        else:
            print(f"{symbol} {name}")

    def check_groundx(self) -> Tuple[bool, str]:
        """
        Check GroundX API connectivity and authentication.

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if not groundx_config.api_key:
                return False, "API key not configured"

            client = GroundX(api_key=groundx_config.api_key)

            # Try to list buckets as a health check
            response = client.buckets.list()

            if hasattr(response, 'buckets'):
                bucket_count = len(response.buckets) if response.buckets else 0
                return True, f"Connected ({bucket_count} buckets found)"
            else:
                return True, "Connected"

        except Exception as e:
            return False, f"Connection failed: {str(e)[:50]}"

    def check_llm(self) -> Tuple[bool, str]:
        """
        Check LLM API connectivity.

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if not llm_config.api_key:
                return False, "API key not configured"

            client = OpenAI(
                api_key=llm_config.api_key,
                base_url=llm_config.api_base
            )

            # Try to list models as a health check
            models = client.models.list()

            if models.data:
                # Check if our configured model is available
                model_ids = [m.id for m in models.data]
                if llm_config.model_name in model_ids:
                    return True, f"Connected (model: {llm_config.model_name})"
                else:
                    return False, f"Model '{llm_config.model_name}' not available"
            else:
                return True, "Connected"

        except Exception as e:
            error_msg = str(e)
            if "getaddrinfo failed" in error_msg or "Connection" in error_msg:
                return False, "Network connection failed"
            return False, f"Connection failed: {error_msg[:50]}"

    def check_langfuse(self) -> Tuple[bool, str]:
        """
        Check Langfuse observability configuration.

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if not langfuse_config.is_configured:
                return True, "Not configured (optional)"

            from langfuse import Langfuse

            client = Langfuse(
                public_key=langfuse_config.public_key,
                secret_key=langfuse_config.secret_key,
                host=langfuse_config.host
            )

            # Simple check - if no exception, it's configured
            return True, f"Configured ({langfuse_config.host})"

        except ImportError:
            return True, "Not installed (optional)"
        except Exception as e:
            return False, f"Configuration error: {str(e)[:50]}"

    def run_all_checks(self) -> bool:
        """
        Run all health checks and display results.

        Returns:
            bool: True if all critical checks pass, False otherwise
        """
        self._print_header()

        # Check GroundX (critical)
        print("Checking GroundX Vector Database...")
        groundx_ok, groundx_msg = self.check_groundx()
        self._print_check("GroundX API", "✓" if groundx_ok else "✗", groundx_msg)
        self.results['groundx'] = groundx_ok

        # Check LLM (critical)
        print("\nChecking LLM API Endpoint...")
        llm_ok, llm_msg = self.check_llm()
        self._print_check("LLM API", "✓" if llm_ok else "✗", llm_msg)
        self.results['llm'] = llm_ok

        # Check Langfuse (optional)
        print("\nChecking Langfuse Observability...")
        langfuse_ok, langfuse_msg = self.check_langfuse()
        symbol = "✓" if langfuse_ok else "⚠"
        self._print_check("Langfuse", symbol, langfuse_msg)
        self.results['langfuse'] = langfuse_ok

        # Summary
        print("\n" + "-"*60)

        all_critical_ok = groundx_ok and llm_ok

        if all_critical_ok:
            print("✓ All critical systems operational")
            print("="*60 + "\n")
            return True
        else:
            print("✗ System health check failed!")
            print("\nFailed components:")
            if not groundx_ok:
                print("  - GroundX: Check GROUNDX_API_KEY in .env")
            if not llm_ok:
                print("  - LLM API: Check network connection and API credentials")
            print("\nPlease fix the issues above before continuing.")
            print("="*60 + "\n")
            return False


def run_health_check() -> bool:
    """
    Convenience function to run health check.

    Returns:
        bool: True if healthy, False otherwise
    """
    checker = HealthChecker()
    return checker.run_all_checks()


if __name__ == "__main__":
    # Test health check
    healthy = run_health_check()
    sys.exit(0 if healthy else 1)
