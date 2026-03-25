"""
Main entry point for the application.
"""

import re
from automation.utils.logger import get_logger
from automation.utils.validators import ValidadorCNPJ
from automation.services.brasil_api import consultar_cnpj
from automation.pipelines.cnpj_pipeline import CNPJPipeline
from config.settings import settings


logger = get_logger(__name__)


def main():
    """Main application entry point."""
    logger.info(f"Starting application - Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    # Example: Run CNPJ Pipeline
    pipeline = CNPJPipeline()

    if pipeline.validate():
        logger.info("Pipeline validation successful")
        result = pipeline.execute()
        logger.info(f"Pipeline result: {result}")
    else:
        logger.error("Pipeline validation failed")

    main()
