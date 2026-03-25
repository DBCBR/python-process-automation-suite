"""
Base pipeline class for automation workflows.

Implements ETL (Extract, Transform, Load) pattern for data pipelines.
"""

from abc import ABC, abstractmethod
from typing import Any

from automation.utils.logger import get_logger

logger = get_logger(__name__)


class BasePipeline(ABC):
    """Abstract base class for automation pipelines using ETL pattern."""

    def __init__(self, name: str):
        """
        Initialize pipeline.

        Args:
            name: Pipeline name
        """
        self.name = name
        self.status = "initialized"

    def run(self) -> Any:
        """
        Execute ETL pipeline (Extract → Transform → Load).

        Returns:
            Result from load operation
        """
        logger.info(f"[{self.name}] Starting pipeline execution")

        try:
            logger.info(f"[{self.name}] EXTRACT phase")
            data = self.extract()
            logger.debug(
                f"[{self.name}] Extracted {len(data) if isinstance(data, list) else 1} items"
            )

            logger.info(f"[{self.name}] TRANSFORM phase")
            transformed = self.transform(data)
            logger.debug(f"[{self.name}] Transformed data ready")

            logger.info(f"[{self.name}] LOAD phase")
            result = self.load(transformed)

            self.status = "completed"
            logger.info(f"[{self.name}] Pipeline completed successfully")
            return result

        except Exception as e:
            self.status = "failed"
            logger.error(f"[{self.name}] Pipeline failed: {str(e)}", exc_info=True)
            raise

    @abstractmethod
    def extract(self) -> Any:
        """
        Extract data from source.

        Returns:
            Raw data from source
        """
        pass

    @abstractmethod
    def transform(self, data: Any) -> Any:
        """
        Transform data.

        Args:
            data: Raw data from extract phase

        Returns:
            Transformed data
        """
        pass

    @abstractmethod
    def load(self, data: Any) -> Any:
        """
        Load data to destination.

        Args:
            data: Transformed data from transform phase

        Returns:
            Result of load operation
        """
        pass
