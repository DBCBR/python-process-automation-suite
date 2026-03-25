"""
Base pipeline class for automation workflows.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BasePipeline(ABC):
    """Abstract base class for automation pipelines."""

    def __init__(self, name: str):
        """
        Initialize pipeline.

        Args:
            name: Pipeline name
        """
        self.name = name
        self.status = "initialized"

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """
        Execute pipeline.

        Returns:
            Dictionary with pipeline results
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate pipeline configuration.

        Returns:
            True if valid, False otherwise
        """
        pass
