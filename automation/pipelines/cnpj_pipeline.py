"""
CNPJ processing pipeline.
"""

import re
from typing import Dict, Any, List
from .base_pipeline import BasePipeline
from automation.utils.validators import ValidadorCNPJ
from automation.services.brasil_api import consultar_cnpj
from automation.utils.logger import get_logger


logger = get_logger(__name__)


class CNPJPipeline(BasePipeline):
    """Pipeline for CNPJ validation and processing."""

    def __init__(self, cnpj_list: List[str] = None):
        """
        Initialize CNPJ pipeline.

        Args:
            cnpj_list: Optional list of CNPJs to process
        """
        super().__init__(name="CNPJ Pipeline")
        self.cnpj_list = cnpj_list or []
        self.results = []

    def execute(self) -> Dict[str, Any]:
        """
        Execute CNPJ processing pipeline.

        Returns:
            Dictionary with CNPJ processing results
        """
        if not self.validate():
            raise ValueError("Pipeline validation failed")

        logger.info(f"Processing {len(self.cnpj_list)} CNPJs")

        for cnpj_input in self.cnpj_list:
            # Validate and clean CNPJ
            validador = ValidadorCNPJ(cnpj_input)
            cnpj_limpo = validador.limpar()

            if cnpj_limpo is None:
                logger.warning(f"Invalid CNPJ: {cnpj_input}")
                continue

            # Query company data
            dados = consultar_cnpj(cnpj_limpo)

            if dados:
                self.results.append(dados)
                logger.info(f"Successfully processed CNPJ: {cnpj_limpo}")

        self.status = "completed"
        return {
            "status": "success",
            "pipeline": self.name,
            "total_processed": len(self.cnpj_list),
            "successful": len(self.results),
            "results": self.results,
        }

    def validate(self) -> bool:
        """
        Validate CNPJ pipeline configuration.

        Returns:
            True if valid
        """
        return True

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
        # Remove duplicates
        return list(set(cnpjs))
