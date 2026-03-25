"""
CNPJ processing pipeline using ETL pattern.
"""

import re
from typing import List

from .base_pipeline import BasePipeline
from automation.utils.validators import ValidadorCNPJ
from automation.services.brasil_api import consultar_cnpj
from automation.utils.logger import get_logger


logger = get_logger(__name__)


class CNPJPipeline(BasePipeline):
    """Pipeline for CNPJ validation and data enrichment using ETL pattern."""

    def __init__(self, cnpj_list: List[str] = None, text_source: str = None):
        """
        Initialize CNPJ pipeline.

        Args:
            cnpj_list: Optional list of CNPJs to process
            text_source: Optional text to extract CNPJs from
        """
        super().__init__(name="CNPJ Pipeline")
        self.cnpj_list = cnpj_list or []
        self.text_source = text_source
        self.results = []

    def extract(self) -> List[str]:
        """
        Extract CNPJ numbers from source (list or text).

        Returns:
            List of CNPJs to process
        """
        if self.text_source:
            logger.info("Extracting CNPJs from text")
            cnpjs = self.extract_cnpjs_from_text(self.text_source)
            logger.debug(f"Found {len(cnpjs)} unique CNPJs")
            return cnpjs

        logger.info(f"Using provided list of {len(self.cnpj_list)} CNPJs")
        return self.cnpj_list

    def transform(self, cnpj_list: List[str]) -> List[dict]:
        """
        Transform and validate CNPJs, enrich with company data from BrasilAPI.

        Args:
            cnpj_list: List of CNPJs to transform

        Returns:
            List of validated and enriched CNPJ data
        """
        enriched_data = []

        for cnpj_input in cnpj_list:
            # Validate and clean CNPJ
            validador = ValidadorCNPJ(cnpj_input)
            cnpj_limpo = validador.limpar()

            if cnpj_limpo is None:
                logger.warning(f"Invalid CNPJ format: {cnpj_input}")
                continue

            # Query company data from BrasilAPI
            try:
                dados = consultar_cnpj(cnpj_limpo)
                if dados:
                    enriched_data.append(dados)
                    logger.debug(f"Enriched CNPJ: {cnpj_limpo}")
            except Exception as e:
                logger.warning(f"Failed to enrich CNPJ {cnpj_limpo}: {str(e)}")
                continue

        return enriched_data

    def load(self, data: List[dict]) -> dict:
        """
        Load processed data and prepare results.

        Args:
            data: List of enriched company data

        Returns:
            Dictionary with pipeline results and summary
        """
        self.results = data

        result = {
            "pipeline": self.name,
            "status": "success",
            "total_processed": len(data),
            "results": data,
        }

        logger.info(f"Pipeline loaded {len(data)} records")
        return result

    def extract_cnpjs_from_text(self, text: str) -> List[str]:
        """
        Extract CNPJ numbers from text using regex.

        Args:
            text: Text to search for CNPJs

        Returns:
            List of unique CNPJs found
        """
        pattern = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"
        cnpjs = re.findall(pattern, text)
        # Remove duplicates and return
        return list(set(cnpjs))
