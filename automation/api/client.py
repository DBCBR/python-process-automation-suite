"""
API client module for handling HTTP requests and responses.
"""

import requests
from typing import Optional, Dict, Any


class APIClient:
    """HTTP client for making API requests."""

    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize API client.

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make GET request."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make POST request."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
